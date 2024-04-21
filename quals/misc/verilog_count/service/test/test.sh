#!/bin/sh

# https://iverilog.fandom.com/wiki/Getting_Started
iverilog -o /tmp/verilog_test -s test -c file_list.txt
vvp /tmp/verilog_test > output.txt