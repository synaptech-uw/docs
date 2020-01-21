

#include "lab.h"
#include <stdint.h>

double temp;
int x = 0;
int main()
{
  reset_clk();
  switch_control_set();
  onboard_led_start();  
  GPIO_b4_analog();
  fast_timer_start();
  onboard_switches_interrupt_enable();
  
  UART_Init();
  
  ADC_Analog_Init();
  ADC_interrupt_enable();
  

   while(1)
   {
     led_data = 0;
   }
   return 1;
}


//Triggers every cycle according to a timer
void ADC_SS3_Handler(void)
{  
  temp = (ADC_FIFO3 * (3.3 / 40960)); //Converts value from ADC into voltage
  
  //Determines the value to put into the led_data register 
  UART_Print(temp);

  ADC_interrupt_clear();

}
  
void Port_F_Handler(void)
{
  
  //Switches the system clock and the timer's load according to which switch was pressed
  if(switch1 == 0)
  {
    timer_off();
    reset_clk();
    UART_Print(16);
    fast_timer_start();
    
    delay
    port_f_clear_interrupt();
  }else if(switch2 == 0)
  {
    timer_off();
    set_clk_80MHz();
    UART_Print(80);
    fast_timer_start();

    delay
    port_f_clear_interrupt();
  }
  
}

