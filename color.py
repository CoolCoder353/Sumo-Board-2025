import wiringpi as w
colorLeft = 26 ##Confirmed
colorRight = 25 ##Confirmed
w.wiringPiSetup()  # For GPIO pin numbering
w.pinMode(colorLeft, w.GPIO.INPUT)
w.pinMode(colorRight, w.GPIO.INPUT)
while True:
    colorLeftValue = w.analogRead(colorLeft)
    colorRightValue = w.analogRead(colorRight)
    
    print(f"ANALOG Color Left: {colorLeftValue}, Color Right: {colorRightValue}")

    w.delay(100)
    colorLeftValue = w.digitalRead(colorLeft)
    colorRightValue = w.digitalRead(colorRight)
    print(f"DIGITAL Color Left: {colorLeftValue}, Color Right: {colorRightValue}")
