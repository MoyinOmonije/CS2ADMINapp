from xml.etree.ElementInclude import include
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
# from django_downloadview import ObjectDownloadView
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login_view'),
    path('register/', views.register, name='register'),
    path('home/', views.home, name='home'),
    path('convenorpage/', views.convenor_view, name='convenorpage'),
    path('studentpage/', views.student_view, name='studentpage'),
    path('tutorpage/', views.tutor_view, name='tutorpage'),
    path('logout', views.logout_request, name='logout'),
    path("convenor/", views.convpage, name="convenor"),
    path("student/", views.stupage, name="student"),
    path("tutor/", views.tutpage, name="tutor"),
    path("learn/", views.learn, name="learn"),
    path("viewmark/", views.viewMarkingAllocation, name="viewmark"),
    path("uploadstudentmarks/", views.upload_stu_marks, name="uploadstudentmarks"),
    path("allocateTutors/", views.allocate_Tutors, name="allocateTutors"),
    path("uploadAssignment/", views.upload_A_marks, name="uploadAssignment"),
    path("requestMedical/", views.request_medical, name="requestMedical"),
    path("requestCompassionate/", views.request_compassionate, name="requestCompassionate"),
    path("sendQuery/", views.send_query, name="sendQuery"),
    path("convQueries/", views.conv_generalQueries, name="convQueries"),
    path("tutQueries/", views.tut_generalQueries, name="tutQueries"),
    path("generalHelp/", views.general_help, name="generalHelp"),
    path("uploadtutors/", views.upload_tut_page, name="uploadtutors"),
    path("uploadclassReps/", views.uploadClassReps, name="uploadclassReps"),
    path("studentMedicalsConvView/", views.conv_medical_Queries, name="studentMedicalsConvView"),
    path("convCompassionateReqs/",views.conv_compassionateRequests, name="convCompassionateReqs"),
    path("responseConvenor/", views.respond_query, name="responseConvenor"),
    path("responseTutor/", views.respond_queryTut, name="responseTutor"),
    path("medicalResponseConvenor", views.respond_medical, name="medicalResponseConvenor"),
    path("compassionateResponseConvenor", views.respond_compassionate, name="compassionateResponseConvenor"),
    path("studentSeeResponse/", views.student_responseQuery, name="studentSeeResponse"),
    path("studentSeeMedicalResponse/", views.student_medicalResponse, name="studentSeeMedicalResponse"),
    path("studentSeeCompassionateResponse/", views.student_compassionateResponse, name="studentSeeCompassionateResponse"),
    re_path(r'^download/(?P<path>.*)$',serve,{'document_root':settings.MEDIA_ROOT}),
    path("viewAnalysis/", views.convenor_analysis, name="viewAnalysis"),
    path("convenorViews/", views.convenorViews_page, name="convenorViews"),
    path("allocationComplete/", views.tutor_alloc, name="allocationComplete"),
    path("tutorStats/", views.tutor_progress, name="tutorStats"),
]
