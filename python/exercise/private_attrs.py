#conding=utf-8
#!/usr/bin/python

class JustConter:
	__secretCount	= 0
	publicCount		= 0

	def count(self):
		self.__secretCount += 1
		self.publicCount +=1
		print self.__secretCount


conter = JustConter()
conter.count()
conter.count()
conter._JustConter__secretCount += 1
print conter.publicCount
print dir(conter)
# print conter.__secretCount
print conter._JustConter__secretCount