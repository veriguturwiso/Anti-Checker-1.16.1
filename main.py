from time import sleep
from ahk import AHK
import os
from threading import Thread

ahk = AHK()

def read_file(file):
    with open(file, 'r') as f:
        read = f.read()
    return read

def write_to_file(file, what):
    with open(file, 'w') as f:
        f.truncate(0)
        f.write(what)

def ask_for_settings():
    logs = input('input your logs folder: ')
    return logs

# creating settings.txt if it doesn't exist
if os.path.isfile('settings.txt') == False:
    with open('settings.txt', 'w') as f:
        f.truncate(0)

# checking if settings.txt is empty
if os.stat('settings.txt').st_size == 0:
    # if it is, ask user for settings
    logs = ask_for_settings()
    write_to_file('settings.txt', logs)
else:
    # else, ask user if he wants to change settings
    to_change_settings = input('do you wanna change your logs path? (Y/N): ')
    if to_change_settings.upper() == 'Y':
        logs = ask_for_settings()
        write_to_file('settings.txt', logs)
    else:
        logs = read_file('settings.txt')

# checks if 'latest.log' exists in logs path
if os.path.isfile(f'{logs}\\latest.log'):
    log = f'{logs}\\latest.log'
else:
    print(f"latest.log doesn't exist in your logs path '{logs}' (you probably provided wrong path, restart the program)")

print("starting to check! (don't close this window)")

def warning():
    ahk.run_script('''
    MsgBox Don't try to check! (first and last warning)
    ''')

def close_game():
    ahk.run_script('''
    SetTitleMatchMode 2
    WinGet PID, PID, Minecraft
    Process, Close, %PID%
    ''')

def wait_for_minecraft():
    ahk.run_script('''
    SetTitleMatchMode 2
    WinWait Minecraft* 1.16
    ''')

while True:
    sleep(0.02)
    with open(log, 'r') as f:
        lines = f.readlines()
        last_line = lines[-1]
    if 'Local game hosted on port' in last_line:
        Thread(target=warning).start()
        while True:
            sleep(0.02)
            with open(log, 'r') as f:
                lines = f.readlines()
                last_line = lines[-1]
            if 'Set own game mode to Spectator Mode' in last_line or 'Set own game mode to Creative Mode' in last_line:
                # if user changes his gamemode to spectator or creative, close the game
                close_game()
                wait_for_minecraft()
                break
            if 'Stopping singleplayer server as player logged out' in last_line or 'Stopping worker threads' in last_line:
                # else if user quits the world, stop checking for spectator or creative
                break