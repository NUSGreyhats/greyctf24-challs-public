#!/usr/bin/python3

import base64
import sys
import subprocess
import tempfile
import os
import shutil

# Replace this with the actual flag
FLAG = "grey{c0un71n6_w17h_r1pp13_4ddr5}"
BAD_WORDS = ['if', 'else', '?', '+']

CURR_DIR = os.getcwd()
def copy_and_run(verilog_code, directory_path='test'):
    output = None
    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()

    try:
        # Copy the directory into the temporary directory
        shutil.copytree(os.path.join(CURR_DIR, directory_path), os.path.join(temp_dir, os.path.basename(directory_path)))
        # Change the current working directory to the temporary directory
        os.chdir(os.path.join(temp_dir, directory_path))
        with open("solve.v", mode='w+') as f:
            f.write(verilog_code)
        # Run the shell script
        os.system('iverilog -o ./vt -s test -c file_list.txt')
        os.system('(vvp ./vt > output.txt )')
        with open('output.txt', 'r') as file:
            output = file.read().strip()
    except Exception as e:
        print(e)
    finally:
        # Cleanup: Remove the temporary directory and its contents
        shutil.rmtree(temp_dir)
        os.chdir(CURR_DIR)
        return output


def run_verilog_code(verilog_code):
    return copy_and_run(verilog_code)


def check_output(output, expected_output_file):
    with open(expected_output_file, 'r') as file:
        expected_output = file.read().strip()
    return output.strip() == expected_output

def main():
    try:
        # Receive Verilog code until 'END'
        enc_input = input("base64 encoded input: ")

        try:
            received_data = base64.b64decode(enc_input).decode()
        except:
            print("failed to decode input as base64 string")
            sys.exit(0)

        for word in BAD_WORDS:
            if word in received_data:
                print("Bad Words Detected")
                sys.exit(0)

        print("Received Verilog code!")

        # Run Verilog code
        output = run_verilog_code(received_data)

        # Check if output matches expected
        expected_output_file = 'expected_output.txt'
        if check_output(output, expected_output_file):
            print(f"Congratulations! Flag: {FLAG}")
        else:
            print("Output does not match expected.")

    finally:
        sys.exit(0)


main()
