
import os, sys

f = open(sys.argv[1], 'r')

lines = f.readlines()
newLines = []

for l in lines:
	if l[0:2] == 'vt':
		s = l.split()
		newLines.append('v ' + str(s[1]) + ' ' + str(s[2]) + ' 0.0' + '\n')
	if l[0] == 'f':
		s = l.split()
		s1 = s[1].split('/')[1]
		s2 = s[2].split('/')[1]
		s3 = s[3].split('/')[1]
		newLines.append('f ' + str(s1) + ' ' + str(s2) + ' ' + str(s3) + '\n')
		
fout = open(sys.argv[2], 'w')
fout.write(''.join(newLines))
