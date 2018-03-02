
#include <Servo.h>

int servoPins[] = {2, 3, 4, 5, 6, 7, 8, 9, 10, 11 , 12};//11
//const int numServos = sizeof(servoPins)/sizeof(int);
const int numServos =11 ;
Servo servos[numServos];

//temp
int pos=0;
String response;



void setup() {
Serial.begin(115200);
Serial.println("Ready");
for (int i=0; i <= numServos; i++) {
    servos[i].attach(servoPins[i]);
    servos[i].write(90);
    

}
}

void loop() {
  if (Serial.available() > 0){
    if (Serial.read()!='/') {
    for (int x = 0; x < numServos; x++) {
      //if (x== numServos-1)break;
      Serial.print("<x"+String(x)+">");
      
      pos =  Serial.parseInt();

      servos[x].write(pos);
      response = String(x)+"="+String(pos)+" / ";
      Serial.print(response);
  }}
  Serial.println();
  
  }
  //byte bytesReceived = Serial.readBytesUntil('.', rd, 5);
}
