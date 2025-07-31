import wiringpi as w
import time
 
w.wiringPiSetup()  # For GPIO pin numbering
startbuttonread = 27  # Confirmed
startbuttonwrite = 25 #Confirmed
w.pinMode(startbuttonread, w.GPIO.INPUT)  # Set to INPUT
w.pinMode(startbuttonwrite, w.GPIO.OUTPUT) # Set to OUTPUT
w.digitalWrite(startbuttonwrite, 1)

while True:
    time.sleep(0.1)
    #w.digitalWrite(27, 1)
    print(w.digitalRead(27))