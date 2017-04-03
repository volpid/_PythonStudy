#!/usr/bin/python3
#-*- coding=utf8 -*-

"""
	Get longest bytes in two Byte in Array
"""
#############################################################################
def GetCommonString(s1, s2) :
	M = [[0] * len(s2) for _ in range(len(s1))]	
	xpos = 0
	maxLength = 0

	for x in range(len(s1)) :
		for y in range(len(s2)) :
			if s1[x] == s2[y] :
				prevValue = 0
				if (x > 0) and (y > 0) :
					prevValue = M[x - 1][y - 1]
				M[x][y] = prevValue + 1

				if M[x][y] > maxLength : 
					maxLength = M[x][y]
					xpos = x

	LCBs = []
	for i in range(maxLength) :
		LCBs.insert(0, s1[xpos - i])

	return LCBs

#############################################################################
def DoMainTest():
	S1='''GET /http.html Http1.1

Host: www.http.header.free.fr

Accept: image/gif, image/x-xbitmap, image/jpeg, image/pjpeg,

Accept-Language: Fr

Accept-Encoding: gzip, deflate

User-Agent: Mozilla/4.0 (compatible MSIE 5.5 Windows NT 4.0)

Connection: Keep-Alive

'''

	S2='''GET / Http1.0

Connection: Keep-Alive

User-Agent: Mozilla/4.7 [Fr] (Win98 I)

Host: www.yahoo.fr

Accept-Charset: iso-8859-1,*,utf-8

Accept-Encoding: gzip

Accept: image/gif, image/x-xbitmap, image/jpeg, image/pjpeg, image/png, 

Accept-Language: Fr

'''
	LCBs = GetCommonString(S1, S2)
	print(''.join(LCBs))

if __name__ == "__main__" :
	DoMainTest()
