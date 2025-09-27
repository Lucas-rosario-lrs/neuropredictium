// Incluindo as bibliotecas necessárias
#include <Wire.h>
#include <Adafruit_SSD1306.h>
#include "Adafruit_TCS34725.h"

// Configurando e criando os objetos para o sensor e o display
Adafruit_TCS34725 sensTCS = Adafruit_TCS34725(TCS34725_INTEGRATIONTIME_300MS, TCS34725_GAIN_1X);
Adafruit_SSD1306 display(-1);

void setup()
{
  // Inicia a comunicação Serial para enviar os dados JSON
  Serial.begin(9600);

  // Inicia o display
  display.begin(SSD1306_SWITCHCAPVCC, 0x3C);

  // Inicia o sensor e verifica a conexão
  if (!sensTCS.begin())
  {
    Serial.println("{\"erro\":\"Sensor de cor nao encontrado\"}");
    while (1)
      ;
  }

  // Limpa o display no início
  display.clearDisplay();
  display.display();
}

void loop()
{
  // << MUDANÇA >> Adicionamos as variáveis TempCor e LUX de volta
  uint16_t r, g, b, c, TempCor, LUX;
  String corDetectada = "Indefinido";

  // Faz a leitura dos dados brutos do sensor
  sensTCS.getRawData(&r, &g, &b, &c);

  // FUNCAO PRA CALCULOS
  TempCor = sensTCS.calculateColorTemperature(r, g, b);
  LUX = sensTCS.calculateLux(r, g, b);

  // --- LÓGICA DE DETECÇÃO DE COR ---
  if (c > 250)
  {
    if (r > b && r > g)
    {
      corDetectada = "Vermelho";
    }
    else if (g > r && g > b)
    {
      corDetectada = "Verde";
    }
    else if (b > r && b > g)
    {
      corDetectada = "Azul";
    }
  }

  // --- BLOCO PARA ATUALIZAR O DISPLAY PARAMOS DE USAR O DISPLAY ---
  display.clearDisplay();
  display.setTextSize(2);
  display.setTextColor(WHITE);
  if (corDetectada == "Vermelho")
    display.setCursor(15, 8);
  else if (corDetectada == "Verde")
    display.setCursor(25, 8);
  else if (corDetectada == "Azul")
    display.setCursor(30, 8);
  else
    display.setCursor(5, 8);
  display.println(corDetectada);
  display.display();

  // =================================================================
  //  PACOTE JSON AGORA
  // =================================================================
  String json = "{\"r\":" + String(r) +
                ",\"g\":" + String(g) +
                ",\"b\":" + String(b) +
                ",\"c\":" + String(c) +
                ",\"corDetectada\":\"" + corDetectada + "\"" + // << Adicionado
                ",\"tempCor\":" + String(TempCor) +            // << Adicionado
                ",\"lux\":" + String(LUX) + "}";               // << Adicionado

  // Envia a string JSON completa pela porta serial
  Serial.println(json);
  // =================================================================

  // Delay para simular a troca de uma amostra de saliva
  delay(2000);
}