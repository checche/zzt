from django.contrib import admin
from .models import Tweet, CustomUser
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

class TweetAdmin(admin.ModelAdmin):
    list_display = ('author', 'text')

class MyUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'screenname', 'email', 'password')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    list_display = ('username', 'screenname', 'email', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email', 'username', 'screnname')
    filter_horizontal = ('groups', 'user_permissions')

admin.site.register(Tweet, TweetAdmin)
admin.site.register(CustomUser, MyUserAdmin)