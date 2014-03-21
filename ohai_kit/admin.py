from django.contrib import admin
from django.contrib.admin import SimpleListFilter

from ohai_kit.models import Project, ProjectSet, WorkStep, \
    StepCheck, StepPicture, StepAttachment, JobInstance, WorkReceipt


#### Machinery for Project Admin View

class WorkStepInline(admin.TabularInline):
    model = WorkStep
    extra = 0
    ordering = ["sequence_number"]
    fields = ["sequence_number", "name"]

class ProjectAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {
                "fields" : ["name", "slug", "abstract"],
                }),
        ("Optional", {
                "fields" : ["photo"],
                }),
        ]
    list_display = ["name", "abstract"]
    list_filter = ["name"]
    search_fields = ["name"]
    inlines = [WorkStepInline]

class ProjectSetAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {
                "fields" : ["name", "abstract", "projects", "private", "legacy"],
                }),
        ("Optional", {
                "fields" : ["photo"],
                }),
    ]
    list_display = ["name", "abstract"]
    list_filter = ["name"]
    search_fields = ["name"]




#### Machinery for WorkStep Admin View

class StepCheckInline(admin.TabularInline):
    model = StepCheck
    extra = 0
    ordering = ["check_order"]
    fields = ["check_order", "message"]

class StepPictureInline(admin.StackedInline):
    model = StepPicture
    extra = 0
    ordering = ["image_order"]
    fields = ["image_order", "photo", "caption"]

class StepAttachmentInline(admin.StackedInline):
    model = StepAttachment
    extra = 0
    ordering = ["order"]
    fields = ["order", "attachment", "thumbnail", "caption"]

class WorkStepAdmin(admin.ModelAdmin):
    inlines = [StepPictureInline, StepAttachmentInline, StepCheckInline]
    list_display = ["name", "description", "project"]
    list_filter = ["project__name"]
    ordering = ["project", "sequence_number"]
    search_fields=["project", "name", "description"]




#### Register Admin Pages

admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectSet, ProjectSetAdmin)
admin.site.register(WorkStep, WorkStepAdmin)
admin.site.register(JobInstance)
admin.site.register(WorkReceipt)
