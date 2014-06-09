from django.contrib import admin

from software.models import Software, SoftwareL10n

class SoftwareL10nInline(admin.TabularInline):
    model = SoftwareL10n

class SoftwareAdmin(admin.ModelAdmin):
    inlines = [SoftwareL10nInline,]

admin.site.register(Software, SoftwareAdmin)
