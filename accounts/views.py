from multiprocessing import context
import os
from urllib import response
from django.conf import settings
from django.http import HttpResponse, Http404
from ast import main
from distutils import extension
from fileinput import filename
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import *
from django.contrib import messages
from .spreadsheet_classes import *
from .user_classes import *
from .models import *
import openpyxl
import pandas as pd  # allows us to access the spreadsheet
from tkinter import Tk  # allows the user to see file upload dialogue
from tkinter.filedialog import askopenfilename
import time
from datetime import date
import sqlite3 as sl
from http.client import HTTPResponse
from django.shortcuts import render, HttpResponse
from .models import MedicalQueries, UploadAssignmentMarks, CompassionateRequest
from django.shortcuts import render
from django.http import HttpResponse
from .functions import handle_uploaded_file
from .models import classReps
from django.core.files.storage import FileSystemStorage
from .send_summary_email import mail
import threading
# Create your views here.


def index(request):
    return render(request, 'index.html')


# this method is called when the user registers
def register(request):
    msg = None
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            msg = 'user created'
            return redirect('login_view')
        else:
            msg = 'form is not valid'
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form, 'msg':msg})


# this method is called when the user logs in
def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_convenor:
                login(request,user)
                return redirect('convenorpage')
            elif user is not None and user.is_tutor:
                login(request,user)
                return redirect('tutorpage')
            elif user is not None and user.is_student:
                login(request,user)
                return redirect('studentpage')
            else:
                msg = 'invalid credentials'
        else:
            msg ='error validating form'
    return render(request, "login.html", {'form':form, 'msg':msg})


# this method is called when a user logs out
def logout_request(request):
    logout(request)
    messages.info(request, 'You have sucessfully logged out')
    return redirect('index')


# this method returns you to the home page
def home(request):
    return render(request, 'homepage.html')


# this method takes the student to the student view page
def student_view(request):
    return render(request, 'student_view.html')


# this method takes the tutor to the tuor view page
def tutor_view(request):
    return render(request, 'tutor_view.html')


# this method takes the convenor to the convenor view page
def convenor_view(request):
    return render(request, 'convenor_view.html')


# this method takes the convenor to the convenor page
def convpage(request):
    return render(request, "convenor.html")


# this method takes the tutor to the tutor page
def tutpage(request):
    return render(request, "tutor.html")


# this method takes the student to the student page
def stupage(request):
    return render(request, "student.html")


# this method takes the convenor to the convenorViews page
def convenorViews_page(request):
    return render(request, 'convenorViews.html')


# this method takes the user to the learn page
def learn(request):
    return render(request, "learn.html")


# this method allows the uploading of student mark spreadsheet to the database
def upload_stu_marks(request):
    if request.method == 'POST':
        upload1 = request.FILES['markSpreadsheet']
        object = UploadStudentMarks.objects.create(file=upload1)
        object.save()
    context = UploadStudentMarks.objects.all()
    return render(request, 'upload_stu_marks.html',{'context':context})


# this method takes the convenor to the upload tut page
def upload_tut_page(request):
    return render(request, "upload_tut.html")


# this method allows the tutor to upload assignment marks to the database
def upload_A_marks(request):
    if request.method == 'POST':
        a_file = UploadAssignmentMarks(request.POST, request.FILES)
        if a_file.is_valid():
            handle_uploaded_file(request.FILES['file'])
            model_instance = a_file.save(commit=False)
            model_instance.save()
            return HttpResponse("File uploaded successfuly")
    else:
        a_file = UploadAssignmentMarks()
        return render(request, "upload_A_marks.html", {'form': a_file})


# this method is called when the student saves/submits a medical request
def request_medical(request):
    if request.method == 'POST':
        studentnumber = request.POST['studentNumber']
        medicalCertificate = request.FILES['medicalCertificate']
        extensionDays = request.POST['extensionDays']
        requestDetails = request.POST['requestDetails']

        new_MedResStatus = MedicalResponse(studentNumber=studentnumber, status='not responded', responseMessage='')
        new_MedResStatus.save()

        new_medicalCertificate = MedicalQueries(studentNumber=studentnumber, medicalCertificate=medicalCertificate, extensionDays=extensionDays, queryDetails=requestDetails)
        new_medicalCertificate.save()

    return render(request, "medical.html")


