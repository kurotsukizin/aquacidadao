#define PINO_FLUXO 27
#define PINO_LED 26

volatile unsigned long pulsos = 0;
unsigned long ultimoCiclo = 0;

void contarPulso() {
  pulsos++;
}

void setup() {
  Serial.begin(115200);
  pinMode(PINO_FLUXO, INPUT_PULLUP);
  pinMode(PINO_LED, OUTPUT);
  attachInterrupt(digitalPinToInterrupt(PINO_FLUXO), contarPulso, FALLING);
  Serial.println("AquaCidadao iniciado");
}

void loop() {
  unsigned long agora = millis();

  if (agora - ultimoCiclo < 60000) {
    return;
  }

  ultimoCiclo = agora;

  float litrosPorMinuto = pulsos * 2.25;
  float volumeLitros = litrosPorMinuto;
  bool alerta = volumeLitros > 10.0;

  digitalWrite(PINO_LED, alerta ? HIGH : LOW);

  Serial.printf("vazao_l_min=%.2f,volume_litros=%.2f,alerta=%d\n",
                litrosPorMinuto, volumeLitros, alerta ? 1 : 0);

  pulsos = 0;
}
