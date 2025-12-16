#include <Servo.h>

Servo s1, s2, s3, s4;

int cur1 = 90, cur2 = 90, cur3 = 90, cur4 = 90;
int tgt1 = 90, tgt2 = 90, tgt3 = 90, tgt4 = 90;

const int STEP = 1;       // 작을수록 부드러움
const int DELAY_MS = 15; // 클수록 느림

int toServo(int logical) {
  return constrain(logical + 90, 0, 180);
}

void setup() {
  Serial.begin(9600);

  s1.attach(2);
  s2.attach(3);
  s3.attach(4);
  s4.attach(5);

  s1.write(90);
  s2.write(90);
  s3.write(90);
  s4.write(90);
}

void smoothMove(Servo &s, int &cur, int tgt) {
  if (cur < tgt) cur += STEP;
  else if (cur > tgt) cur -= STEP;

  s.write(cur);
}

void loop() {
  if (Serial.available()) {
    String data = Serial.readStringUntil('\n');

    int l1, l2, l3, l4;
    sscanf(data.c_str(), "%d,%d,%d,%d", &l1, &l2, &l3, &l4);

    tgt1 = toServo(l1);
    tgt2 = toServo(l2);
    tgt3 = toServo(l3);
    tgt4 = toServo(l4);
  }

  smoothMove(s1, cur1, tgt1);
  smoothMove(s2, cur2, tgt2);
  smoothMove(s3, cur3, tgt3);
  smoothMove(s4, cur4, tgt4);

  delay(DELAY_MS);
}