# this method is called when the student saves/submits a compassionate request
def request_compassionate(request):
    if request.method == 'POST':
        studentnumber = request.POST['studentNumber']
        proofOfReason = request.FILES['proofOfReason']
        extensionDays = request.POST['extensionDays']
        requestDetails = request.POST['requestDetails']

        new_CompResStatus = CompassionateResponse(studentNumber=studentnumber, status ='not responded', responseMessage ='')
        new_CompResStatus.save()

        new_compassionateRequest = CompassionateRequest(studentNumber=studentnumber, proofOfReason=proofOfReason, extensionDays=extensionDays, requestDetails=requestDetails)
        new_compassionateRequest.save()
    return render(request, "compassionate.html")


# this method is called when the student saves/submits a query
def send_query(request):
    form = queryForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            studentNumber = request.POST.get('studentNumber')
            query = request.POST.get('queryDetails')
            type = request.POST.get('queryChoice')
            assignDest = request.POST.get('assignDest')

            new_QueryStatus = QueryTableResponse(studentNumber=studentNumber, status ='not responded', responseMessage ='')
            new_QueryStatus.save()

            new_QueryItem = QueryTable(studentNum=studentNumber,queryDetails=query,queryType=type,assigned_to=assignDest)
            new_QueryItem.save()

    return render(request, "sendQuery.html", {'form': form})


