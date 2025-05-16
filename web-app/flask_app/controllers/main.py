# from flask import render_template, session, redirect,request, Blueprint
# from flask_app import app
# import random
# # Importing Dynamically the Color
# # from ....sort_disk import disk_color
# # from ..models.sort_disk import data
# from motor_state import load_motor_state, save_motor_state

# motors_bp = Blueprint('motors', __name__)


# @app.route("/")
# def index():
#     return redirect("/dashboard")

# # # Sample state (replace with actual logic)
# # servo_angle = 45
# # conveyor_speed = 100

# @app.route("/dashboard")
# def dashboard():
#     # print(data)
#     # to be removed when the import is done
#     disk_color = random.choice(['red', 'green', 'blue'])
#     # Static Numbers for Data Reg of Disks if Nothing yet
#     if 'redCount' not in session:
#         session['redCount'] = 0
#     if 'greenCount' not in session:
#         session['greenCount'] = 0
#     if 'blueCount' not in session:
#         session['blueCount'] = 0
#     # Increeasing wiht the appearance of the color each time
#     if disk_color=="green":
#         session['greenCount']+=1
#     elif disk_color=="blue":
#         session['blueCount']+=1
#     elif disk_color=="red":
#         session['redCount']+=1
#     else:
#         print("Nothing Detected")
#     # Motors Params
#     if 'servo_angle' not in session:
#         session['servo_angle'] = 45  # default value from system
#     if 'conveyor_speed' not in session:
#         session['conveyor_speed'] = 100  # default value
#     return render_template("dashboard.html",ledOn=disk_color, redCount=session['redCount'], greenCount=session['greenCount'], blueCount=session['blueCount'],
#                             servo_angle=session['servo_angle'],conveyor_speed=session['conveyor_speed'])

# # Posting To the System Variations Needed In Motors params

# @app.route('/update-servo', methods=['POST'])
# def update_servo():
#     if 'servo_angle' not in session:
#         session['servo_angle'] = 45 #Default Value Would be set from the current system

#     if request.form['action'] == 'increase':
#         session['servo_angle'] += 5
#     elif request.form['action'] == 'decrease':
#         session['servo_angle'] -= 5

#     return redirect('/dashboard')

# @app.route('/update-conveyor', methods=['POST'])
# def update_conveyor():
#     if 'conveyor_speed' not in session:
#         session['conveyor_speed'] = 100 #Default Value Would be set from the current system

#     if request.form['action'] == 'increase':
#         session['conveyor_speed'] += 10
#     elif request.form['action'] == 'decrease':
#         session['conveyor_speed'] -= 10

#     return redirect('/dashboard')
from flask import Blueprint, render_template, redirect, request
import random
from motor_state import load_motor_state, save_motor_state

motors_bp = Blueprint('motors', __name__)

# Simulated color detection
@motors_bp.route('/dashboard')
def dashboard():
    disk_color = random.choice(['red', 'green', 'blue'])

    # Load current motor state
    state = load_motor_state()

    return render_template("dashboard.html",
                           ledOn=disk_color,
                           redCount=0, greenCount=0, blueCount=0,  # replace with real values later
                           servo_angle=state["servo_angle"],
                           conveyor_speed=state["conveyor_speed"])

@motors_bp.route('/update-servo', methods=['POST'])
def update_servo():
    state = load_motor_state()
    if request.form['action'] == 'increase':
        state['servo_angle'] += 5
    elif request.form['action'] == 'decrease':
        state['servo_angle'] -= 5
    save_motor_state(state)
    return redirect('/dashboard')

@motors_bp.route('/update-conveyor', methods=['POST'])
def update_conveyor():
    state = load_motor_state()
    if request.form['action'] == 'increase':
        state['conveyor_speed'] += 10
    elif request.form['action'] == 'decrease':
        state['conveyor_speed'] -= 10
    save_motor_state(state)
    return redirect('/dashboard')

