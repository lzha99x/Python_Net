from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice
from com.android.monkeyrunner.easy import By
from com.android.chimpchat.hierarchyviewer import HierarchyViewer
import time
import sys
import os, signal
import subprocess
import re

FAILURE = -1
SUCCESS = 0
TAG = "Camera_test"
mCount = int(0)


def open_device(device_name):
    device = MonkeyRunner.waitForConnection(5,device_name)
    return device

def get_hierarchy_view(device):
    result = device.getHierarchyViewer()
    result = device.getRootView()
    print result

def start_camera(device):
    package = 'com.android.camera2'
    activity= 'com.android.camera.CameraLauncher'
    runComponent = package + '/' + activity

    device.startActivity(component=runComponent)

def close_camera(device):
    device.press('KEYCODE_BACK','DOWN_AND_UP')


def take_action(device):
    device.press('KEYCODE_CAMERA','DOWN_AND_UP')


#    press_button(deviceHandle,"id/on_screen_indicators")
def press_button(device,id):
    pointButton = get_button_viewer(device,id)
    device.touch(int(pointButton.x),int(pointButton.y),"DOWN_AND_UP")

def get_button_viewer(device,id):
    hierarchyViewer = device.getHierarchyViewer()
#    viewNodeButton  = hierarchyViewer.findViewById("id/on_screen_indicators")
    viewNodeButton  = hierarchyViewer.findViewById(id)
    pointButton = hierarchyViewer.getAbsoluteCenterOfView(viewNodeButton)
    print pointButton
    return pointButton
#    device.touch(int(pointButton.x),int(pointButton.y),"DOWN_AND_UP")

def drag_touch(device):
    device.drag((626,584),(720,500),0.1,4)

#----------------------------------------------------------------#
def test_fail(device_name):
    log_path = "./log"+ "/" + device_name + "_" + TAG +"_"+ time.ctime() + ".log"
    log_file = log_path.replace(" ","_").replace(":","_")
    # print log_file
    time.sleep(1)
    os.system("adb -s %s logcat -d > %s" % (device_name,log_file))

#----------------------------------------------------------------#
def install_apk(device,apkPath):
    res = device.installPackage(apkPath)
    log = "Install %s " % apkPath
    if not res:
        print_log(log,'fail')
    else:
        print_log(log,'pass')

#----------------------------------------------------------------#
def uninstall_apk(device, apkPath):
    res = device.removePackage(apkPath)
    log = "uninstall %s" % apkPath
    if not res:
        print_log(log, 'fail')
    else:
        print_log(log, 'pass')

#----------------------------------------------------------------#
def print_log(log, flag):
    if 'pass' in flag:
        print log ,"\033[;32;40m Pass \033[0m"
    elif 'fail' in flag:
        print "\033[;31;40m Fail \033[0m"

#----------------------------------------------------------------#
def local_exec(command, timeout):
    def timeout_end(signum, frame):
        print "ERROR : *** TIMEOUT ***"
        p.terminate()
        return FAILURE

    # Create signal alarm
    signal.signal(signal.SIGALRM, timeout_end)
    signal.alarm(timeout)

    # start
    output = ""
    log = "local_exec()"
    p = subprocess.Popen(command.split(), 
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    # while process is runing
    while p.poll() is None:
        # Loop output
        for line in iter(p.stdout.readline, ''):
            output += line + '\r\n'
            for l in line.rstrip("\r\n").replace("\r", "").split("\n"):
                # print log, l
                pass

    # Check return code
    signal.alarm(0)
    code = p.returncode
    if code != 0:
        print "Command Fail"

    return code ,output.rstrip("\r\n")

#----------------------------------------------------------------#
# TODO: Don't work
def get_package_name(string):
    pattern =   re.compile(string)
    match   =   pattern.match('package:')
    print "pattern ",match.group()
    if match:
        print match.group()
    else:
        print "Match fail!!"
#----------------------------------------------------------------#

def Camera_test():
    if len(sys.argv) != 3:
        print "eg: .py loop=?  device name = ?"
        sys.exit(1)
    (loop) = int(sys.argv[1])
    device_name = sys.argv[2]
    global mCount
    deviceHandle = open_device(device_name)
    if not deviceHandle:
        print "can't find device!!"
        sys.exit(1)
    else:
        print "-----Start  %s--time: %s---" % (TAG, time.ctime())

    close_camera(deviceHandle)
    time.sleep(2)
    start_camera(deviceHandle)
    time.sleep(2)
#    get_hierarchy_view(deviceHandle)
    while loop > 0:
        try:
            time.sleep(2)
            take_action(deviceHandle)
            time.sleep(2)
            take_action(deviceHandle)
            time.sleep(4)
            drag_touch(deviceHandle)
            mCount = mCount + 1
            loop = loop - 1
        except:
            print "Error ++++loop= [%d]+++++++ fail" % mCount
            test_fail(device_name)
            sys.exit(0)
    print "-----End---Passed=%d--Completed time=%s" % (mCount, time.ctime())
# if __name__ == "__main__":
# #    Camera_test()
