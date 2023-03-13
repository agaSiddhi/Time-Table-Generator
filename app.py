from flask import Flask, render_template
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

def validate_input(inp, course_list, course_details):
    try:
        inp_details=course_details[inp]
    except:
        print("Course doesnot exist")
        return False
    
    inp_slot=inp_details['slot']
    inp_fractal=inp_details['fractal']
    
    if inp_slot=="NA" or inp_fractal=="NA":
        return True
    
    inp_fractal=convert_fractal_to_list(inp_fractal)
    
    for course in course_list:
        if course==inp:
            print('Course have been added before')
            return False
        curr_course_details=course_details[course]
        curr_course_slot=curr_course_details['slot']
        
        if curr_course_details['fractal']=="NA" or curr_course_slot=="NA":
            continue
        
        curr_course_fractal=convert_fractal_to_list(curr_course_details['fractal'])
        
        if curr_course_slot==inp_slot and len(Intersection(curr_course_fractal, inp_fractal))!=0:
            print(f'course {inp} and {course} clash!!!')
            return False
        else:
            continue
            
    return True

def convert_fractal_to_list(fractal):
    converted_fractal=[]
    for i in range(int(fractal[0]), int(fractal[1])+1): 
        converted_fractal.append(i)
    return converted_fractal


def Intersection(lst1, lst2):
    return list(set(lst1) & set(lst2))

if __name__ == '__main__':
    app.run(debug=True)