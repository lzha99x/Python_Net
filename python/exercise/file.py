#coding=utf-8
#!/usr/bin/python
fo = open("foo.txt", "wb")
print "Name of the file: ", fo.name
print "Closed or not : ", fo.closed
print "Opening mode : ", fo.mode
print "Softspace flag : ", fo.softspace
fo.close()
print "Closed or not : ", fo.closed
