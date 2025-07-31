import wiringpi as w
 
w.wiringPiSetup()  # For GPIO pin numbering
while True:
    w.digitalWrite(27, 1)