# Challenge Summary

simple q&a, answers can be googled

```c
int chall_qna(){
  HAL_Delay(1000);
  fastPrintString("Mini Trivia Quiz > \nWe'll be asking you a few simple questions relating to this board.\nPlease answer all in lowercase:\n—-----------------------------------------------------------------");
  if (
    qna("\nWhat is the microcontroller (MCU) chip used?", "stm32f103c8t6") &&
    qna("\nWhat is a popular development board using this MCU?", "bluepill") &&
    qna("\nWhat is the smallest SMD size of a resistor on the board?", "0603") &&
    qna("\nWhat company provides manufacturing of PCBs from $2 (please sponsor us)?", "jlcpcb") &&
    qna("\nWhat does HAL stand for?", "hardware abstraction layer") &&
    qna("\nWhat is the logic level (voltage) used in this board?", "3.3v") &&
    qna("\nWhat usb class are you using to communicate to this board?", "communications device class")
  ) {
    fastPrintString("\nCorrect! Here you get a flag -> grey{STM32_ExP3R1}\n");
    badge_state_set_unlock_status_bit(UNLOCK_BIT_YELLOWHAT);
  } else {
    fastPrintString("\nTry again\n");
  }
}
```

How to search for questions
1. Read off the chip label
2. Google `stm32f103c8t6` - https://stm32-base.org/boards/STM32F103C8T6-Blue-Pill.html - iterate through the combinations (space, no space)
3. Google `SMD resistor size` - have a list to spam
4. Google `$2 PCB` - jlcpcb.com
5. Google `STM32 HAL` - in 1 of the results
6. Google `STM32 Logic Level`
7. Google `USB Class` - https://www.usb.org/defined-class-codes - CDC - USB CDC

# Details

GreyCat has an existential crisis. Join it on it's journey of self discovery! Challenge 1.

# Author

Hackin7

# Hints

nil

# Flag

`grey{STM32_ExP3R1}`
