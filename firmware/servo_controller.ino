#include <Arduino.h>
#include <Servo.h>

Servo servo1;
Servo servo2;
Servo servo3;
Servo servo4;

const int PIN_SERVO1 = 3;
const int PIN_SERVO2 = 5;
const int PIN_SERVO3 = 6;
const int PIN_SERVO4 = 9;

String rxBuffer = "";

float clampDeg(float val) {
  if (val < 0.0f) return 0.0f;
  if (val > 180.0f) return 180.0f;
  return val;
}

void applyJointLine(const String &line) {
  int idx = line.indexOf("JOINTS:");
  if (idx == -1) return;

  String payload = line.substring(idx + 7);
  int start = 0;
  while (start < payload.length()) {
    int comma = payload.indexOf(',', start);
    String token = (comma == -1) ? payload.substring(start) : payload.substring(start, comma);
    int eq = token.indexOf('=');
    if (eq != -1) {
      String jname = token.substring(0, eq);
      float deg = clampDeg(token.substring(eq + 1).toFloat());
      int pulse = (int)deg;

      if (jname == "joint1") servo1.write(pulse);
      else if (jname == "joint2") servo2.write(pulse);
      else if (jname == "joint3") servo3.write(pulse);
      else if (jname == "joint4") servo4.write(pulse);
    }
    if (comma == -1) break;
    start = comma + 1;
  }
}

void setup() {
  Serial.begin(115200);
  servo1.attach(PIN_SERVO1);
  servo2.attach(PIN_SERVO2);
  servo3.attach(PIN_SERVO3);
  servo4.attach(PIN_SERVO4);

  servo1.write(90);
  servo2.write(90);
  servo3.write(90);
  servo4.write(90);
}

void loop() {
  while (Serial.available() > 0) {
    char c = (char)Serial.read();
    if (c == '\n') {
      rxBuffer.trim();
      if (rxBuffer.length() > 0) {
        applyJointLine(rxBuffer);
      }
      rxBuffer = "";
    } else if (c != '\r') {
      rxBuffer += c;
    }
  }
}
