# Challenge Summary

connect 2 pads together as told by the badge

```c
void chall_hyper_glitch(){
    if (HAL_GPIO_ReadPin(GPIOB, GPIO_PIN_15) == 0){
        usbPrintf(MAX_BUF_LEN, "grey{d3Bu9_P4D5}");
        badge_state_set_unlock_status_bit(UNLOCK_BIT_REDHAT); 
    }else{
        usbPrintf(MAX_BUF_LEN, "Connect PB15 to GND");
    }
}
```

# Details

GreyCat is short. Help it short something! Challenge 2.

# Author

Hackin7

# Hints

nil

# Flag

`grey{d3Bu9_P4D5}`
