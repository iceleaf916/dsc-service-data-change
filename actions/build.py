#! /usr/bin/env python
# -*- coding: utf-8 -*-

from deepin_utils.file import get_parent_dir
import subprocess
import tarfile
import os, sys
from upyun import UpYun
from deepin_utils.file import remove_file, remove_directory, create_directory
from deepin_utils.hash import md5_file
from deepin_utils.date_time import get_current_time
import getpass
import json

BUILD_ORIGIN_DATA = 1
BUILD_UPDATE_PATCH = 2

DATA_ORIGIN_DIR = os.path.join(get_parent_dir(__file__, 3), "deepin-software-center-data", "data", "origin")
TIME_FLAG_FILE = os.path.join(get_parent_dir(__file__, 3), "deepin-software-center-data", "data", "origin_data_time")
    
class Build(object):
    '''
    class docs
    '''
    
    def __init__(self, 
            space_name, 
            action_type, 
            input_data_dir, 
            output_data_dir,
            server_data_dir,
            action):
        '''
        init docs
        '''
        # Init.
        self.space_name = space_name
        self.input_data_dir = input_data_dir
        self.output_data_dir = output_data_dir
        self.server_data_dir = server_data_dir
        self.action = action
        
        if not os.path.exists(DATA_ORIGIN_DIR):
            create_directory(DATA_ORIGIN_DIR)

        self.data_origin_file = os.path.join(DATA_ORIGIN_DIR, "%s.tar.gz" % self.space_name)

        if action_type == BUILD_ORIGIN_DATA:
            self.build_origin_data(self.action[1])
        if action_type == BUILD_UPDATE_PATCH:
            self.build_update_patch(self.action[1])

    def check_permission(self, space_name):
        # Set upyun information.
        username = raw_input("Username: ")
        password = getpass.getpass()
        self.server = UpYun(space_name, username, password)
        self.server.setApiDomain('v0.api.upyun.com')
        if self.server.getFileInfo("/") <> None:
            return True
        else:
            print "验证失败..."
            return False
                
    def upload_file(self, 
                    local_file,
                    remote_file,
                    data_name):
        if self.server.getFileInfo(remote_file):
            print "%s: 删除远端%s..." % (self.space_name, data_name)
            self.server.deleteFile(remote_file)
            print "%s: 删除远端%s完成" % (self.space_name, data_name)
            
        print "%s: 上传远端%s..." % (self.space_name, data_name)    
        self.server.setContentMD5(md5_file(local_file))
        with open(local_file, "rb") as patch_list_file:
            if self.server.writeFile(remote_file, patch_list_file.read(), True):
                print "%s: 上传远端%s成功" % (self.space_name, data_name)    
            else:
                print "%s: 上传远端%s失败" % (self.space_name, data_name)    

    def delete_remote_file(self, remote_file, data_name):
        if self.server.getFileInfo(remote_file):
            print "%s: 删除远端%s..." % (self.space_name, data_name)
            self.server.deleteFile(remote_file)
            print "%s: 删除远端%s完成" % (self.space_name, data_name)
        else:
            print "%s: 远端不存在%s" % (self.space_name, data_name)
                
    def build_origin_data(self, action):
        if action == "build":
            # Delete origin data
            remove_file(self.data_origin_file)
            
            # Build origin data.
            print "%s: 创建本地原始数据..." % (self.space_name)
            with tarfile.open(self.data_origin_file, "w:gz") as tar:
                for root, dir, files in os.walk(self.input_data_dir):
                    for file in files:
                        fullpath=os.path.join(root, file)
                        tar.add(fullpath, fullpath.split(self.input_data_dir)[1], False)
            print "%s: 创建本地原始数据完成" % (self.space_name)
            with open(TIME_FLAG_FILE, 'w') as fp:
                s = get_current_time("%Y_%m_%d_%H:%M:%S")
                fp.write(s)

        if action == "upload" and self.check_permission(self.space_name):
            remote_origin_file_path = os.path.join(
                    self.server_data_dir, 
                    "origin", 
                    md5_file(self.data_origin_file), 
                    "%s.tar.gz" % self.space_name)
            self.upload_file(self.data_origin_file, remote_origin_file_path, "原始数据")
    
    def build_update_patch(self, action):
        if os.path.exists(self.data_origin_file):
            self.output_patch_dir = os.path.join(self.output_data_dir, "patch")
            if not os.path.exists(self.output_patch_dir):
                create_directory(self.output_patch_dir)

            self.output_temp_dir = os.path.join(self.output_data_dir, "temp")
            self.output_temp_file = os.path.join(self.output_temp_dir, "%s.tar.gz" % self.space_name)
            self.output_temp_patch_file = os.path.join(self.output_temp_dir, "patch")

            self.patch_md5_file = os.path.join(self.output_patch_dir, "patch_md5.json")
            self.origin_data_md5 = md5_file(self.data_origin_file)
            if not os.path.exists(self.patch_md5_file):
                self.patch_md5_json = {}
                self.patch_md5_json["origin_data"] = self.origin_data_md5
                self.patch_md5_json["current_patch"] = []
            else:
                self.patch_md5_json = json.load(open(self.patch_md5_file))

            if self.patch_md5_json["origin_data"] != self.origin_data_md5:
                self.patch_md5_json["origin_data"] = self.origin_data_md5
                self.patch_md5_json["current_patch"] = []

            self.remote_patch_dir = os.path.join(self.server_data_dir, "patch")

            if action == "build":
                # Delete temp directory first.
                create_directory(self.output_temp_dir, True)

                # Build temp file.
                print "%s: 创建本地更新数据..." % self.space_name    
                with tarfile.open(self.output_temp_file, "w:gz") as tar:
                    for root, dir, files in os.walk(self.input_data_dir):
                        for file in files:
                            fullpath=os.path.join(root, file)
                            tar.add(fullpath, fullpath.split(self.input_data_dir)[1], False)
                print "%s: 创建本地更新数据完成" % self.space_name    
                
                print "%s: 生成补丁文件..." % self.space_name    
                subprocess.Popen(
                    "xdelta3 -ves %s %s %s" % (
                        self.data_origin_file,
                        self.output_temp_file,
                        self.output_temp_patch_file),
                    shell=True).wait()
                
                newest_patch_file_md5 = md5_file(self.output_temp_patch_file)
                current_patch_dict = self.patch_md5_json.get("current_patch")
                if current_patch_dict:
                    last_patch_md5 = current_patch_dict[0]["md5"]
                    if last_patch_md5 == newest_patch_file_md5:
                        remove_directory(self.output_temp_dir)
                        print "%s: input_data数据未做任何改变，删除相同补丁文件" % self.space_name
                        sys.exit(0)
                else:
                    current_patch_dict = []
                newest_patch_dir = os.path.join(self.output_patch_dir, self.origin_data_md5)
                if not os.path.exists(newest_patch_dir):
                    create_directory(newest_patch_dir)

                newest_patch_name = "%s-%s.xd3" % (self.space_name, get_current_time("%Y_%m_%d_%H:%M:%S"))
                newest_patch_file = os.path.join(newest_patch_dir, newest_patch_name)

                os.renames(self.output_temp_patch_file, newest_patch_file)
                remove_directory(self.output_temp_dir)
                current_patch_dict.insert(0, {"name" : newest_patch_name, "md5" : newest_patch_file_md5})
                print "%s: 生成补丁文件完成" % self.space_name    
                
                print "%s: 写入补丁md5..." % self.space_name
                self.patch_md5_json["current_patch"] = current_patch_dict
                with open(self.patch_md5_file, "w") as fp:
                    json.dump(self.patch_md5_json, fp)
                print "%s: 写入补丁md5完成" % self.space_name
                
            elif action == "upload" and self.check_permission(self.space_name):
                # Upload patch file.
                current_patch_dict = self.patch_md5_json.get("current_patch")
                if current_patch_dict != []:
                    if len(current_patch_dict) > 2:
                        print "%s: 清理多余的补丁" % self.space_name
                        spare_patchs = current_patch_dict[2:]
                        current_patch_dict = current_patch_dict[:2]
                        for patch in spare_patchs:
                            patch_name = patch["name"].encode("utf-8")
                            local_path = os.path.join(self.output_patch_dir, self.origin_data_md5, patch_name)
                            try:
                                remove_file(local_path)
                                print "%s: 清除了补丁%s" % (self.space_name, patch_name)
                            except:
                                pass
                            remote_path = os.path.join(self.remote_patch_dir, self.origin_data_md5, patch_name)
                            self.delete_remote_file(remote_path, patch_name)
                        self.patch_md5_json["current_patch"] = current_patch_dict
                        with open(self.patch_md5_file, "w") as fp:
                            json.dump(self.patch_md5_json, fp)

                    newest_patch_name = current_patch_dict[0]["name"].encode("utf-8")
                    newest_patch_file = os.path.join(self.output_patch_dir, self.origin_data_md5, newest_patch_name)
                    remote_patch_file = os.path.join(self.remote_patch_dir, self.origin_data_md5, newest_patch_name)
                    remote_patch_md5_file = os.path.join(self.remote_patch_dir, self.origin_data_md5, "patch_md5.json")

                    # upload newest_patch_file
                    self.upload_file(newest_patch_file, remote_patch_file, "补丁更新数据")

                    # Update patch list file.
                    self.upload_file(self.patch_md5_file, remote_patch_md5_file, "补丁md5列表文件")
                else:
                    print "%s: 当前没有任何补丁，请打好补丁再上传吧！" % self.space_name
        else:
            print "%s: %s 不存在， 无法进行补丁的创建和上传" % (self.space_name, self.data_origin_file)
