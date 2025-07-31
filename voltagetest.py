import wiringpi as w
import time
 
w.wiringPiSetup()  # For GPIO pin numbering
w.digitalWrite(27, 1)
while True:
    time.sleep(0.1)
    #w.digitalWrite(27, 1)
    print(w.digitalRead(27))