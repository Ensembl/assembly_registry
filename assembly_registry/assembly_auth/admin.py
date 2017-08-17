from django.contrib import admin
from assembly_auth.models import Profile
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


# Register your models here.
class UserProfileInline(admin.StackedInline):
    model = Profile


class UserAdmin(UserAdmin):
    '''ModelAdmin Class to alter the display for Users'''
    inlines = [UserProfileInline, ]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
