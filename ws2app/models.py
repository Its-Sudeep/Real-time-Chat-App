from django.db import models

class Chat(models.Model):
    content = models.CharField(max_length=1000)
    timestamp = models.DateTimeField(auto_now=True)
    room = models.ForeignKey('Group', on_delete=models.CASCADE)
    sender = models.CharField(max_length=100, default="")
    is_status = models.BooleanField(null=True)
    
    def __str__(self) -> str:
        return f"{self.content}{self.sender}"

class Group(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"
    
class UserInfo(models.Model):
    userinfo = models.CharField(max_length=1000)
    password = models.CharField(max_length=1000, default="")
    
    def __str__(self):
        return f"{self.userinfo}"
    
    