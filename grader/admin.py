from django.contrib import admin

from .models import User, Lab, Submission

# Register your models here.


class LabAdmin(admin.ModelAdmin):
    pass


class UserAdmin(admin.ModelAdmin):
    pass


class SubmissionAdmin(admin.ModelAdmin):
    pass


admin.site.register(Lab, LabAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Submission, SubmissionAdmin)
