import RPi.GPIO as GPIO
import time
from picamera import PiCamera
from lobe import ImageModel
GPIO.setwarnings(False); GPIO.setmode(GPIO.BCM)
trig = 23 
echo = 24 
led = 17
servo_pin = 18

GPIO.setup(trig, GPIO.OUT)
GPIO.setup(echo, GPIO.IN)
GPIO.setup(led, GPIO.OUT)
GPIO.setup(servo_pin, GPIO.OUT)

servo = GPIO.PWM(servo_pin, 50)
servo.start(0)
servo.ChangeDutyCycle(7.5)

GPIO.output(trig, False)
print("Waiting for sensor to settle")
time.sleep(2)

camera = PiCamera()
model = ImageModel.load('/home/jbnu/Lobe/model')  #경로 수정

def take_photo():
    time.sleep(2)
    print("Pressed")
    # Start the camera preview
    camera.start_preview(alpha=200)
    # wait 2s or more for light adjustment
    time.sleep(3)
    # Optional image rotation for camera
    # --> Change or comment out as needed
    camera.rotation = 270
    #Input image file path here
    # --> Change image path as needed
    camera.capture('/home/jbnu/Pictures/image.jpg')
    #Stop camera
    camera.stop_preview()
    time.sleep(1)

def select(label):
    print(label)
    if label == "opaque":
        i = 7.5
        while(i > 5.0):
            i -= 0.01
            servo.ChangeDutyCycle(i)
            time.sleep(0.01)
        #servo.ChangeDutyCycle(5.0)
        time.sleep(1)
        servo.ChangeDutyCycle(7.5)
        time.sleep(1)
    if label == "transparent":
        i = 7.5
        while(i < 10.0):
            i += 0.01
            servo.ChangeDutyCycle(i)
            time.sleep(0.01)
        #servo.ChangeDutyCycle(10.0)
        time.sleep(1)
        servo.ChangeDutyCycle(7.5)
        time.sleep(1)

try:
    GPIO.output(led, False)
    while True:
        '''
        servo.ChangeDutyCycle(7.5)  # 90도
        time.sleep(2)
        servo.ChangeDutyCycle(12.5)  # 180도
        time.sleep(2)
        servo.ChangeDutyCycle(2.5)  # 0도
        time.sleep(2)
        '''
        GPIO.output(trig, True)
        time.sleep(0.00001)
        GPIO.output(trig, False)
        
        while GPIO.input(echo) == 0:
            pulse_start = time.time()
        while GPIO.input(echo) == 1:
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 34300/2
        distance = round(distance, 2)
        print("Distance : ", distance, "cm")

        if distance <= 23:
            GPIO.output(led, True)
            take_photo()
            result = model.predict_from_file('/home/jbnu/Pictures/image.jpg')
            select(result.prediction)
            '''
            label = result.prediction
            print(label)
            print("start")
            servo.start(0)
            if label == "opaque":
                servo.ChangeDutyCycle(2.5)
                time.sleep(1)
                servo.ChangeDutyCycle(7.5)
                time.sleep(1)
            if label == "transparent":
                servo.ChangeDutyCycle(12.5)
                time.sleep(1)
                servo.ChangeDutyCycle(7.5)
                time.sleep(1)            
            print("end")
            servo.stop()
            '''
            time.sleep(0.4)
        else:
            time.sleep(0.4)
            GPIO.output(led, False)
except KeyboardInterrupt:
    print("Measurement stopped by User")
    servo.stop()
    GPIO.cleanup()
