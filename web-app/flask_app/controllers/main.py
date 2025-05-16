from flask import render_template, session, redirect,request
from flask_app import app
import random
# Importing Dynamically the Color
# from ....sort_disk import disk_color
from ..models.sort_disk import data



@app.route("/")
def index():
    return redirect("/dashboard")

# # Sample state (replace with actual logic)
# servo_angle = 45
# conveyor_speed = 100

@app.route("/dashboard")
def dashboard():
    print(data)
    # to be removed when the import is done
    disk_color = random.choice(['red', 'green', 'blue'])
    # Static Numbers for Data Reg of Disks if Nothing yet
    if 'redCount' not in session:
        session['redCount'] = 0
    if 'greenCount' not in session:
        session['greenCount'] = 0
    if 'blueCount' not in session:
        session['blueCount'] = 0
    # Increeasing wiht the appearance of the color each time
    if disk_color=="green":
        session['greenCount']+=1
    elif disk_color=="blue":
        session['blueCount']+=1
    elif disk_color=="red":
        session['redCount']+=1
    else:
        print("Nothing Detected")
    # Motors Params
    if 'servo_angle' not in session:
        session['servo_angle'] = 45  # default value from system
    if 'conveyor_speed' not in session:
        session['conveyor_speed'] = 100  # default value
    return render_template("dashboard.html",ledOn=disk_color, redCount=session['redCount'], greenCount=session['greenCount'], blueCount=session['blueCount'],
                            servo_angle=session['servo_angle'],conveyor_speed=session['conveyor_speed'])

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

