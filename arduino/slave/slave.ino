#include <Wire.h>

#define SLAVE_ADDRESS 0x04
#define DATA_SIZE 8
#define CMD 255

byte data[DATA_SIZE];
void receiveData(int byteCount){
    byte flag;
    int i = 0;
    while(Wire.available()) {
        flag = Wire.read();
          Serial.println(flag);
        if( i == DATA_SIZE) {
            i %= DATA_SIZE;
            output(data);
        }
        if (flag != CMD){
            data[i] = flag;
            i ++;
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




