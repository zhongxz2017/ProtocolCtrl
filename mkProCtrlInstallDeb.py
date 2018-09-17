#! /usr/bin/python3
# _*_ coding: UTF-8 _*_ 
# Filename: startGUI.py

import os
import py_compile

proCtrlVersion = 'v5.1.14'
pkgDir = 'ProtocolCtrl'
pkgDes = 'Auto-Tour'
debPkg = pkgDir + '-' + pkgDes + '-' + proCtrlVersion + '.deb'

dpkgCmd = 'dpkg -b ' + pkgDir + '/ ' + debPkg
print (dpkgCmd)

try:
	py_compile.compile(r'./ProtocolCtrl2.py')
	cpPyc = 'cp ./ProtocolCtrl2.pyc ./ProtocolCtrl/etc/aqueti/ProtocolCtrl'
	print cpPyc
	os.system(cpPyc)
	os.system(dpkgCmd)
	print ('create deb package success.')
except OSError:
	print ('create deb package failed, cmd string is ' + debPkg)