# this method is called when the convenor responds to a query
def respond_query(request):
    form = queryFormConv(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            studentNumber = request.POST.get('studentNumber')
            status = request.POST.get('status')
            messageResponse = request.POST.get('messageResponse')
            new_QueryResponse = QueryTableResponse.objects.get(studentNumber=studentNumber,status='not responded')
            new_QueryResponse.status = 'responded'
            new_QueryResponse.responseMessage = messageResponse
            new_QueryResponse.save()
    return render(request, "responseConvenor.html", {'form': form})


# this method is called when the convenor responds to a query assigned to a tutor
def respond_queryTut(request):
    form = queryFormConv(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            studentNumber = request.POST.get('studentNumber')
            status = request.POST.get('status')
            messageResponse = request.POST.get('messageResponse')
            new_QueryResponse = QueryTableResponse.objects.get(studentNumber=studentNumber,status='not responded')
            new_QueryResponse.status = 'responded'
            new_QueryResponse.responseMessage = messageResponse
            new_QueryResponse.save()
    return render(request, "responseTutor.html", {'form': form})


# this method is called when the convenor responds to a medical request
def respond_medical(request):
    form = medicalFormConv(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            studentNumber = request.POST.get('studentNumber')
            status = request.POST.get('status')
            messageResponse = request.POST.get('messageResponse')
            new_QueryResponse = MedicalResponse.objects.get(studentNumber=studentNumber,status='not responded')
            new_QueryResponse.status = 'responded'
            new_QueryResponse.responseMessage = messageResponse
            new_QueryResponse.save()
    return render(request, "medicalResponseConv.html", {'form': form})


# this method is called when the convenor responds to a compassionate request
def respond_compassionate(request):
    form = compassionateFormConv(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            studentNumber = request.POST.get('studentNumber')
            status = request.POST.get('status')
            messageResponse = request.POST.get('messageResponse')
            new_QueryResponse = CompassionateResponse.objects.get(studentNumber=studentNumber,status='not responded')
            new_QueryResponse.status = 'responded'
            new_QueryResponse.responseMessage = messageResponse
            new_QueryResponse.save()
    return render(request, "compassionateResponseConv.html", {'form': form})


# this method takes the user to the general help page
def general_help(request):
    return render(request, "generalHelp.html")


# this method is called when the convenor uploads class reps
def uploadClassReps(request):
    if request.method == 'POST':
        stuNumber = request.POST['stuNumber']
        name = request.POST['name']
        email = request.POST['email']

        new_classRep = classReps(stuNumber=stuNumber, name=name, email=email)
        new_classRep.save()

    return render(request, "classReps.html")


# this function is called when the tutor wants to view the marking allocation
def viewMarkingAllocation(request):
    df = pd.DataFrame(columns=['Student', 'A1_marker', 'A2_marker', 'A3_marker', 'A4_marker', 'A5_marker', 'A6_marker']) # create a pandas object for storing all students and their markers
    all_students = AllocationTable.objects.all()  # return an object storing all students
    i = 0
    for s in all_students:
        df.loc[i] = [s.studentNum, s.A1_marker, s.A2_marker, s.A3_marker, s.A4_marker, s.A5_marker, s.A6_marker]
        i += 1

    excel_object = df.to_html()
    return HttpResponse(excel_object)


# this method is called when the convenor uploads a tutor list
def allocate_Tutors(request):
    if request.method == 'POST':
        upload1 = request.FILES['tutorSpreadsheet']
        object = AllocateTutors.objects.create(file=upload1)
        object.save()
    context = AllocateTutors.objects.all()
    return render(request, 'upload_tut.html',{'context':context})


def conv_medical_Queries(request):
    data_List = MedicalQueries.objects.all()
    context = {'data_List': data_List}
    return render (request, 'medicalCertificatesStudent.html', context)


def conv_compassionateRequests(request):
    data_List = CompassionateRequest.objects.all()
    context = {'data_List': data_List}
    return render (request, 'compassionateRequestsConvenor.html', context)


def conv_generalQueries(request):
    data_List = QueryTable.objects.all()
    context = {'data_List': data_List}
    return render (request, 'queries_convenor.html', context)


def tut_generalQueries(request):
    data_List = QueryTable.objects.all()
    context = {'data_List': data_List}
    return render (request, 'queries_tutor.html', context)


def student_responseQuery(request):
    data_List = QueryTableResponse.objects.all()
    context = {'data_List': data_List}
    return render (request, 'studentSeeResponse.html', context)


def student_medicalResponse(request):
    data_List = MedicalResponse.objects.all()
    context = {'data_List': data_List}
    return render (request, 'studentSeeMedicalResponse.html', context)


def student_compassionateResponse(request):
    data_List = CompassionateResponse.objects.all()
    context = {'data_List': data_List}
    return render (request, 'studentSeeCompassionateResponse.html', context)


def upload(request):
    #get download path
    download_path = os.path.join(settings.MEDIA_ROOT, os.path)
    if os.path.exists(download_path):
        with open(download_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type='application/medicalCertificate')
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(download_path)
            return response
    raise Http404


# do calculations
def do_calculation(panda_obj):  # this object contains the spreadsheet
    marks = Marksheet(panda_obj)
    return marks.process()


def convenor_analysis(self):  # this method conducts the analysis of student marks
    num_of_spreadsheets = UploadStudentMarks.objects.count()  # checks the number of spreadsheets currently stored
    markObj = UploadStudentMarks.objects.get(id=num_of_spreadsheets)  # get the latest spreadsheet
    marksheet = pd.read_excel(markObj.file)  # stores the marksheet in a pandas object
    output = do_calculation(marksheet)  # a pandas dataframe is returned

    output = output.to_html()
    return HttpResponse(output)


def tutor_alloc(request):  # this method randomly assigns tutors to students for marking their assignments
    num_of_spreadsheets = AllocateTutors.objects.count()  # checks the number of spreadsheets currently stored
    tutor_list_obj = AllocateTutors.objects.get(id=num_of_spreadsheets)  # get the latest spreadsheet
    tutor_list_obj = pd.read_excel(tutor_list_obj.file)  # convert to a pandas dataframe

    num_students = MarksTable.objects.count()  # get the number of students currently in the MarksTable table
    df = pd.DataFrame(columns=['Student']) # create a pandas object of all students

    # loop through all students and store them in a pandas dataframe
    for x in range(num_students):
        df.loc[x] = [(MarksTable.objects.get(id=x+1)).student]

    stu_list_obj = df
    conv = Convenor('BMNSON001')
    conv.allocate_tutors(tutor_list_obj, stu_list_obj)  # call the allocate_tutors function in the Convenor class
    return HttpResponse("Tutors have been allocated")


def tutor_progress(request):  # checks how far tutors are with their marking
    num_of_spreadsheets = AllocateTutors.objects.count()
    tutor_list_obj = AllocateTutors.objects.get(id=num_of_spreadsheets)  # get the latest spreadsheet
    tutor_list_obj = pd.read_excel(tutor_list_obj.file)
    num_tutors = len(tutor_list_obj)
    tutor_progress_df = pd.DataFrame(columns=['Tutor Progress Summary For Assignment 1 to 6'])
    all_tutors_progress_df = pd.DataFrame(columns=['Tutor Progress Summary For Assignment 1 to 6'])

    for a in range(6):  # number of assignments
        for t in range(num_tutors):
            num_to_mark = 0  # number of assignments to mark for this tutor
            num_unmarked = 0  # number of assignments that are unmarked for this tutor
            s_names = ''  # students allocated to this tutor
            tutor_summary = ''
            all_students = MarksTable.objects.all()
            for s in all_students:
                tutor_id = tutor_list_obj.iloc[t]['Student']  # get the tutor's student number
                stu_num = s.student  # holds the current student's stu_id
                if (a == 0):
                    if (AllocationTable.objects.filter(studentNum=stu_num, A1_marker=tutor_id).exists()):  # checks if this tutor is assigned to mark this student's assignment
                        num_to_mark += 1
                        s_names = s_names + ' ' + stu_num
                        # check if their assignment is marked or no
                        if (MarksTable.objects.filter(A1__isnull=True, student=stu_num)):  # checks if the student's assignment has been marked or no
                            num_unmarked += 1

                elif (a == 1):
                    if (AllocationTable.objects.filter(studentNum=stu_num, A2_marker=tutor_id).exists()):
                        num_to_mark += 1
                        s_names = s_names + ' ' + stu_num
                        # check if their assignment is marked or no
                        if (MarksTable.objects.filter(A2__isnull=True, student=stu_num)):
                            num_unmarked += 1

                elif (a == 2):
                    if (AllocationTable.objects.filter(studentNum=stu_num, A3_marker=tutor_id).exists()):
                        num_to_mark += 1
                        s_names = s_names + ' ' + stu_num
                        # check if their assignment is marked or no
                        if (MarksTable.objects.filter(A3__isnull=True, student=stu_num)):
                            num_unmarked += 1

                elif (a == 3):
                    if (AllocationTable.objects.filter(studentNum=stu_num, A4_marker=tutor_id).exists()):
                        num_to_mark += 1
                        s_names = s_names + ' ' + stu_num
                        # check if their assignment is marked or no
                        if (MarksTable.objects.filter(A4__isnull=True, student=stu_num)):
                            num_unmarked += 1

                elif (a == 4):
                    if (AllocationTable.objects.filter(studentNum=stu_num, A5_marker=tutor_id).exists()):
                        num_to_mark += 1
                        s_names = s_names + ' ' + stu_num
                        # check if their assignment is marked or no
                        if (MarksTable.objects.filter(A5__isnull=True, student=stu_num)):
                            num_unmarked += 1

                elif (a == 5):
                    if (AllocationTable.objects.filter(studentNum=stu_num, A6_marker=tutor_id).exists()):
                        num_to_mark += 1
                        s_names = s_names + ' ' + stu_num
                        # check if their assignment is marked or no
                        if (MarksTable.objects.filter(A6__isnull=True, student=stu_num)):
                            num_unmarked += 1

            tutor_summary = str(tutor_id) + ' was assigned ' + str(num_to_mark) + ' assignment ' + str(a+1) + ' scripts'
            # print(tutor_id, 'was assigned', num_to_mark, 'assignment', a+1, 'scripts')
            tutor_summary = tutor_summary + '. The students are ' + s_names
            # print('The students are', s_names)
            tutor_summary = tutor_summary + '. They still need to mark ' + str(num_unmarked) + ' assignment ' + str(a+1) + ' scripts'
            # print('They still  need to mark', num_unmarked, 'assignment', a+1, 'scripts')
            tutor_progress_df.loc[t] = [tutor_summary]
            all_tutors_progress_df = pd.concat([all_tutors_progress_df,tutor_progress_df]).drop_duplicates().reset_index(drop=True)

    output = all_tutors_progress_df.to_html()
    return HttpResponse(output)


def check_records():  # this method checks if there are any pending messages for the convenor
    num_queries = 0  # the number of queries that the convenor has not responded to yet
    num_med_requests = 0  #
    num_comp_requests = 0  #
    if (QueryTableResponse.objects.filter(status="not responded").exists()):
        num_queries = QueryTableResponse.objects.filter(status="not responded").count()

    if (MedicalResponse.objects.filter(status="not responded").exists()):
        num_med_requests = MedicalResponse.objects.filter(status="not responded").count()

    if (CompassionateResponse.objects.filter(status="not responded").exists()):
        num_comp_requests = CompassionateResponse.objects.filter(status="not responded").count()

    msg = 'Good morning Prof Berman.\nYou currently have ' + str(num_queries) + ' queries you have not responded to.\nYou currently have ' + str(num_med_requests) + ' extension requests (medical reasons) you have not responded to.\n You currently have ' + str(num_comp_requests) + ' extension requests (compassionate reasons) you have not responded to.'
    return msg


def check_date():  # checks if the date is Monday at 8am
    day_of_the_week = date.today().weekday()  # returns an integer indicating the day of the week today. Monday is 0, Sunday is 6
    if (day_of_the_week == 0):  # this means it is Monday
        time_right_now = time.strftime("%H:%M")  # returns a string of the current time
        if (time_right_now == '08:00'):  # checks if the current time is not 8am
            message_to_send = check_records()
            mail(message_to_send)  # call the mail function if it's a Monday at 8am


th = threading.Thread(target=check_date)  # creates a thread that deals with emails
th.start()  # start the thread
