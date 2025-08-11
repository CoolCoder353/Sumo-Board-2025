// Include the Cytron motor driver library for controlling DC motors
#include <CytronMotorDriver.h>

// IR sensor pins for obstacle detection
int leftIR = 10;      // Left IR sensor pin
int centerIR = 10;    // Center IR sensor pin  
int rightIR = 10;     // Right IR sensor pin
int backIR = 10;      // Back IR sensor pin (currently unused)

// Color sensor pins for detecting white boundary lines
int colorLeft = A0;   // Left color sensor (analog pin)
int colorRight = A1;  // Right color sensor (analog pin)

// Motor speed settings (0-255 PWM values)
float forwardSpeed = 50;   // Normal forward movement speed
float backwardSpeed = 25;  // Backward movement speed
float turnSpeed = 20;      // Turning speed
float sprintSpeed = 100;   // High speed when enemy is detected

// Sensor threshold values
float whiteThreshold = 200;      // Analog value threshold for detecting white surface
float distanceThreshold = 100;   // Digital threshold for IR obstacle detection

// Behavior control flags
bool hardTurn = false;                    // Enable hard turns (both motors in opposite directions)
bool ignoreWhiteIfAttacking = false;     // Ignore white lines when enemy is detected
bool sprintOnceFoundEnemy = false;       // Use sprint speed when enemy is found
bool turnBackwardsWhenSeeWhite = true;   // Back up before turning when white line detected

// Timing values for movements (in milliseconds)
float turnTimeOnWhite = 10;      // Time to turn when white line detected
float backwardTimeOnWhite = 10;  // Time to move backward when white line detected

CytronMD motorLeft(PWM_DIR, 5, 4);  // Left motor
CytronMD motorRight(PWM_DIR, 6, 7); // Right motor

void setup()
{
  // Set pin modes
  pinMode(leftIR, INPUT);
  pinMode(centerIR, INPUT);
  pinMode(rightIR, INPUT);
  pinMode(backIR, INPUT);

  pinMode(colorLeft, INPUT);
  pinMode(colorRight, INPUT);

  delay(3000);
}

void forward()
{
  motorLeft.setSpeed(forwardSpeed);
  motorRight.setSpeed(forwardSpeed);
}

void backward()
{
  motorLeft.setSpeed(-backwardSpeed);
  motorRight.setSpeed(-backwardSpeed);
}

void left()
{
  if (hardTurn)
  {
    motorLeft.setSpeed(-turnSpeed);
    motorRight.setSpeed(turnSpeed);
  }
  else
  {
    motorLeft.setSpeed(0);
    motorRight.setSpeed(turnSpeed);
  }
}
void right()
{
  if (hardTurn)
  {
    motorLeft.setSpeed(turnSpeed);
    motorRight.setSpeed(-turnSpeed);
  }
  else
  {
    motorLeft.setSpeed(turnSpeed);
    motorRight.setSpeed(0);
  }
}
void stop()
{
  motorLeft.setSpeed(0);
  motorRight.setSpeed(0);
}

bool isWhiteAt(int pinNum)
{
  if (analogRead(pinNum) >= whiteThreshold)
  {
    return true;
  }
  return false;
}

bool canSeeAt(int pinNum)
{
  if (digitalRead(pinNum) <= distanceThreshold)
  {
    return true;
  }
  return false;
}

void loop()
{
  // put your main code here, to run repeatedly:
  if (canSeeAt(centerIR) && (ignoreWhiteIfAttacking || (!isWhiteAt(colorLeft) && !isWhiteAt(colorRight))))
  {
    if (sprintOnceFoundEnemy)
    {
      sprint();
    }
    else
    {
      forward();
    }
  }
  else if (isWhiteAt(colorLeft))
  {
    if (turnBackwardsWhenSeeWhite)
    {
      backward();
      if (backwardTimeOnWhite > 0)
      {
        delay(backwardTimeOnWhite)
      }
    }
    right();
    if (turnTimeOnWhite > 0)
    {
      delay(turnTimeOnWhite)
    }
  }
  else if (isWhiteAt(colorRight))
  {
    if (turnBackwardsWhenSeeWhite)
    {
      backward();
      if (backwardTimeOnWhite > 0)
      {
        delay(backwardTimeOnWhite)
      }
    }
    left();
    if (turnTimeOnWhite > 0)
    {
      delay(turnTimeOnWhite)
    }
  }
  else if (canSeeAt(leftIR))
  {
    left()
  }
  else if (canSeeAt(rightIR))
  {
    right()
  }
  else
  {
    forward()
  }
}
