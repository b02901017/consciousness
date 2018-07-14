#include <Wire.h>

#define SLAVE_ADDRESS 0x06
#define DATA_SIZE 10
#define CMD 255

byte data[DATA_SIZE] = {0,0,0,0,0,0,0,0,0,0};
void receiveData(){
    byte flag;
    int i = 0;
    while(Wire.available()) {
        flag = Wire.read();
        i %= DATA_SIZE;
        if (flag != CMD){
            Serial.print(i);
            Serial.print(",");
            Serial.print(flag);
            Serial.print(",");
            data[i] = flag;
            i ++;
        } else {
            output(data);
            Serial.println("accept");
        }

    }
}

void initPin(){
    for (int i = 0; i < DATA_SIZE; i++) {
        pinMode(i+2, OUTPUT);
    }
}

void output(byte *data) {
    for (int i = 0; i < DATA_SIZE; i++) {
      digitalWrite(i+2, data[i]);
   } 
}

void setup(void) {
    initPin();
    Serial.begin(9600);
    Wire.begin(SLAVE_ADDRESS);
    Wire.onReceive(receiveData);
    Serial.println("Ready!");
}

void loop(void) {


}




