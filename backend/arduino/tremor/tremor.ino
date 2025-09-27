#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>

Adafruit_MPU6050 mpu;

float gyro_x_offset = 0;
float gyro_y_offset = 0;
float gyro_z_offset = 0;

const float TREMOR_THRESHOLD = 0.8; // Ajuste este valor conforme a necessidade
const int UPDATE_INTERVAL = 1500; // << MUDANÇA AQUI: 1500ms = 1.5 segundos

unsigned long last_update_time = 0;
int peak_count = 0;
float hertz = 0;
bool peak_detected_flag = false;

void setup(void)
{
  Serial.begin(115200);

  if (!mpu.begin())
  {
    Serial.println("{\"erro\":\"Falha ao encontrar o chip MPU6050\"}");
    while (1)
      delay(10);
  }

  mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
  mpu.setGyroRange(MPU6050_RANGE_250_DEG);
  mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);

  delay(1000); 
  calibrarSensor();
  delay(1000);
  last_update_time = millis();
}

void calibrarSensor()
{
  long gyro_x_cal = 0, gyro_y_cal = 0, gyro_z_cal = 0;
  int num_leituras = 1000;
  for (int i = 0; i < num_leituras; i++)
  {
    sensors_event_t a, g, temp;
    mpu.getEvent(&a, &g, &temp);
    gyro_x_cal += g.gyro.x;
    gyro_y_cal += g.gyro.y;
    gyro_z_cal += g.gyro.z;
    delay(3);
  }
  gyro_x_offset = (float)gyro_x_cal / num_leituras;
  gyro_y_offset = (float)gyro_y_cal / num_leituras;
  gyro_z_offset = (float)gyro_z_cal / num_leituras;
}

void loop()
{
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);

  float gyro_x_calibrado = g.gyro.x - gyro_x_offset;
  float gyro_y_calibrado = g.gyro.y - gyro_y_offset;
  float gyro_z_calibrado = g.gyro.z - gyro_z_offset;

  float magnitude_giro = sqrt(sq(gyro_x_calibrado) + sq(gyro_y_calibrado) + sq(gyro_z_calibrado));

  if (magnitude_giro > TREMOR_THRESHOLD && !peak_detected_flag)
  {
    peak_count++;
    peak_detected_flag = true;
  }
  else if (magnitude_giro < TREMOR_THRESHOLD)
  {
    peak_detected_flag = false;
  }

  unsigned long current_time = millis();
  if (current_time - last_update_time >= UPDATE_INTERVAL)
  {
    float segundos = (float)UPDATE_INTERVAL / 1000.0;
    hertz = (float)peak_count / segundos;

    String json = "{\"frequencia\": " + String(hertz) + "}";
    Serial.println(json);

    peak_count = 0;
    last_update_time = current_time;
  }
}