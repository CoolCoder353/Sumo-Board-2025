import wiringpi as w
import time
 
w.wiringPiSetup()  # For GPIO pin numbering
startbutton = 27  # Confirmed
w.pinMode(startbutton, w.GPIO.INPUT)  # Set to INPUT
w.pullUpDnControl(startbutton, w.PUD_DOWN) # Sets internal pull up resistor function
while True:
    time.sleep(0.1)
    #w.digitalWrite(27, 1)
    print(w.digitalRead(27))