from django.contrib import admin
from .models import Chat, Group, UserInfo

# Register your models here.

@admin.register(Chat)
class ChatModelAdmin(admin.ModelAdmin):
    list_display = ['content', 'timestamp', 'room', 'sender', 'is_status']

@admin.register(Group)
class GroupModelAdmin(admin.ModelAdmin):
    list_display = ['name']
    
@admin.register(UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    list_display = ['userinfo', 'password']