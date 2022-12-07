# this module contains all classes related to and including the User class
from accounts.spreadsheet_classes import *
import xlrd
import pandas as pd
import random
import math
import sqlite3 as sl
from .models import *


class User:
    def __init__(self, username):    # Constructor
        self.username = username

    def log_out(self):
        pass
        # end the current user's session


class Convenor(User):
    status = ''   # default is an empty string. Is meant to show for example number of unseen notifications and other relevant information

    def __init__(self, username):
        super().__init__(username)


    def allocate_tutors(self, tutor_list, student_list):  # allows the convenor to allocate tutors to students for marking purposes
        original_stu_list = student_list

        for a in range(6):  # loop for each assignment
            df = pd.DataFrame(columns=['Tutor', 'Students'])  # object will store allocation
            student_list = original_stu_list
            num_tutors = len(tutor_list.index)
            num_students = len(student_list.index)
            students_per_tutor = math.floor(num_students/num_tutors)
            remaining_students = num_students % num_tutors  # some tutors will get at most more than one student than the rest if the number of students is not a factor of number or tutors
            unallocated_students = num_students
            first_student = True
            for x in range(num_tutors):  # loop for each tutor
                tutor_id = tutor_list.iloc[x]['Student']  # get the tutor's student number
                for k in range(students_per_tutor):
                    selected_student = random.randint(0, unallocated_students-1)  # returns random number within range of rows
                    stu_id = student_list.iloc[selected_student]['Student']  # get the student number in that row
                    if (first_student):  # check if there is already a student(s) assigned to this tutor
                        df.loc[x] = [tutor_id, str(stu_id)]  # add new row with tutor and student
                        first_student = False
                    else:  # there is at least one student assigned to this tutor already
                        current_alloc = df.iloc[x]['Students']
                        new_alloc = str(current_alloc) + '\n' + str(stu_id)  # append this student to current allocation
                        df.loc[x] = [tutor_id, new_alloc]

                    student_list = student_list.drop(selected_student).reset_index(drop=True)  # remove this student from the data frame. reset_index makes sure the index is reset so there are no gaps in the numbering. This is important as the random number generated is based on the row/index numbers.
                    unallocated_students -= 1

                if (remaining_students > 0):  # assigns one more student to this tutor
                    selected_student = random.randint(0, unallocated_students-1)
                    stu_id = student_list.iloc[selected_student]['Student']
                    current_alloc = df.iloc[x]['Students']
                    new_alloc = str(current_alloc) + '\n' + str(stu_id)  # append this student to current allocation
                    df.loc[x] = [tutor_id, new_alloc]
                    student_list = student_list.drop(selected_student).reset_index(drop=True)  # remove this student from the data frame
                    unallocated_students -= 1
                    remaining_students -= 1

                first_student = True
                # GET STUDENTS HERE WITH A FOR LOOP
                print(x)
                students_for_this_tutor = str(df.iat[x, 1])
                stu_array = students_for_this_tutor.split('\n')
                if (a == 0):  # allocation for assignment 1
                    for s in range(len(stu_array)):
                        # check if record already exists
                        if not (AllocationTable.objects.filter(studentNum=stu_array[s]).exists()):
                            aTable = AllocationTable(studentNum=stu_array[s], A1_marker=tutor_id)
                        else:
                            aTable = AllocationTable.objects.get(studentNum=stu_array[s])
                            aTable.A1_marker = tutor_id
                        aTable.save()

                if (a == 1):  # allocation for assignment 2
                    for s in range(len(stu_array)):
                        # check if record already exists
                        if not (AllocationTable.objects.filter(studentNum=stu_array[s]).exists()):
                            aTable = AllocationTable(studentNum=stu_array[s], A2_marker=tutor_id)
                        else:
                            aTable = AllocationTable.objects.get(studentNum=stu_array[s])
                            aTable.A2_marker = tutor_id
                        aTable.save()

                if (a == 2):  # allocation for assignment 3
                    for s in range(len(stu_array)):
                        # check if record already exists
                        if not (AllocationTable.objects.filter(studentNum=stu_array[s]).exists()):
                            aTable = AllocationTable(studentNum=stu_array[s], A3_marker=tutor_id)
                        else:
                            aTable = AllocationTable.objects.get(studentNum=stu_array[s])
                            aTable.A3_marker = tutor_id
                        aTable.save()

                if (a == 3):  # allocation for assignment 4
                    for s in range(len(stu_array)):
                        # check if record already exists
                        if not (AllocationTable.objects.filter(studentNum=stu_array[s]).exists()):
                            aTable = AllocationTable(studentNum=stu_array[s], A4_marker=tutor_id)
                        else:
                            aTable = AllocationTable.objects.get(studentNum=stu_array[s])
                            aTable.A4_marker = tutor_id
                        aTable.save()

                if (a == 4):  # allocation for assignment 5
                    for s in range(len(stu_array)):
                        # check if record already exists
                        if not (AllocationTable.objects.filter(studentNum=stu_array[s]).exists()):
                            aTable = AllocationTable(studentNum=stu_array[s], A5_marker=tutor_id)
                        else:
                            aTable = AllocationTable.objects.get(studentNum=stu_array[s])
                            aTable.A5_marker = tutor_id
                        aTable.save()

                if (a == 5):  # allocation for assignment 6
                    for s in range(len(stu_array)):
                        # check if record already exists
                        if not (AllocationTable.objects.filter(studentNum=stu_array[s]).exists()):
                            aTable = AllocationTable(studentNum=stu_array[s], A6_marker=tutor_id)
                        else:
                            aTable = AllocationTable.objects.get(studentNum=stu_array[s])
                            aTable.A6_marker = tutor_id
                        aTable.save()
