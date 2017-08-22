from django.contrib import admin

# Register your models here.

from .models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Activity)
admin.site.register(Like)
admin.site.register(Bookmark)
admin.site.register(Share)
admin.site.register(Relationship)
admin.site.register(Tag)
admin.site.register(DetailedPost)