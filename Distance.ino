#include <Wire.h>
#include <Adafruit_VL53L0X.h>


Adafruit_VL53L0X lox = Adafruit_VL53L0X();

void setup() {
  // Initial setup
  Serial.begin(115200);
  while (!Serial) {
    delay(1); // wait for connection
  }

  Serial.println("VL53L0X Test");

  //Sensor Initialization
  if (!lox.begin()) {
    Serial.println("Failed to boot VL53L0X");
    while (1);
  }
  Serial.println("VL53L0X booted");
}

void loop() {
  VL53L0X_RangingMeasurementData_t measure;

  // Read the Value
  lox.rangingTest(&measure, false); // false: not using the long distance function

  if (measure.RangeStatus != 4) {  // 4 = measurement fail
    Serial.println(measure.RangeMilliMeter);
  } else {
    Serial.println("Out of range");
  }

  delay(100); // reduce reading frequency
}
