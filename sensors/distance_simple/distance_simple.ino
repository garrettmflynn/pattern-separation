//The trigger sends a ping (signal). This will be an output in our setup
int trigPin = 3;

//The echo listens for the returning signal. This will be an input in our setup
int echoPin = 2;

//Keep track of the time it takes for the ping to go and come back (using pulseIn)
long duration;

//Convert that time to cm
long distance_cm; 

void setup() {
 Serial.begin (9600); 
 pinMode(trigPin, OUTPUT); 
 pinMode(echoPin, INPUT);
}

void loop() {
 digitalWrite(trigPin, LOW); 
 digitalWrite(trigPin, HIGH);
 digitalWrite(trigPin, LOW); 
 
 // Get timing (in microseconds) when the echo went high, then stop when it went low
 duration = pulseIn(echoPin, HIGH);
 
 //Sound travels 34300 cms every 100000 μs (microsecond)
 //That means that it moves 29 cm every 1 μs
 //Divide duration by 29, but then by half (because it's travelling from and to)
 distance_cm = duration / 29 / 2; 
 
 Serial.print(distance_cm);
 Serial.println();
 delay(100);
}
