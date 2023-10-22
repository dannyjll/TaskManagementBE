from django.contrib import admin
from HoneyDo.models import (List, Group, Task, Profile, Reminder, Category)


admin.site.register(List)
#.site.register(MembershipTable)
admin.site.register(Group)
admin.site.register(Task)
admin.site.register(Profile)
admin.site.register(Reminder)
admin.site.register(Category)
#admin.site.register(SiteUser)
#admin.site.register(Category)
#admin.site.register(Comment)