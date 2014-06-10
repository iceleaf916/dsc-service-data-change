#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2011 ~ 2012 Deepin, Inc.
#               2011 ~ 2012 Wang Yong
# 
# Author:     Wang Yong <lazycat.manatee@gmail.com>
# Maintainer: Wang Yong <lazycat.manatee@gmail.com>
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import tarfile
import sys

from deepin_utils.file import remove_file, get_parent_dir
from deepin_utils.date_time import get_current_time

database_dir = os.path.join(get_parent_dir(__file__, 2), "database/data")
deepin_software_center_data_dir = os.path.join(get_parent_dir(__file__, 3), "deepin-software-center-data")
TIME_FLAG_FILE = os.path.join(deepin_software_center_data_dir, "data", "origin_data_time")

def update_origin_data(space_name):
    data_origin_file = os.path.join(deepin_software_center_data_dir, "data/origin/dsc-%s-data.tar.gz" % space_name)
    input_data_dir = os.path.join(database_dir, space_name)

    remove_file(data_origin_file)
    
    # Build origin data.
    print "%s: 创建本地原始数据..." % (space_name)
    with tarfile.open(data_origin_file, "w:gz") as tar:
        for root, dir, files in os.walk(input_data_dir):
            for file in files:
                fullpath=os.path.join(root, file)
                tar.add(fullpath, fullpath.split(database_dir)[1], False)
    print "%s: 创建本地原始数据完成" % (space_name)
    with open(TIME_FLAG_FILE, 'w') as fp:
        s = get_current_time("%Y_%m_%d_%H:%M:%S")
        fp.write(s)

if __name__ == "__main__":
    args = os.listdir(database_dir)
    if sys.argv[1] in args:
        update_origin_data(sys.argv[1])
