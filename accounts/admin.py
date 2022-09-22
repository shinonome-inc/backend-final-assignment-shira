from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import Follower

User = get_user_model()

admin.site.register(User)
admin.site.register(Follower)
