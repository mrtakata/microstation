const int BUTTON = 2;
const int LED = 3;
int CURRENT_BUTTON_STATE = 0;
int PREVIOUS_BUTTON_STATE = 0;
int IS_LED_ON = 0;

void  setup()
{
  pinMode(BUTTON, INPUT);
  pinMode(LED, OUTPUT);
}

void  loop()
{
  CURRENT_BUTTON_STATE = digitalRead(BUTTON);
  if (CURRENT_BUTTON_STATE == HIGH && PREVIOUS_BUTTON_STATE == LOW)  // BUTTON PRESSED
  {
    PREVIOUS_BUTTON_STATE = HIGH;
  } 
  else if (CURRENT_BUTTON_STATE == LOW && PREVIOUS_BUTTON_STATE == HIGH)  // BUTTON RELEASED
  {
    PREVIOUS_BUTTON_STATE = LOW;
    if(IS_LED_ON){
      IS_LED_ON = 0;
      digitalWrite(LED, LOW);
    }
    else{
      IS_LED_ON = 1;
      digitalWrite(LED, HIGH);
    }
  }
}