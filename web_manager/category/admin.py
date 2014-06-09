from django.contrib import admin

from category.models import Firstcategory, Secondcategory, FirstcategoryL10n, SecondcategoryL10n

class FirstcategoryL10nInline(admin.TabularInline):
    model = FirstcategoryL10n

class FirstcategoryAdmin(admin.ModelAdmin):
    list_display = ('id_name', 'alias_name', 'order')
    list_editable = ('order',)
    inlines = [FirstcategoryL10nInline,]

class SecondcategoryL10nInline(admin.TabularInline):
    model = SecondcategoryL10n

class SecondcategoryAdmin(admin.ModelAdmin):
    list_display = ('id_name', 'alias_name', 'order', 'first_category')
    list_editable = ('order',)
    inlines = [SecondcategoryL10nInline,]

admin.site.register(Firstcategory, FirstcategoryAdmin)
admin.site.register(Secondcategory, SecondcategoryAdmin)
