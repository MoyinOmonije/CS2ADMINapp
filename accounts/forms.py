from dataclasses import fields
import imp
from pyexpat import model
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from .models import *
from .models import UploadAssignmentMarks
from .models import UploadStudentMarks
from .models import AllocateTutors
from .models import MedicalQueries, CompassionateRequest, QueryTable

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )

class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    email = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'is_convenor', 'is_tutor','is_student')

class UploadAssignmentMarks(forms.ModelForm):
    class Meta:  
        model = UploadAssignmentMarks
        fields = "__all__"

class  UploadStudentMarks(forms.ModelForm):
    class Meta:  
        model = UploadStudentMarks
        fields = "__all__"


class  AllocateTutors(forms.ModelForm):
    class Meta:  
        model = AllocateTutors
        fields = "__all__"

class uploadmedicalQueries(forms.ModelForm):
    class Meta:
        model = MedicalQueries
        fields = "__all__"

class uploadCompassionateRequestsForm(forms.ModelForm):
   # studentNumber = forms.CharField(
      #  widget=forms.TextInput(
        #    attrs={
          #      "class": "form-control"
          #  }
      #  )
#    )
  #  proofOfReason = forms.FileField()
   #extensionDays = forms.IntegerField(max_value=200)
   # requestDetails = forms.CharField(
   #     widget=forms.Textarea(
   #         attrs={
   #             "class": "form-control"
   #         }
   #     )
   # )

    class Meta:
        model = CompassionateRequest
        fields = '__all__'

class queryForm(forms.ModelForm):
    QUERYTYPE_CHOICES = (
        ('content','CONTENT'),
        ('assessment marking', 'ASSESSMENT MARKING'),
        ('other','OTHER'),
    )

    STATUS_RESPONSE_CHOICES = (
        ('responded','RESPONDED'),
        ('not responded', 'NOT RESPONDED'),
    )

    ASSIGN_CHOICES = (
        ('convenor','CONVENOR'),
        ('tutor','TUTOR'),
    )

    studentNumber = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    queryDetails = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control"
            }
        )
    )

    queryChoice = forms.ChoiceField(choices=QUERYTYPE_CHOICES)

    assignDest = forms.ChoiceField(choices=ASSIGN_CHOICES)

    class Meta:
        model = QueryTable
        fields = ('studentNumber','queryChoice','queryDetails','assignDest')

class queryFormConv(forms.ModelForm):
    QUERYTYPE_CHOICES = (
        ('content','CONTENT'),
        ('assessment marking', 'ASSESSMENT MARKING'),
        ('other','OTHER'),
    )

    STATUS_RESPONSE_CHOICES = (
        ('responded','RESPONDED'),
        ('not responded', 'NOT RESPONDED'),
    )

    ASSIGN_CHOICES = (
        ('convenor','CONVENOR'),
        ('tutor','TUTOR'),
    )

    studentNumber = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )

    status = forms.ChoiceField(choices=STATUS_RESPONSE_CHOICES, required=False)

    messageResponse = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control"
            }
        )
    )
    class Meta:
        model = QueryTableResponse
        fields = ('studentNumber','status','messageResponse')

class medicalFormConv(forms.ModelForm):
    QUERYTYPE_CHOICES = (
        ('content','CONTENT'),
        ('assessment marking', 'ASSESSMENT MARKING'),
        ('other','OTHER'),
    )

    STATUS_RESPONSE_CHOICES = (
        ('approved','approved'),
        ('not approved', 'NOT APPROVED'),
    )

    ASSIGN_CHOICES = (
        ('convenor','CONVENOR'),
        ('tutor','TUTOR'),
    )

    studentNumber = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )

    status = forms.ChoiceField(choices=STATUS_RESPONSE_CHOICES, required=False)

    messageResponse = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control"
            }
        )
    )
    class Meta:
        model = MedicalResponse
        fields = ('studentNumber','status','messageResponse')

class compassionateFormConv(forms.ModelForm):
    QUERYTYPE_CHOICES = (
        ('content','CONTENT'),
        ('assessment marking', 'ASSESSMENT MARKING'),
        ('other','OTHER'),
    )

    STATUS_RESPONSE_CHOICES = (
        ('approved','approved'),
        ('not approved', 'NOT APPROVED'),
    )

    ASSIGN_CHOICES = (
        ('convenor','CONVENOR'),
        ('tutor','TUTOR'),
    )

    studentNumber = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )

    status = forms.ChoiceField(choices=STATUS_RESPONSE_CHOICES, required=False)

    messageResponse = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control"
            }
        )
    )
    class Meta:
        model = CompassionateResponse
        fields = ('studentNumber','status','messageResponse')

