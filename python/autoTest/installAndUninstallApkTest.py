from common import coreTest
import sys, string, os, time

dir = 'apkForTest'
# mCommand = r'adb shell logcat -d -s BackupManagerService | grep "PACKAGE_ADDED" | cut -d = -f 3'
mCommand = r'adb shell logcat -d -s BackupManagerService | grep "PACKAGE_ADDED"'

if len (sys.argv) != 2:
	print "eg: .py   device name = ?"
	sys.exit(0)
device_name = sys.argv[1]

# Open device with device name
deviceFd = coreTest.open_device(device_name)
if not deviceFd:
	print "Open Device Error: Can't find device"
# Get apk list.
file = os.listdir(dir)
for f in file:
	# dir/*.apk
	apkPath = dir +'/' + f
	# print apkPath
	coreTest.local_exec("adb shell logcat -c", 5)
	# Start install apk package
	coreTest.install_apk(deviceFd, apkPath)	
	(code, output) = coreTest.local_exec(mCommand, 5)
	# log = output.replace(" ","_")
	# print output
	log = output.replace(' ',':').split(':')
	# print log[10]
	# coreTest.get_package_name(log)
	time.sleep(1)
	# start remove apk package
	coreTest.uninstall_apk(deviceFd, log[10])

