from common import coreTest
import sys, string, os, time

dir = 'apkForTest'


if len (sys.argv) != 2:
	print "eg: .py   device name = ?"
	sys.exit(0)
# apkPath = sys.argv[1]
device_name = sys.argv[1]

deviceFd = coreTest.open_device(device_name)
if not deviceFd:
	print "Open Device Error: Can't find device"
# (code, output) = coreTest.local_exec("adb shell logcat -s BackupManagerService", 5)
# print code, output
file = os.listdir(dir)
for f in file:
	apkPath = dir +'/' + f
	# print apkPath
	coreTest.install_apk(deviceFd, apkPath)	
	# time.sleep(3)
	# coreTest.uninstall_apk(deviceFd, "com.example.hello")

