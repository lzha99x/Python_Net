#!/usr/bin/python
from common import coreTest
import sys, string, os, time



(exec_status, outpue) = coreTest.local_exec("adb logcat -c", 5)
print exec_status, outpue
time.sleep(3)
(exec_status, outpue) = coreTest.local_exec("adb logcat -d -s ServiceState", 5)
print exec_status, outpue

