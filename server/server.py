import json
from random import randint
import sqlite3
import time
from datetime import datetime

from user import User
from room import Room
from sensor import Sensor
from camera import Camera
from event import Event

from bottle import route, run, template, static_file, request, response, redirect, abort, error, get, post
import bottle

from faker import Faker
from faker.providers import date_time

faker = Faker()
faker.add_provider(date_time)

user = User(1, 'admin', 'admin')
room1 = Room(1, 'Living Room')
room2 = Room(2, 'Dining Room')
room3 = Room(3, 'Bedroom')
sensor1 = Sensor(2, 'infrared', 'b')
camera1 = Camera(1)
camera1.online = True
sensor1.online = True
room1.sensors.append(sensor1)
room1.cameras.append(camera1)

user.rooms = [room1, room2, room3]

# setup an in-memory database
db = sqlite3.connect(':memory:')

with open('static/logs.txt') as f:
    logs = f.readlines()

@route('/')
def index():
    return redirect("login")

@route('/login')
def index():
    return template("login_template")

@get('/login_failure')
def login_submit():
    return template("login_failure")

@route('/logout')
def index():
    return template("login_template")

@post('/login_submit')
def login_submit():
    username = request.forms.get('username')
    password = request.forms.get('password')
    if username == 'admin' and password == 'admin':
        redirect('/dashboard')
    else:
        redirect('/login_failure')

@route('/static/css/<filename>')
def serve_static_css(filename):
    return static_file(filename, root='./static/css')

@route('/static/img/<filename>')
def serve_static_images(filename):
    return static_file(filename, root='./static/img')

@route('/logs')
def logs_page():
    logs = []
    try:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM event ORDER BY timestamp DESC")
        for item in cursor:
            logs.append(Event(item[0], item[1], item[2], item[3]))
    except:
        abort(500, "SQL ERROR")
    return template("logs_template", logs=logs)

@route('/dashboard')
def dashboard_page():
    return template("dashboard_template", rooms=user.rooms)

@route('/layout')
def layout_page():
    return template("layout_template", rooms=user.rooms )

@route('/surveillance')
def surveillance_page():
    return template("surveillance_template", rooms=user.rooms)


# ----------
# API ROUTES
# ----------

@get('/api/users')
def user_api():
    username = request.query.user
    if username is None or not username:
        abort(400, "Expected value: 'user'")
    user = {
        "id": randint(0, 1000),
        "username": username
    }
    response.content_type = "application/json"
    return json.dumps(user)

@post('/api/sensor/events')
def sensor_events_post_api():
    sensor_id = None
    secret = None
    message = None
    if "sensor_id" in request.json and query_int_valid(request.json["sensor_id"]):
        sensor_id = int(request.json["sensor_id"])
    else:
        abort(400, "Missing or incorrect field: 'sensor_id'")

    if "secret" in request.json and request.json["secret"]:
        secret = request.json["secret"]
    else:
        abort(400, "Missing or incorrect field: 'secret'")

    if "message" in request.json and request.json["message"]:
        message = request.json["message"]
    else:
        abort(400, "Missing or incorrect field: 'message'")

    millis = int(round(time.time() * 1000))
    try:
        cursor = db.cursor()
        cursor.execute("INSERT INTO event (timestamp, message, sensor_id) VALUES (?, ?, ?)", (millis, message, sensor_id))
        db.commit()
    except:
        abort(500, "SQL ERROR")
    return

@get('/api/sensor/events')
def sensor_events_get_api():
    log_amount = parse_query_int_default(request.query.amount, 10)
    log_start = parse_query_int_default(request.query.start, 0)
    sensor_id = request.query.sensor_id
    if not query_int_valid(sensor_id):
        abort(400, "Expected value: 'sensor_id'")
    sensor_id = int(sensor_id)
    logs = []

    try:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM event WHERE sensor_id = ? ORDER BY timestamp", (sensor_id,))
        logs = cursor.fetchmany(log_amount)
    except:
        abort(500, "SQL ERROR")

    response.content_type = "application/json"
    return json.dumps(logs)

@get('/api/room')
def rooms_by_id_api():
    room_id = request.query.id
    if not query_int_valid(room_id):
        abort(400, "Expected value: 'id'")
    room_id = int(room_id)
    room = {
        "id": room_id,
        "name": faker.word()
    }
    response.content_type = "application/json"
    return json.dumps(room)

@get('/api/user/rooms')
def rooms_by_username_api():
    user_id = request.query.user_id
    if not query_int_valid(user_id):
        abort(400, "Expected value: 'user_id'")
    user_id = int(user_id)
    rooms = []
    for _ in range(randint(1,12)):
        rooms.append({
            "id": randint(0, 1000),
            "name": faker.word()
        })
    response.content_type = "application/json"
    return json.dumps(rooms)

@get('/api/room/sensors')
def sensors_by_room_api():
    room_id = request.query.room_id
    if not query_int_valid(room_id):
        abort(400, "Expected value: 'room_id'")
    room_id = int(room_id)
    sensors = []
    for _ in range(randint(1,12)):
        sensors.append({
            "id": randint(0, 1000),
            "type": faker.word()
        })
    response.content_type = "application/json"
    return json.dumps(sensors)

@get('/api/sensor')
def sensor_api():
    sensor_id = request.query.id
    if not query_int_valid(sensor_id):
        abort(400, "Expected value: 'sensor_id'")
    sensor_id = int(sensor_id)
    sensor = {
        "id": randint(0, 1000),
        "type": faker.word()
    }
    response.content_type = "application/json"
    return json.dumps(sensor)

def parse_query_int_default(value, default):
    if value is None or value == '':
        value = default
    else:
        value = int(value)
    return value

def query_int_valid(value):
    if value is None or not value:
        return False
    try:
        int(value)
    except ValueError:
        return False
    return True

def setup_db(conn):
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE event (
    id INTEGER PRIMARY KEY,
    sensor_id INTEGER NOT NULL,
    timestamp INTEGER NOT NULL,
    message TEXT,
    FOREIGN KEY(sensor_id) REFERENCES sensor(id))""")
    cursor.execute("""CREATE TABLE sensor (
    id INTEGER PRIMARY KEY,
    type TEXT NOT NULL,
    secret TEXT NOT NULL)""")
    cursor.execute("""CREATE TABLE user (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    password TEXT NOT NULL)""")
    cursor.execute("""CREATE TABLE room (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL)""")
    cursor.execute("""CREATE TABLE room_sensors (
    id INTEGER PRIMARY KEY,
    sensor_id INTEGER,
    room_id INTEGER,
    FOREIGN KEY(sensor_id) REFERENCES sensor(id),
    FOREIGN KEY(room_id) REFERENCES room(id))""")
    cursor.execute("""CREATE TABLE user_rooms (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    room_id INTEGER,
    FOREIGN KEY(user_id) REFERENCES user(id),
    FOREIGN KEY(room_id) REFERENCES room(id))""")
    conn.commit()

def populate_db(conn):
    cursor = db.cursor()
    for _ in range(100):
        cursor.execute("INSERT INTO event (timestamp, message, sensor_id) VALUES (?, ?, ?)", (faker.unix_time(), faker.sentence(), randint(0, 10000)))
    conn.commit()

# setup the database
setup_db(db)
populate_db(db)

run(host='192.168.1.160', port=8080, debug=True)
