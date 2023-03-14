from flask import Flask, render_template, request
import json
import pandas as pd 
import numpy as np

with open('courses.json') as f:
    courses = json.load(f)

with open('slots.json') as f:
    slots = json.load(f)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/check_clash', methods=['GET', 'POST'])
def check_clash():
    selectedCourses=request.form.getlist('course_checkbox')
    valid_courses=[]
    for i in selectedCourses:
        if len(valid_courses)==0:
            valid_courses.append(i)
            continue

        if validate_input(inp=i, course_list=valid_courses, course_details=courses):
            valid_courses.append(i)
        else: 
            return "Courses are clashing!" ## we will add some error html here
    
    def create_DataFrame():
        return pd.DataFrame(columns=['8:30-9:50', '10:00-11:20', '11:30-12:50', '14:00-15:20', '15:30-16:50', '17:00-18:30'], index=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'])
    
    df=create_DataFrame()
    for i in valid_courses:
        book_slot(df=df, slots=slots, course_code=i, course_details=courses)
    print(df)
    return render_template('time_table.html', df=df)

if __name__ == '__main__':
    app.run(debug=True)