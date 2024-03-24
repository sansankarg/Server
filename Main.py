from flask import Flask, render_template, request, Response
import cv2
import os
from flask_mqtt import Mqtt

app = Flask(__name__)
app.config['MQTT_BROKER_URL'] = 'Raspi_ip_address'
app.config['MQTT_BROKER_PORT'] = 1883  #default one No need to change
app.config['MQTT_USERNAME'] = ''
app.config['MQTT_PASSWORD'] = '' #Fill both username and password if you have one or else leave it empty
app.config['MQTT_KEEPALIVE'] = 5
app.config['MQTT_TLS_ENABLED'] = False

mqtt = Mqtt(app)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/view.html')
def view():
    print ("redirected to stream page")
    return render_template('view.html')

@app.route('/about.html')
def about():
    print ("redirected to stream page")
    return render_template('about.html')
@app.route('/home.html')
def home():
    print ("redirected to stream page")
    return render_template('home.html')
@app.route('/routine.html')
def routine():
    print ("redirected to stream page")
    return render_template('routine.html')

@app.route('/main_page.html')
def main():
    print ("redirected to main page")
    return render_template('main_page.html')

@app.route('/left')
def left():
    print ("Left")
    os.system("python ser.py 1 2 0.1 1")
    return ("nothing")

@app.route('/center')
def center():
    print ("Center")
    os.system("python ser.py 89 90 0.3 1")
    return ("nothing")

@app.route('/right')
def right():
    print ("Right")
    os.system("python ser.py 179 180 0.1 1")
    return ("nothing")

@app.route('/dev1_on')
def dev1_on():
    print ("dev1 is on")
    mqtt.publish('connect', '1_onn')
    return ("nothing")
@app.route('/dev1_off')
def dev1_off():
    print ("dev1 is off")
    mqtt.publish('connect', '1_off')
    return ("nothing")
@app.route('/dev2_on')
def dev2_on():
    print ("dev2 is on")
    mqtt.publish('connect', '2_onn')
    return ("nothing")
@app.route('/dev2_off')
def dev2_off():
    print ("dev2 is off")
    mqtt.publish('connect', '2_off')
    return ("nothing")
@app.route('/dev3_on')
def dev3_on():
    print ("dev3 is on")
    mqtt.publish('connect', '3_onn')
    return ("nothing")
@app.route('/dev3_off')
def dev3_off():
    print ("dev3 is off")
    mqtt.publish('connect', '3_off')
    return ("nothing")
@app.route('/dev4_on')
def dev4_on():
    print ("dev4 is on")
    mqtt.publish('connect', '4_onn')
    return ("nothing")
@app.route('/dev4_off')
def dev4_off():
    print ("dev4 is off")
    mqtt.publish('connect', '4_off')
    return ("nothing")
@app.route('/routine_1')
def routine_1():
    print ("Routine 1 is enabled")
    os.system("python routine1.py")
    return ("nothing")
@app.route('/routine_2')
def routine_2():
    print ("Routine 2 is enabled")
    os.system("python routine2.py")
    return ("nothing")
@app.route('/routine_3')
def routine_3():
    print ("Routine 3 is enabled")
    os.system("python routine3.py")
    return ("nothing")

def gen_frames():
    camera = cv2.VideoCapture(0)
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True)