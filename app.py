from flask import Flask, render_template, request
import json
import pandas as pd 
import numpy as np

with open('./data/courses.json') as f:
    courses = json.load(f)

with open('./data/slots.json') as f:
    slots = json.load(f)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html', courses=courses.keys())

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



def book_slot(df, slots, course_code, course_details):
    course_info=course_details[course_code]
    slot=course_details[course_code]['slot']
    if slot=='NA':
        return
    slot_data=slots.get(slot)
    if slot_data==None:
        print("slot not readable")
        return 
    cell_data=course_code + "/" + course_info['name'] + "/" + course_info['room'] + "/" + course_info['fractal']+" $ "
    if len(slot_data)==2:
        for i in range(len(slot_data)):
            if type(df.loc[slot_data[i]["day"], slot_data[i]['start']+"-"+slot_data[i]['end']])==str:
                df.loc[slot_data[i]["day"], slot_data[i]['start']+"-"+slot_data[i]['end']]+=cell_data
            else:
                df.loc[slot_data[i]["day"], slot_data[i]['start']+"-"+slot_data[i]['end']]=cell_data
        
    if len(slot_data)==1:
        possi={'8:30-11:20' : ['9:50', '10:00'], '10:00-12:50' : ['11:20', '11:30'], '14:00-16:50' : ['15:20', '15:30'], '15:30-18:30' : ['16:50', '17:00']}
        if slot_data[0]['start']+"-"+slot_data[0]['end'] in possi.keys():
            mid=possi[slot_data[0]['start']+"-"+slot_data[0]['end']]
            if type(df.loc[slot_data[0]["day"], slot_data[0]['start']+"-"+mid[0]])==str:
                df.loc[slot_data[0]["day"], slot_data[0]['start']+"-"+mid[0]]+=cell_data
                df.loc[slot_data[0]["day"], mid[1]+"-"+slot_data[0]['end']]+=cell_data
            else:
                df.loc[slot_data[0]["day"], slot_data[0]['start']+"-"+mid[0]]=cell_data
                df.loc[slot_data[0]["day"], mid[1]+"-"+slot_data[0]['end']]=cell_data
        else:
            return 




if __name__ == '__main__':
    app.run()