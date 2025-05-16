# from flask import render_template, session, redirect,request
# from flask_app import app
# import random
# # Importing Dynamically the Color
# # from ....sort_disk import disk_color
# from ..models.wifi import data_exported
# print(data_exported)
# @app.route("/")
# def index():
#     return redirect("/dashboard")

# # # Sample state (replace with actual logic)
# # servo_angle = 45
# # conveyor_speed = 100

# @app.route("/dashboard")
# def dashboard():
#     # print(data)
#     print("Hello")
#     # to be removed when the import is done
#     disk_color = data_exported["LED"]
#     # Static Numbers for Data Reg of Disks if Nothing yet
#     if 'redCount' not in session:
#         session['redCount'] = 0
#     if 'greenCount' not in session:
#         session['greenCount'] = 0
#     if 'blueCount' not in session:
#         session['blueCount'] = 0
#     # Increeasing wiht the appearance of the color each time
#     # 1: blue
#     # 2: Green
#     # 3: Red
#     if disk_color==2:
#         session['greenCount']+=1
#     elif disk_color==1:
#         session['blueCount']+=1
#     else:
#         print("Nothing Detected")
#     # Motors Params
#     # if 'servo_angle' not in session:
#     #     session['servo_angle'] = 45  # default value from system
#     # if 'conveyor_speed' not in session:
#     #     session['conveyor_speed'] = 100  # default value
#     servo_angle=data_exported["Servo angle"]
#     conveyor_speed=data_exported["Motor speed"]*1000/255 #converted to rpm
#     return render_template("dashboard.html",ledOn=disk_color,greenCount=session['greenCount'], blueCount=session['blueCount'],
#                             servo_angle=servo_angle,conveyor_speed=conveyor_speed)




from flask import render_template, session, redirect, request
from flask_app import app
from ..models.wifi import fetch_esp_data  # Now you're importing the function

@app.route("/")
def index():
    return redirect("/dashboard")

@app.route("/dashboard")
def dashboard():
    print("Fetching data from ESP...")
    data = fetch_esp_data()
    if not data:
        return "Error: Could not retrieve data from ESP32", 500

    disk_color = data.get("LED", 0)
    servo_angle = data.get("Servo angle", 0)
    conveyor_speed = data.get("Motor speed", 0) * 1000 / 255

    if 'redCount' not in session:
        session['redCount'] = 0
    if 'greenCount' not in session:
        session['greenCount'] = 0
    if 'blueCount' not in session:
        session['blueCount'] = 0

    if disk_color == 2:
        session['greenCount'] += 1
    elif disk_color == 1:
        session['blueCount'] += 1

    return render_template(
        "dashboard.html",
        ledOn=disk_color,
        greenCount=session['greenCount'],
        blueCount=session['blueCount'],
        servo_angle=servo_angle,
        conveyor_speed=conveyor_speed
    )






# Posting To the System Variations Needed In Motors params

@app.route('/update-servo', methods=['POST'])
def update_servo():
    if 'servo_angle' not in session:
        session['servo_angle'] = 45 #Default Value Would be set from the current system

    if request.form['action'] == 'increase':
        session['servo_angle'] += 5
    elif request.form['action'] == 'decrease':
        session['servo_angle'] -= 5

    return redirect('/dashboard')

@app.route('/update-conveyor', methods=['POST'])
def update_conveyor():
    if 'conveyor_speed' not in session:
        session['conveyor_speed'] = 100 #Default Value Would be set from the current system

    if request.form['action'] == 'increase':
        session['conveyor_speed'] += 10
    elif request.form['action'] == 'decrease':
        session['conveyor_speed'] -= 10

    return redirect('/dashboard')

