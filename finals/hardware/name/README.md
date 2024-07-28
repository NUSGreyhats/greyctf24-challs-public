# Challenge Summary

understand that stm32 uses printf, and `%s` to read the flag

```c
void chall_name(){
    volatile char flag[128] = "grey{you_can_printf_on_stm32?}";
    usbPrintf(MAX_BUF_LEN, "\nEnter your name> ");
    
    char input_ans[STATE_NAME_SIZE];
    memset(input_ans, 0, STATE_NAME_SIZE);
    int ans_len = readString(input_ans, STATE_NAME_SIZE-1);
    input_ans[ans_len] = '\0';
    
    usbPrintf(MAX_BUF_LEN, input_ans, flag);
    usbPrintf(MAX_BUF_LEN, "\n");
    
    if (strstr(input_ans, "%s") != NULL) {
        badge_state_set_unlock_status_bit(UNLOCK_BIT_BLUEHAT);
    }

    oled_update_name(input_ans);
    badge_state_update_name(input_ans);

    usbPrintf(MAX_BUF_LEN, "Updated!\n");
}
```

# Details

GreyCat has an onboard screen where it can communicate with others. Hmm I wonder if there's some special format? Challenge 3.

# Author

Hackin7

# Hints

nil

# Flag

`grey{you_can_printf_on_stm32?}`
