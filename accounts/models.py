import imp
from pickle import NONE
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    is_convenor= models.BooleanField('Is convenor', default=False)
    is_tutor = models.BooleanField('Is tutor', default=False)
    is_student = models.BooleanField('Is student', default=False)


class MarksTable(models.Model):
    student = models.CharField(max_length=7)
    A1 = models.FloatField(null = True, blank = True)
    A2 = models.FloatField(null = True, blank = True)
    A3 = models.FloatField(null = True, blank = True)
    A4 = models.FloatField(null = True, blank = True)
    A5 = models.FloatField(null = True, blank = True)
    A6 = models.FloatField(null = True, blank = True)
    T1 = models.FloatField(null = True, blank = True)
    T2 = models.FloatField(null = True, blank = True)
    final1016 = models.FloatField(null = True, blank = True)
    A_avg1016 = models.FloatField(null = True, blank = True)
    Test_avg1016 = models.FloatField(null = True, blank = True)

    class Meta:
        db_table = 'MarksTable'


class AllocationTable(models.Model):
    studentNum = models.CharField(max_length=7)
    A1_marker = models.CharField(max_length=7)
    A2_marker = models.CharField(max_length=7)
    A3_marker = models.CharField(max_length=7)
    A4_marker = models.CharField(max_length=7)
    A5_marker = models.CharField(max_length=7)
    A6_marker = models.CharField(max_length=7)

    class Meta:
        db_table = 'Allocation Table'


class AssessmentTable(models.Model):
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    dueDate = models.CharField(max_length=20)

    class Meta:
        db_table = 'Assessment Table'

class ExtensionRequestTable(models.Model):
    studentNum = models.CharField(max_length=8)
    extensionReason = models.CharField(null = True, blank = True, max_length=20)
    numDays = models.IntegerField()
    status = models.CharField(null = True, blank = True, max_length=20)
    assessment = models.CharField(null = True, blank = True, max_length=7)
    reasoning = models.CharField(null = True, blank = True, max_length=200)
    file = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=100)
    convenorMessage = models.CharField(null = True, blank = True, max_length=200)

    class Meta:
        db_table = 'Extension Request Table'

class QueryTable(models.Model):
    QUERYTYPE_CHOICES = (
        ('content','CONTENT'),
        ('assessment marking', 'ASSESSMENT MARKING'),
        ('other','OTHER'),
    )

    ASSIGN_CHOICES = (
        ('convenor','CONVENOR'),
        ('tutor','TUTOR'),
    )
    studentNum = models.CharField(max_length=8)
    queryType = models.CharField(choices=QUERYTYPE_CHOICES, default='content', max_length=20)
    queryDetails = models.CharField(null = True, blank = True, max_length=200)
    assigned_to = models.CharField(choices=ASSIGN_CHOICES, default='convenor', max_length=10)

    class Meta:
        db_table = 'Query Table'

class QueryTableResponse(models.Model):
    STATUS_RESPONSE_CHOICES = (
        ('responded','RESPONDED'),
        ('not responded', 'NOT RESPONDED'),
    )
    studentNumber = models.CharField(null = False, blank = False, max_length=10, default=1)
    status = models.CharField(choices=STATUS_RESPONSE_CHOICES, default='not responded', max_length=20)
    responseMessage = models.CharField(null = True, blank = True, max_length=200)

    class Meta:
        db_table = 'Query Table Response'

class MedicalResponse(models.Model):
    STATUS_RESPONSE_CHOICES = (
        ('approved','approved'),
        ('not approved', 'NOT APPROVED'),
    )
    studentNumber = models.CharField(null = False, blank = False, max_length=10, default=1)
    status = models.CharField(choices=STATUS_RESPONSE_CHOICES, default='not responded', max_length=20)
    responseMessage = models.CharField(null = True, blank = True, max_length=200)

    class Meta:
        db_table = 'Medical Table Response'

class CompassionateResponse(models.Model):
    STATUS_RESPONSE_CHOICES = (
        ('approved','approved'),
        ('not approved', 'NOT APPROVED'),
    )
    studentNumber = models.CharField(null = False, blank = False, max_length=10, default=1)
    status = models.CharField(choices=STATUS_RESPONSE_CHOICES, default='not responded', max_length=20)
    responseMessage = models.CharField(null = True, blank = True, max_length=200)

    class Meta:
        db_table = 'Compassionate Table Response'


class UploadAssignmentMarks(models.Model):
    file = models.FileField(upload_to='media')

    class Meta:
        db_table = 'Upload Assignment Marks'


class UploadStudentMarks(models.Model):
    file = models.FileField(upload_to='media', null = True, blank = True)

    class Meta:
        db_table = 'Upload Student Marks'


class AllocateTutors(models.Model):
    file = models.FileField(upload_to='media')

    class Meta:
        db_table = 'Allocate Tutors'


class classReps(models.Model):
    
    stuNumber = models.CharField(null = False, blank = False, max_length=10)
    name = models.CharField(null = False, blank = False, max_length=50)
    email = models.CharField(null = False, blank = False, max_length=50)

    class Meta:
        db_table = 'class Representatives'

class MedicalQueries(models.Model):
    studentNumber = models.CharField(null = False, blank = False, max_length=10, default=1)
    medicalCertificate = models.FileField(upload_to='media',blank=False)
    extensionDays = models.IntegerField()
    queryDetails = models.CharField(null = True, blank = True, max_length=1000)

    class Meta:
        db_table = 'Medical Queries'

class CompassionateRequest(models.Model):
    studentNumber = models.CharField(null = False, blank = False, max_length=10, default=1)
    proofOfReason = models.FileField(upload_to='media',blank=False)
    extensionDays = models.IntegerField()
    requestDetails = models.CharField(null = True, blank = True, max_length=1000)

    class Meta:
        db_table = 'Compassionate Request'
