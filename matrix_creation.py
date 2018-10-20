import csv
import copy

subjects_list = {}
grades = {}
mat1 = {}
with open('data/csv/1.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count != 0:
            course_code = row[len(row)-6]
            if course_code not in subjects_list:
                subjects_list[course_code] = 0
            grade_val = row[len(row)-3]
            if grade_val not in grades:
                grades[grade_val] = 0
        line_count+=1
csv_file.close()

grade_scale = {}
grade_scale['A+'] = 10
grade_scale['A'] = 10
grade_scale['A-'] = 9
grade_scale['B'] = 8
grade_scale['B-'] = 7
grade_scale['C'] = 6
grade_scale['C-'] = 5
grade_scale['D'] = 4
grade_scale['F'] = 2
grade_scale['S'] = 10
grade_scale['X'] = 2
grade_scale['I'] = 0
grade_scale['W'] = 0
grade_scale[''] = 0
grade_scale['On Leave'] = 0

with open('data/csv/1.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count != 0:
            student_val = row[1]
            student_val = int(student_val.split('Student ')[1])
            if student_val not in mat1:
                temp = copy.deepcopy(subjects_list)
                mat1[student_val] = temp
            course_code = row[len(row)-6]
            grade_val = grade_scale[row[len(row)-3]]
            mat1[student_val][course_code] = grade_val
            semester_val = row[2].split()
            semester_val = semester_val[len(semester_val)-1]
            mat1[student_val]['semester'] = semester_val
        line_count+=1

addval = len(mat1)
with open('data/csv/2.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count != 0:
            student_val = row[1]
            student_val = int(student_val.split('Student ')[1]) + addval
            if student_val not in mat1:
                temp = copy.deepcopy(subjects_list)
                mat1[student_val] = temp
            course_code = row[len(row)-6]
            grade_val = grade_scale[row[len(row)-3]]
            mat1[student_val][course_code] = grade_val
            semester_val = row[2].split()
            semester_val = semester_val[len(semester_val)-1]
            mat1[student_val]['semester'] = semester_val
        line_count+=1

addval = len(mat1)
with open('data/csv/3.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count != 0:
            student_val = row[1]
            student_val = int(student_val.split('Student ')[1]) + addval
            if student_val not in mat1:
                temp = copy.deepcopy(subjects_list)
                mat1[student_val] = temp
            course_code = row[len(row)-6]
            grade_val = grade_scale[row[len(row)-3]]
            mat1[student_val][course_code] = grade_val
            semester_val = row[2].split()
            semester_val = semester_val[len(semester_val)-1]
            mat1[student_val]['semester'] = semester_val
        line_count+=1

addval = len(mat1)
with open('data/csv/4.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count != 0:
            student_val = row[1]
            student_val = int(student_val.split('Student ')[1]) + addval
            if student_val not in mat1:
                temp = copy.deepcopy(subjects_list)
                mat1[student_val] = temp
            course_code = row[len(row)-6]
            grade_val = grade_scale[row[len(row)-3]]
            mat1[student_val][course_code] = grade_val
            semester_val = row[2].split()
            semester_val = semester_val[len(semester_val)-1]
            mat1[student_val]['semester'] = semester_val
        line_count+=1

addval = len(mat1)
with open('data/csv/5.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count != 0:
            student_val = row[1]
            student_val = int(student_val.split('Student ')[1]) + addval
            if student_val not in mat1:
                temp = copy.deepcopy(subjects_list)
                mat1[student_val] = temp
            course_code = row[len(row)-6]
            grade_val = grade_scale[row[len(row)-3]]
            mat1[student_val][course_code] = grade_val
            semester_val = row[2].split()
            semester_val = semester_val[len(semester_val)-1]
            mat1[student_val]['semester'] = semester_val
        line_count+=1

addval = len(mat1)
with open('data/csv/6.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count != 0:
            student_val = row[1]
            student_val = int(student_val.split('Student ')[1]) + addval
            if student_val not in mat1:
                temp = copy.deepcopy(subjects_list)
                mat1[student_val] = temp
            course_code = row[len(row)-6]
            grade_val = grade_scale[row[len(row)-3]]
            mat1[student_val][course_code] = grade_val
            semester_val = row[2].split()
            semester_val = semester_val[len(semester_val)-1]
            mat1[student_val]['semester'] = semester_val
        line_count+=1

addval = len(mat1)
with open('data/csv/7.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count != 0:
            student_val = row[1]
            student_val = int(student_val.split('Student ')[1]) +addval
            if student_val not in mat1:
                temp = copy.deepcopy(subjects_list)
                mat1[student_val] = temp
            course_code = row[len(row)-6]
            grade_val = grade_scale[row[len(row)-3]]
            mat1[student_val][course_code] = grade_val
            semester_val = row[2].split()
            semester_val = semester_val[len(semester_val)-1]
            mat1[student_val]['semester'] = semester_val
        line_count+=1

data_matrix = []

for k,v in mat1.iteritems():
    temp = []
    for key,val in v.iteritems():
        temp.append(val)
    data_matrix.append(temp)








            