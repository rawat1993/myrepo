from django.contrib import admin
from djangoChat.models import Message,ChatUser


admin.site.register(Message)
admin.site.register(ChatUser)
# optional ordering
