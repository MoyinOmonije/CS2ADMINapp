import imp
from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(MarksTable)
admin.site.register(AllocationTable)
admin.site.register(AssessmentTable)
admin.site.register(ExtensionRequestTable)
admin.site.register(QueryTable)
admin.site.register(UploadAssignmentMarks)
admin.site.register(UploadStudentMarks)
admin.site.register(AllocateTutors)
admin.site.register(classReps)
admin.site.register(MedicalQueries)
admin.site.register(CompassionateRequest)
admin.site.register(QueryTableResponse)
admin.site.register(MedicalResponse)
admin.site.register(CompassionateResponse)
