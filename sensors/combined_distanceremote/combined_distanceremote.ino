//www.elegoo.com
//2016.12.9

#include "IRremote.h"

/*-----( Global Constants )-----*/
const int receiver = 9;      // Signal Pin of IR receiver to Arduino Digital Pin 11
String results_buffer = "NONE";
char serialData;

/* For Distance */
int trigPin = 3;
int echoPin = 2;
long duration;
long distance_cm; 


/*-----( Declare objects )-----*/
IRrecv irrecv(receiver);     // create instance of 'irrecv'
decode_results results;      // create instance of 'decode_results'

/*-----( Function )-----*/
void translateIR() {          // takes action based on IR code received
// describing Remote IR codes 

  switch(results.value){
    case 0xFFA25D: results_buffer = "POWER"; break;
    case 0xFFE21D: results_buffer = "FUNC/STOP"; break;
    case 0xFF629D: results_buffer = "VOL+"; break;
    case 0xFF22DD: results_buffer = "FAST BACK";    break;
    case 0xFF02FD: results_buffer = "PAUSE";    break;
    case 0xFFC23D: results_buffer = "FAST FORWARD";   break;
    case 0xFFE01F: results_buffer = "DOWN";    break;
    case 0xFFA857: results_buffer = "VOL-";    break;
    case 0xFF906F: results_buffer = "UP";    break;
    case 0xFF9867: results_buffer = "EQ";    break;
    case 0xFFB04F: results_buffer = "ST/REPT";    break;
    case 0xFF6897: results_buffer = "0";    break;
    case 0xFF30CF: results_buffer = "1";    break;
    case 0xFF18E7: results_buffer = "2";    break;
    case 0xFF7A85: results_buffer = "3";    break;
    case 0xFF10EF: results_buffer = "4";    break;
    case 0xFF38C7: results_buffer = "5";    break;
    case 0xFF5AA5: results_buffer = "6";    break;
    case 0xFF42BD: results_buffer = "7";    break;
    case 0xFF4AB5: results_buffer = "8";    break;
    case 0xFF52AD: results_buffer = "9";    break;
    case 0xFFFFFFFF: results_buffer = " REPEAT";break;  

  default: 
    results_buffer = " other button   ";

  }// End Case

} //END translateIR

void setup(){   /*----( SETUP: RUNS ONCE )----*/
  Serial.begin(9600);
  Serial.println("IR Receiver Button Decode"); 
  irrecv.enableIRIn();           // Start the receiver

  /* For Distance */
  pinMode(trigPin, OUTPUT); 
  pinMode(echoPin, INPUT);

}/*--(end setup )---*/

void loop(){   /*----( LOOP: RUNS CONSTANTLY )----*/
  if (irrecv.decode(&results))   // have we received an IR signal?
  {
    translateIR(); 
    irrecv.resume();            // receive the next value
  }
  else{
    digitalWrite(trigPin, LOW); 
   digitalWrite(trigPin, HIGH);
   digitalWrite(trigPin, LOW); 
   
   // Get timing (in microseconds) when the echo went high, then stop when it went low
   duration = pulseIn(echoPin, HIGH);
   
   //Sound travels 34300 cms every 100000 μs (microsecond)
   //That means that it moves 29 cm every 1 μs
   //Divide duration by 29, but then by half (because it's travelling from and to)
   distance_cm = duration / 29 / 2; 

   Serial.println(String(distance_cm) + "|" + results_buffer);
   Serial.flush();
   
    if (results_buffer != "NONE"){
      results_buffer = "NONE";
    }
    delay(100);
  }

}/* --(end main loop )-- */
