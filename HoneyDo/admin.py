from django.contrib import admin
from HoneyDo.models import Category, Comment, List, MembershipTable, Group, Task, SiteUser

admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(List)
admin.site.register(MembershipTable)
admin.site.register(Group)
admin.site.register(Task)
admin.site.register(SiteUser)
