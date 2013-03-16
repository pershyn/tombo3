'''
Created on Apr 11, 2012

Builds UI

@author: Mykhailo.Pershyn
'''
import os
import subprocess


commands = [
            ["pyrcc4", "-py3", "resources/icons.qrc", "-o", "icons_rc.py"],
            ["pyuic4", "-o", "settings_ui.py", "settings.ui"],
            ["pyuic4", "-o", "main_window_ui.py", "main_window.ui"]
           ]


def run_command(cmd):
    cmdtext = os.path.abspath(os.path.curdir) + "\\"
    for i in cmd:
        cmdtext += i + " "
    print(cmdtext)
    res = subprocess.call(cmd, shell=True)
    if res == 0:
        print("SUCCEEDED")
    else:
        print("FAILED")
    print("")


for cmd in commands:
    run_command(cmd)
