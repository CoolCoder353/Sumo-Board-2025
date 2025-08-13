// Include the Cytron motor driver library for controlling DC motors
#include "CytronMotorDriver.h"
#include "digitalWriteFast.h"

// IR sensor pins for obstacle detection
const int leftIR = 10;   // Left IR sensor pin
const int centerIR = 10; // Center IR sensor pin
const int rightIR = 10;  // Right IR sensor pin
const int backIR = 10;   // Back IR sensor pin (currently unused)

// Color sensor pins for detecting white boundary lines
const int colorLeft = A0;  // Left color sensor (analog pin)
const int colorRight = A1; // Right color sensor (analog pin)

// Motor speed settings (0-255 PWM values)
const int forwardSpeed = 50;  // Normal forward movement speed
const int backwardSpeed = 25; // Backward movement speed
const int turnSpeed = 20;     // Turning speed
const int sprintSpeed = 100;  // High speed when enemy is detected

// Sensor threshold values
const int whiteThreshold = 200;    // Analog value threshold for detecting white surface
const int distanceThreshold = 100; // Digital threshold for IR obstacle detection

// Behavior control flags
const bool hardTurn = true;                  // Enable hard turns (both motors in opposite directions)
const bool ignoreWhiteIfAttacking = true;    // Ignore white lines when enemy is detected
const bool sprintOnceFoundEnemy = false;     // Use sprint speed when enemy is found
const bool turnBackwardsWhenSeeWhite = true; // Back up before turning when white line detected
const bool useFastPinWrites = true;

// Timing values for movements (in milliseconds)
const int turnTimeOnWhite = 10;     // Time to turn when white line detected
const int backwardTimeOnWhite = 10; // Time to move backward when white line detected

// Initialize motor driver objects using PWM_DIR mode
// PWM_DIR mode uses separate pins for speed (PWM) and direction
CytronMD motorLeft(PWM_DIR, 5, 4);  // Left motor: PWM pin 5, DIR pin 4
CytronMD motorRight(PWM_DIR, 6, 7); // Right motor: PWM pin 6, DIR pin 7

void setup()
{
  if (useFastPinWrites)
  {
    pinModeFast(leftIR, INPUT);
    pinModeFast(centerIR, INPUT);
    pinModeFast(rightIR, INPUT);
    pinModeFast(backIR, INPUT);

    pinModeFast(colorLeft, INPUT);
    pinModeFast(colorRight, INPUT);
  }
  else
  {
    // Configure IR sensor pins as inputs
    pinMode(leftIR, INPUT);
    pinMode(centerIR, INPUT);
    pinMode(rightIR, INPUT);
    pinMode(backIR, INPUT);

    // Configure color sensor pins as inputs (analog pins don't need pinMode)
    pinMode(colorLeft, INPUT);
    pinMode(colorRight, INPUT);
  }
  // Wait 3 seconds before starting (sumo competition requirement)
  delay(3000);
}

// Movement functions

// Move forward at normal speed
void forward()
{
  Serial.println("Moving Forward");
  motorLeft.setSpeed(forwardSpeed);
  motorRight.setSpeed(forwardSpeed);
}

// Move backward at reduced speed
void backward()
{
  Serial.println("Moving Backward");
  motorLeft.setSpeed(-backwardSpeed);
  motorRight.setSpeed(-backwardSpeed);
}

// Turn left - either hard turn or soft turn based on hardTurn flag
void left()
{
  if (hardTurn)
  {
    Serial.println("Moving left hard turn");
    // Hard turn: left motor backward, right motor forward
    motorLeft.setSpeed(-turnSpeed);
    motorRight.setSpeed(turnSpeed);
  }
  else
  {
    Serial.println("Moving left soft turn");
    // Soft turn: stop left motor, move right motor forward
    motorLeft.setSpeed(0);
    motorRight.setSpeed(turnSpeed);
  }
}

// Turn right - either hard turn or soft turn based on hardTurn flag
void right()
{
  if (hardTurn)
  {
    Serial.println("Moving right hard turn");
    // Hard turn: left motor forward, right motor backward
    motorLeft.setSpeed(turnSpeed);
    motorRight.setSpeed(-turnSpeed);
  }
  else
  {
    Serial.println("Moving right soft turn");
    // Soft turn: move left motor forward, stop right motor
    motorLeft.setSpeed(turnSpeed);
    motorRight.setSpeed(0);
  }
}

// Stop both motors
void stop()
{
  Serial.println("Stopping Motors");
  motorLeft.setSpeed(0);
  motorRight.setSpeed(0);
}

// Sensor reading functions

// Check if white surface is detected at specified analog pin
// Returns true if analog reading is above white threshold
bool isWhiteAt(int pinNum)
{
  if (analogRead(pinNum) >= whiteThreshold)
  {
    return true;
  }

  return false;
}

// Check if obstacle is detected by IR sensor at specified digital pin
// Returns true if digital reading indicates object within distance threshold
bool canSeeAt(int pinNum)
{
  if (useFastPinWrites)
  {
    if (digitalReadFast(pinNum) <= distanceThreshold)
    {
      return true;
    }
  }
  else
  {
    if (digitalRead(pinNum) <= distanceThreshold)
    {
      return true;
    }
  }
  return false;
}

// Move forward at high speed (sprint mode)
void sprint()
{
  Serial.println("Sprinting Forward");
  motorLeft.setSpeed(sprintSpeed);
  motorRight.setSpeed(sprintSpeed);
}

void loop()
{
  // Main control logic - runs continuously

  // Priority 1: If enemy detected in center AND not on white line (or ignoring white)
  if (canSeeAt(centerIR))
  {
    stop(); // Stop turning if seen
  }
  // Priority 4: Enemy detected on left side
  else if (canSeeAt(leftIR))
  {
    left();
  }
  // Priority 5: Enemy detected on right side
  else if (canSeeAt(rightIR))
  {
    right();
  }
  // // Priority 6: Enemy detected behind us
  // else if (canSeeAt(backIR))
  // {
  //   right();
  // }
}
