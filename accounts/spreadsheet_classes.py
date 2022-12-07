# this module contains all classes related to and including the Spreadsheet class
import xlrd
import pandas as pd
from datetime import date
import sqlite3 as sl


class Marksheet():
    def __init__(self, spreadsheet_object):
        self.spreadsheet_object = spreadsheet_object
        self.critical_df = None

    def process(self):  # checks the students who need help based on the cases below
        # case 1: Those who miss both A1 and A2, and do badly in test 1
        # case 2: students who did well in CSC1016S assignments and are now doing worse in the CS2 (15% difference) assignments
        num_rows = len(self.spreadsheet_object.index)  # returns the number of students
        a1_missed = False  # the student did not submit assignment 1
        a2_missed = False  # the student did not submit assignment 2
        test1_failed = False  # the student failed test 1
        case_1 = False
        critical_count = 0  # number of students who need help based on the two cases
        cs1_as_avg = 0  # the student's average for assignments in CS1
        cs2_as_avg = 0  # the student's average for assignments in CS2
        case_2 = False
        case_1_count = 0  # the number of students who meet the Case 1 criteria
        case_2_count = 0  # the number of students who meet the Case 2 criteria
        self.case_1_df = None  # this data frame holds all students who fall into Case 1
        self.case_2_df = None  # this data frame holds all students who fall into Case 2

        for k in range(num_rows):
            # Checking Case 1
                # Store the student's assignment marks
            student_a1_mark = self.spreadsheet_object.iloc[k]['A1']
            student_a2_mark = self.spreadsheet_object.iloc[k]['A2']
            student_a3_mark = self.spreadsheet_object.iloc[k]['A3']
            student_a4_mark = self.spreadsheet_object.iloc[k]['A4']
            student_a5_mark = self.spreadsheet_object.iloc[k]['A5']
            student_a6_mark = self.spreadsheet_object.iloc[k]['A6']
            student_t1_mark = self.spreadsheet_object.iloc[k]['T1']

            if (pd.isna(student_a1_mark)):  # just checks if the cell is empty
                a1_missed = True

            if (pd.isna(student_a2_mark)):  # just checks if the cell is empty
                a2_missed = True

            if (student_t1_mark <= 17.5):  # less than 50%
                test1_failed = True

            if (a1_missed and a2_missed and test1_failed):
                case_1_count += 1
                case_1 = True

            a1_missed = False
            a2_missed = False
            test1_failed = False

            # checking case 2
            cs1_as_avg = self.spreadsheet_object.iloc[k]['1016asgAv']

            if (pd.isna(student_a1_mark)):
                student_a1_mark = 0

            if (pd.isna(student_a2_mark)):
                student_a2_mark = 0

            if (pd.isna(student_a3_mark)):
                student_a3_mark = 0

            if (pd.isna(student_a4_mark)):
                student_a4_mark = 0

            if (pd.isna(student_a5_mark)):
                student_a5_mark = 0

            if (pd.isna(student_a6_mark)):
                student_a6_mark = 0

            cs2_as_avg = (student_a1_mark + student_a2_mark + student_a3_mark + student_a4_mark + student_a5_mark + student_a6_mark) / 6

            if (cs1_as_avg > cs2_as_avg):
                # check if the difference is >= 15%
                if (cs1_as_avg - cs2_as_avg >= 15):
                    # check if last year's assignment mark is less than or equal to 70%
                    if (cs1_as_avg <= 70):
                        case_2 = True
                        case_2_count += 1

            if (case_1 or case_2):
                critical_count += 1
                if (case_1):
                    if (case_1_count == 1):  # if it's the first student identified for case 1
                        self.case_1_df = self.create_data_frame(1)

                    self.append_spreadsheet(self.spreadsheet_object, self.case_1_df, k, case_1_count, 1)

                if (case_2):
                    if (case_2_count == 1):  # if it's the first student identified for case 2
                        self.case_2_df = self.create_data_frame(2)

                    self.append_spreadsheet(self.spreadsheet_object, self.case_2_df, k, case_2_count, 2, cs2_as_avg)

            cs1_as_avg = 0
            cs2_as_avg = 0
            case_1 = False
            case_2 = False

        today = date.today()
        new_sum = Marks_Summary(today, critical_count, case_1_count, case_2_count)
        new_sum.update_summary()

        # if both cases have students in them then they can be merged
        if ((self.case_1_df is not None) and (self.case_1_df is not None)):
            new_dataframe = pd.concat([self.case_1_df, self.case_2_df]).drop_duplicates()  # remove any duplicate students who meet both case 1 and case 2
            return new_dataframe
        elif(self.case_1_df is not None):
            return self.case_1_df
        else:
            return self.case_2_df

    def append_spreadsheet(self, old_data_frame, new_data_frame, old_index, new_index, case_num, cs2_avg = 0):  # add student details to object
        if (case_num == 1):
            column_1 = old_data_frame.iloc[old_index]['Student']
            column_2 = old_data_frame.iloc[old_index]['A1']
            column_3 = old_data_frame.iloc[old_index]['A2']
            column_4 = old_data_frame.iloc[old_index]['T1']

            new_data_frame.loc[new_index] = [column_1, column_2, column_3, column_4]

        elif (case_num == 2):
            column_1 = old_data_frame.iloc[old_index]['Student']
            column_2 = old_data_frame.iloc[old_index]['1016asgAv']
            column_3 = cs2_avg

            new_data_frame.loc[new_index] = [column_1, column_2, column_3]

    def create_data_frame(self, case_num):  # create a new data frame object with relevant columns for a case
        if (case_num == 1):
            df = pd.DataFrame(columns=['Student', 'A1', 'A2', 'T1'])
            return df
        elif (case_num == 2):
            df = pd.DataFrame(columns=['Student', '1016asgAv', 'CurrentAsgAv'])
            return df


