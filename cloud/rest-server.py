#!flask/bin/python
from __future__ import print_function
from flask import Flask, jsonify, abort, request, make_response, url_for
from flask import render_template, redirect
from awscredentials import ACCESS_KEY, SECRET_KEY, REGION
from random import randint
import boto3
import string
import json
import time
import sys

app = Flask(__name__, static_url_path="")


sqs = boto3.resource('sqs', aws_access_key_id=ACCESS_KEY,
                            aws_secret_access_key=SECRET_KEY,
                            region_name=REGION)
                            
# Get the queue
queue = sqs.get_queue_by_name(QueueName='TestA')


dynamodb = boto3.resource('dynamodb', aws_access_key_id=ACCESS_KEY,
                            aws_secret_access_key=SECRET_KEY,
                            region_name=REGION)

Students = dynamodb.Table('Students');
Courses = dynamodb.Table('Courses');
Takes = dynamodb.Table('Takes');
Grades = dynamodb.Table('Grades');

# Add Major and GPA to main page
@app.route('/', methods=['GET'])
def home_page():
    students = getData(Students)
    return render_template('index.html', students=students['Items'])

# Requirement: Viewing all Students who are taking classes by semester
@app.route('/course', methods=['GET'])
def course_view_page():
    courses = getData(Courses)
    return render_template('courses.html', courses=courses['Items'])
    # return render_template('courses.html', title='Courses', courses=courses)



@app.route('/student/add', methods=['GET', 'POST'])
def student_add_page():
    if request.method == 'POST':
        data = { 
            "studentId": request.form['studentId'], 
            "firstName": request.form['firstName'], 
            "lastName": request.form['lastName'], 
            "major": request.form['major'], 
            "gpa":request.form['gpa']
        }

        storeData('Students', data)
        time.sleep(3)
        return redirect('/')
    else:
        return render_template('add_student.html', title='Add Student')


# Requirement: Adding a course
@app.route('/course/add', methods=['GET', 'POST'])
def course_add_page():
    if request.method == 'POST':
        data = { 
            "courseId": request.form['courseId'], 
            "courseName": request.form['courseName'], 
            "department": request.form['department']
        }

        storeData('Courses', data)
        time.sleep(3)
        return redirect('/course')
    else:
        return render_template('add_course.html', title='Add Course')

# Requirement: Add student to course
@app.route('/student/enroll', methods=['GET', 'POST'])
def student_enroll_page():
    if request.method == 'POST':

        data = { 
            "studentId": request.form['studentId'],
            "courseId": request.form['courseId'], 
            "semester": request.form['semester'], 
            "year": request.form['year']
        }

        storeData('Takes', data)
        time.sleep(3)
        return redirect('/semester')
    else:
        # Get students
        students = getData(Students)

        # Get courses
        courses = getData(Courses)

        return render_template('enroll_student.html', title='Enroll Student', students=students['Items'], courses=courses['Items'])

# Requirement: Semester filtering
@app.route('/semester', methods=['GET'])
def semester_view_page():

    # Get students
    students = getData(Students)

    # Get courses
    courses = getData(Courses)

    # Get takes
    takes = getData(Takes)

    studentObject = []

    for take in takes['Items']:
        for student in students['Items']:
            if student['studentId'] == take['studentId']:
                found = {
                    "firstName": student['firstName'], 
                    "lastName": student['lastName'], 
                    "semester": take['semester'], 
                    "year": take['year'],
                    "courseId": take['courseId']
                }
                studentObject.append(found)

    for object in studentObject:
        for course in courses['Items']:
            if course['courseId'] == object['courseId']:
                object['courseName'] = course['courseName']

    return render_template('semester.html', title='Semester', rows=studentObject)

# Requirement: Semester filtering
@app.route('/grades/', methods=['GET'])
def grades_view_page():

    # Get students
    students = getData(Students)

    # Get courses
    courses = getData(Courses)

    # Get takes
    grades = getData(Grades)

    studentObject = []

    for grade in grades['Items']:
        for student in students['Items']:
            if student['studentId'] == grade['studentId']:
                found = {
                    "firstName": student['firstName'], 
                    "lastName": student['lastName'], 
                    "grade": grade['grade'], 
                    "courseId": grade['courseId']
                }
                studentObject.append(found)

    for object in studentObject:
        for course in courses['Items']:
            if course['courseId'] == object['courseId']:
                object['courseName'] = course['courseName']

    return render_template('grades.html', title='Grade', rows=studentObject)

# Requirement: Add student to course
@app.route('/grades/add', methods=['GET', 'POST'])
def grades_add_page():
    if request.method == 'POST':
        print(request.form)
        data = { 
            "studentId": request.form['studentId'],
            "courseId": request.form['courseId'], 
            "grade": request.form['grade'] 
        }

        storeData('Grades', data)
        time.sleep(3)
        return redirect('/grades')
    else:
        # Get students
        students = getData(Students)

        # Get courses
        courses = getData(Courses)

        return render_template('add_grade.html', title='Enroll Student', students=students['Items'], courses=courses['Items'])


def getData(table):
    return table.scan()

def storeData(table, data):
    data['table'] = table
    queue.send_message(MessageBody=json.dumps(data))

if __name__ == '__main__':
    app.run(debug=True, port=5000)

