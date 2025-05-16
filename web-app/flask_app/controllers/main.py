
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
    if 'servo_angle' not in session:
        servo_angle = data.get("Servo angle", 0)
    else: 
        servo_angle=session['servo_angle'] 
    if 'conveyor_speed' not in session:
        conveyor_speed = data.get("Motor speed", 0) * 1000 / 255
    else: 
        conveyor_speed= session['conveyor_speed']
    disk_color = data.get("LED", 0)
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


# servo_angle_updated=0
# conveyor_speed_updated=0



# Posting To the System Variations Needed In Motors params

@app.route('/update-servo', methods=['POST'])
def update_servo():
    global servo_angle_updated  # This is important!
    
    # if 'servo_angle' not in session:
    #     session['servo_angle'] = 45

    if request.form['action'] == 'increase':
        session['servo_angle'] += 5
    elif request.form['action'] == 'decrease':
        session['servo_angle'] -= 5

    servo_angle_updated = session['servo_angle']
    return redirect('/dashboard')


@app.route('/update-conveyor', methods=['POST'])
def update_conveyor():
    global conveyor_speed_updated  # This is important!

    # if 'conveyor_speed' not in session:
    #     session['conveyor_speed'] = 100

    if request.form['action'] == 'increase':
        session['conveyor_speed'] += 10
    elif request.form['action'] == 'decrease':
        session['conveyor_speed'] -= 10

    # conveyor_speed_updated = session['conveyor_speed'] * 255 / 1000
    return redirect('/dashboard')