class Summary():  # this class is used to create a Summary
    def __init__(self, date_created):
        self.date_created = date_created

    def update_summary(self, student_count):
        print('Student Analysis')
        print('*************************************************************')
        print('From the spreadsheet provided, in total,', student_count, 'students are critically in need of support\n')
        print('*************************************************************')
        print()

    def get_Summary(self, summary_day):
        print('These students missed both A1 and A2, and got less than 50% in Test 1')

        print('These students currently have an assignment average 15% less than their 1016 assignment average')

        # case 2: students who did well in CSC1016S assignments and are now doing worse in the CS2
        # example: based on test 1 these are the students that need help (then list them and their marks maybe)
        # example: based on a combination of t1, t2 and a1 " " " "

    def view_list(cls):
        print(cls.crit_data_frame)


class Marks_Summary(Summary):  # This class deals specifically with summaries for Marks
    def __init__(self, date_created, crit_count, case_1_count, case_2_count):
        super().__init__(date_created)
        self.crit_count = crit_count
        self.case_1_count = case_1_count
        self.case_2_count = case_2_count

    # alternative constructor
    @classmethod
    def get_Summary(cls, date_created, crit_students_file, summary_num):  # constructor for struggling students summary.
        cls.crit_students_file = crit_students_file

        if (summary_num == '1'):  # produce a summary for all students who meet Case 1
            student_frame = pd.ExcelFile(cls.crit_students_file)
            df1 = pd.read_excel(student_frame, 'Sheet1')
            print('Students who missed both A1 and A2, and got less than 50% in Test 1:\n')
            print(df1)

        elif (summary_num == '2'):  # produce a summary for all students who meet Case 2
            student_frame = pd.ExcelFile(cls.crit_students_file)
            df1 = pd.read_excel(student_frame, 'Sheet2')
            print('Students who currently have an assignment average 15% less than their 1016 assignment average:/n')
            print(df1)

        else:  # produce a summary for all students who need assistance
            df1 = pd.concat(pd.read_excel(cls.crit_students_file, sheet_name=None), ignore_index=True)
            df1.drop_duplicates(subset='student', ignore_index=True)  # make sure there are no duplicate students
            print('All students who need assistance:/n')
            print(df1)

    def update_summary(self):  # Updates the summary of all struggling students
        print('Student Analysis on', self.date_created)
        print('*************************************************************')
        print('From the spreadsheet provided, in total,', self.crit_count, 'students are critically in need of support\n')
        print(self.case_1_count, 'students missed both A1 and A2, and got less than 50% in Test 1/n')

        print(self.case_2_count, 'students currently have an assignment average 15% less than their 1016 assignment average')
        print('*************************************************************')
