#! /usr/bin/env python
# _*_ coding: UTF-8 _*_ 
# Filename: ProtocolCtrl.py

import os
from Tkinter import *
import ttk
import webbrowser
import tkFileDialog
import tkSimpleDialog
import socket, traceback

# onvif cmd para define
onvifDict = {
	'onvifBin' : 'mantisONVIFServer',
	'rtspIpAddr' : '',
	'rtspPort' : '17100',
	'onvifPort' : '21100',
	'HW1080P'	: '1080 * 1920',
	'HW4K'		: '2160 * 3840',
	'HWCustom'	: 'high * width',
	'onvifLogoFile' : './logo/onvifLogo.png',
	'tourDefault'	: "2, (0 / 1 / 1.2)",
	'PTZLeft'	: './logo/left.png',
	'PTZRight'	: './logo/right.png',
	'PTZUp'		: './logo/up.png',
	'PTZDown'	: './logo/down.png',
	'PTZIn'		: './logo/ZoomIn.png',
	'PTZOut'	: './logo/ZoomOut.png',
	'PTZStop'	: './logo/stop.png',
	'PTZHome'	: './logo/home.png',
	'Play'		: './logo/play.png'
	}

# 28181 cmd/cfg para define
gbCfgList = ('server_id', 'server_ip', 'server_port', 'device_id', 'listen_port', 'username', 'password', 'alarm_id', 'media_id', 'register_expire')
gbDict =  {
	'gbCfgFileName' : '/etc/aqueti/GB/mantisGBprofile.conf',
	'gbCfgFileDir' : '/etc/aqueti/GB/',
	'gbBin' : 'mantisGBclient',
	'gbLogoFile' : './logo/gb28181Logo.png'
	}

gbCfgFilePrefix = '{\n  "keepalive_timeout":10,\n  "re-register_timeout":60,\n  "keepalive_timeout_num":3,\n  "user_profile":{\n'
gbCfgFileSuffix ='  }\n}'

# modle
modelDict = {
	'modleLogoFile' : './logo/modelCtrl.png',
	'DefModelPath'	: '/etc/aqueti/modelgen/',
	'RenderServer'	: 'aqt://Aqueti148',
	'NickName'		: '233',
	'ModelFile'		: 'model.json',
	'ModelEdit'		: 'model_edited.json',
	'CustomModel'	: 'model_custom.json',
	'ModelPagoda'	: 'model_pagoda.json',
	'ModelPanoLH'	: 'model_panorama_lh.json',
	'ModelPanoFH'	: 'model_panorama_fh.json'
	}

simpleDialogDict = {
	'pagoda'	: '',
	'panoLH'	: '',
	'panoFH'	: '',
	'custom'	: '',
	'InitModel'	: '恢复模型到初始状态\n1.删除用户定义的模型文件\n2.时间戳信息不会还原\n',
}

helpDocDict = {
	'onvifHelp' : './help/接入协议控制(ONVIF)用户指南' + '.docx',
	'gb28181Help' : './help/Mantis_ONVIF_help' + '.docx',
	}

LisenceNotice = '''***************************************************************************************
 *
 *  IMPORTANT: READ BEFORE DOWNLOADING, COPYING, INSTALLING OR USING.
 *
 *  By downloading, copying, installing or using the software you agree to this license.
 *  If you do not agree to this license, do not download, install, copy or use the software.
 *
 *  Copyright (C) 2018, Aqueti Inc, all rights reserved.
 *
 *  Redistribution and use in binary forms, with or without modification, are permitted.
 *
 *  Unless required by applicable law or agreed to in writing, software distributed
 *  under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
 *  CONDITIONS OF ANY KIND, either express or implied. See the License for the specific
 *  language governing permissions and limitations under the License.
 *
****************************************************************************************'''

FunctionNotice = '''***************************************************************************************
 *
 * ONVIF
 * 	1. Set onvif start parameter
 *	2. Start onvif
 *	3. Reinstall onvif
 * Tour
 *	1. CFG preset stay time
 *	2. Start/Stop Tour
 * MODEL
 *	1. Select model file
 *	2. Modify model file
 * GB28181 Hide
 *	1. Modify gb28181 config
 *	2. Update gb28181 config
 *	3. Start gb28181
 *
****************************************************************************************'''

ContactNotice = '''***************************************************************************************
 *
 * Lynn, Zhong
 * 2018-09-10
 * xiaozhen.zhong@aqueti.com
 *
****************************************************************************************'''


root = Tk()
#root.geometry('450x400')
root.resizable(True, False)
root.attributes("-alpha",0.6)
#1 title
root.title('ProtocolCtrl-Auto-Tour v5.１.13')

#2 meun
def quit_window():
	root.quit()
	root.destroy()
	exit()
	
def click_help_onvif():
	top = Toplevel()
	top.title('ONVIF user manual')
	Label(top, text='\nPlease check the protocol user manual.\nContact information of software team:li.min@aqueti.com.\n').pack()
	webbrowser.open(helpDocDict['onvifHelp'])

def click_help_gb28181():
	top = Toplevel()
	top.title('GB28181 user manual')
	Label(top, text='\nPlease check the protocol user manual.\nContact information of software team:li.min@aqueti.com.\n').pack()
	webbrowser.open(helpDocDict['gb28181Help'])

def click_about_me():
	top = Toplevel()
	top.title("About Me")
	LicenseFrame = LabelFrame(top, text=' Permission statement ', fg = 'green')
	LicenseFrame.grid(row=0, column=0, padx=10, pady=5)
	Label(LicenseFrame, text = LisenceNotice, wraplength = 720, justify = 'left').grid(row = 0, column = 0, padx=10, pady=5)
	FunctionFrame = LabelFrame(top, text=' Software Features  ', fg = 'green')
	FunctionFrame.grid(row=1, column=0, padx=10, pady=5)
	Label(FunctionFrame, text = FunctionNotice, wraplength = 720, justify = 'left').grid(row = 0, column = 0, padx=10, pady=5)
	ContactFrame = LabelFrame(top, text=' Contact Us ', fg = 'green')
	ContactFrame.grid(row=2, column=0, padx=10, pady=5)
	Label(ContactFrame, text = ContactNotice, wraplength = 720, justify = 'left').grid(row = 0, column = 0, padx=10, pady=5)

def click_start_onvif(sudo, rip, rp, op, enc, res, show, render, nn, record):
	print "click_start_onvif", sudo, rip, rp, op, enc, res, show, render, nn, record

	if sudo:
		start_onvif_commad = 'sudo ' + onvifDict['onvifBin']
	else:
		start_onvif_commad = onvifDict['onvifBin']
	if '' == rip.strip():
		start_onvif_commad += ' -rip ' + onvifDict['rtspIpAddr']
	else:
		start_onvif_commad += ' -rip ' + rip
	if '' == rp.strip():
		start_onvif_commad += ' -rp ' + onvifDict['rtspPort']
	else:
		start_onvif_commad += ' -rp ' + rp
	if '' != op.strip():
		start_onvif_commad += ' -op ' + op
	if 'h264' == enc.strip():
		start_onvif_commad += ' -h264'
	elif 'JPEG' == enc.strip():
		start_onvif_commad += ' -JPEG'
	else:
		start_onvif_commad += ' -h265'
	if '0: normal' == show.strip():
		start_onvif_commad += ' -Show 0'
	elif '1: indicate' == show.strip():
		start_onvif_commad += ' -Show 1'
	else:
		start_onvif_commad += ' -Show 2'
	if onvifDict['HW1080P'] == res.strip():
		start_onvif_commad += ' -res 1080 1920'
	elif onvifDict['HW4K'] == res.strip():
		start_onvif_commad += ' -res 2160 3840'
	else:
		start_onvif_commad += ' -res '
		start_onvif_commad += res.split('*')[0].strip()
		start_onvif_commad += ' '
		start_onvif_commad += res.split('*')[1].strip()
	if '' != render.strip():
		start_onvif_commad += ' -Render ' + render
	if '' != nn.strip():
		start_onvif_commad += ' -NickName ' + nn
	start_onvif_commad += ' -Record '
	if record:
		start_onvif_commad += '1'
	else:
		start_onvif_commad += '0'
	start_onvif_commad += ' &'

	print ('Start onvifServer CMD [' + start_onvif_commad + "]")
	# start onvifServer
	if os.system(start_onvif_commad) == 0:
		print 'Successful START onvifServer on', start_onvif_commad
	else:
		print 'START onvifServer Completed'
def reInstall_onvif():
	print os.system("pwd");
	rebuild_commad = 'sudo dpkg -r mantis_onvifserver;'
#	rebuild_commad += 'make ONVIFServer;'
	rebuild_commad += 'sudo dpkg -i ./mantis_ONVIFServer-*_.deb'
	
	# start onvifServer
	if os.system(rebuild_commad) == 0:
		print 'Successful ReInstall onvifServer on', rebuild_commad
	else:
		print 'ReInstall onvifServer Completed'

def selectPath():
	path_ = tkFileDialog.askopenfilename()
	path.set(path_)

def popSimpleDialog(level, hintStr):
	userStr = hintStr + "Only Enter [OK] to take effect."
	rsp = tkSimpleDialog.askstring(level, userStr)
	if 'OK' != rsp:
		return False
	return True

def recovery_model(dirpath):
	try:
		if False == popSimpleDialog("NOTICE", simpleDialogDict['InitModel']):
			print "User cancel the action"
			return
		if not(os.path.isdir(dirpath)):
			print (" Err: Invalid path dir " + dirpath)
			return
		recModel = dirpath + '/' + modelDict['ModelPagoda']
		if os.path.isfile(recModel):
			rmCmd = 'rm -r ' + recModel
			print rmCmd
			os.system(rmCmd)
		recModel = dirpath + '/' + modelDict['ModelPanoLH']
		if os.path.isfile(recModel):
			rmCmd = 'rm -r ' + recModel
			print rmCmd
			os.system(rmCmd)
		recModel = dirpath + '/' + modelDict['ModelPanoFH']
		if os.path.isfile(recModel):
			rmCmd = 'rm -r ' + recModel
			print rmCmd
			os.system(rmCmd)
		recModel = dirpath + '/' + modelDict['CustomModel']
		if os.path.isfile(recModel):
			rmCmd = 'rm -r ' + recModel
			print rmCmd
			os.system(rmCmd)
	except OSError:
		print ("Delete user define modelFile failed.")
    	return


def custom_model_cfg(dirpath, saveAs):
	try:
		if not(os.path.isdir(dirpath)):
			print (" Err: Invalid path dir " + dirpath)
			return
		initModel = dirpath + '/' + modelDict['ModelEdit']
		customModel = dirpath + '/'
		if 'pagoda' == saveAs.strip():
			customModel += modelDict['ModelPagoda']
		elif 'panorama LH' == saveAs.strip():
			customModel +=  modelDict['ModelPanoLH']
		elif 'panorama FH' == saveAs.strip():
			customModel += modelDict['ModelPanoFH']
		else:
			customModel += modelDict['CustomModel']
		if not(os.path.isfile(customModel)):
			cpModel = 'cp ' +  initModel + ' ' + customModel
			os.system(cpModel)
		customCmd = "geany " + customModel
		os.system(customCmd)
		key = 'timestamp'
		with open(customModel, "r") as f:
			for line in f:
				if key in line:
					print eval(line.split(':')[1].strip())
					defTS.set(eval(line.split(':')[1].strip()))
					break
	except OSError:
		print ("custom modelFile ", dirpath, " abnormal.")
    	return

def StartModelEditor():
	try:
		print ('Start ModelEditor base on Cur Model.')
		ModelEditorCmd = 'ModelEditor'
		os.system(ModelEditorCmd)
	except OSError:
		print ('Err: start ModelEditor tool failed, maybe reinstall the tool.')
		return

def StartModelAdder(dirpath, nickname, saveAs):
	try:
		if not(os.path.isdir(dirpath)):
			print (" Err: Invalid path dir " + dirpath)
			return
		modelFile = ""
		if 'pagoda' == saveAs.strip():
			modelFile = modelDict['ModelPagoda']
		elif 'panorama LH' == saveAs.strip():
			modelFile =  modelDict['ModelPanoLH']
		elif 'panorama FH' == saveAs.strip():
			modelFile = modelDict['ModelPanoFH']
		else:
			modelFile = modelDict['CustomModel']
		customModel = dirpath + '/' + modelFile
		print ('Select ModelFile: ' + customModel)
		defTS.set(update_max_timestamp(dirpath, modelFile));
		addertModelCmd = 'ModelAdder ' + nickname + ' ' + customModel
		print ('ModerAdder Cmd[' + addertModelCmd + ']')
		os.system(addertModelCmd)
	except OSError:
		print ('Err: start ModelAdder tool failed, please check nickname, maybe reinstall the tool.')
		return

def update_max_timestamp(dirpath, modelFile):
	CurFileName = dirpath + '/' + modelFile
	fileName = dirpath + '/' + modelDict['ModelEdit']
	key = 'timestamp'
	curTimeStamp = "0"
	maxTimeStamp = "0"
	if os.path.isfile(CurFileName):
		with open(CurFileName, "r") as f:
			for line in f:
				if key in line:
					curTimeStamp = eval(line.split(':')[1].strip())
					print "TimeStamp in", CurFileName, curTimeStamp
					break
	else:
		print "Invalid dir path or file name",  CurFileName
		return maxTimeStamp
	maxTimeStamp = curTimeStamp
	if os.path.isfile(fileName):
		fileData = ""
		with open(fileName, "r") as f:
			for line in f:
				if key in line:
					oldStr = eval(line.split(':')[1].strip())
					if int(oldStr) > int(curTimeStamp):
						curTimeStamp = oldStr
					maxTimeStamp = str(int(curTimeStamp) + 1)
					line = line.replace(oldStr, maxTimeStamp)
				fileData += line
		with open(fileName, "w") as f:
			f.write(fileData)
	fileData = ""
	with open(CurFileName, "r") as f:
		for line in f:
			if key in line:
				curTimeStamp = eval(line.split(':')[1].strip())
				line = line.replace(curTimeStamp, maxTimeStamp)
			fileData += line
	with open(CurFileName, "w") as f:
			f.write(fileData)
	return maxTimeStamp

def startTour(ip, op, p1, p2, p3, p4, p5, p6, mf, ps, ts, zs):
	try:
		clientSock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		clientSock.connect((ip, int(op)))
		print 'startTour Connect', ip, op, 'success!'
		cmdStr = 'Tour '
		for item in [p1, p2, p3, p4, p5, p6]:
			cmdStr += item.replace(' ', '') + ';'
		if mf:
			cmdStr += '--- 1 '
			cmdStr += ps + ' ' + ts + ' ' + zs
		cmdStr += '\r\n'
		clientSock.sendall(bytes(cmdStr))
		print 'send cmdStr [', cmdStr, '] success'
		''' rsp
		ret = str(clientSock.recv(1024))
		print ret
		'''
		clientSock.close()
	except socket.error, e:
		print "onvifClient start on", ip, op,"failed"
		print e,int(op)
		traceback.print_exc()
		#sys.exit(1)

def stopTour(ip, op):
	try:
		clientSock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		clientSock.connect((ip, int(op)))
		print 'stopTour Connect', ip, op, 'success!'
		cmdStr = 'Tour stop preset tour\r\n';
		clientSock.sendall(bytes(cmdStr))
		print 'send cmdStr [', cmdStr, '] success'
		'''
		wait rsp
		'''
		clientSock.close()
	except socket.error, e:
		print "onvifClient start on", ip, op,"failed"
		print e,int(op)
		traceback.print_exc()
		#sys.exit(1)

def CtrlRecord(ip, op, action):
	try:
		clientSock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		clientSock.connect((ip, int(op)))
		print 'startRecord Connect', ip, op, 'success!'
		cmdStr = 'Record ';
		if 'start' == action.strip():
			cmdStr += 'START'
		else:
			cmdStr += 'STOP'
		cmdStr += ' record\r\n'
		clientSock.sendall(bytes(cmdStr))
		print 'send cmdStr [', cmdStr, '] success'
		'''
		wait rsp
		'''
		clientSock.close()
	except socket.error, e:
		print "onvifClient start on", ip, op,"failed"
		print e,int(op)
		traceback.print_exc()
		#sys.exit(1)	

def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except socket.error, e:
		print  e
		traceback.print_exc()
		return '127.0.0.1'
    finally:
        s.close()
    return ip

def PTZMotion(cmd, ps, ts, zs, ip, op):
	try:
		panSpeed = 0
		tiltSpeed = 0
		zoomSpeed = 0
		if 'Pan Left' == cmd.strip():
			panSpeed = -1 * float(ps) / 100
		elif 'Pan Right' == cmd.strip():
			panSpeed = float(ps) / 100
		elif 'Tilt Up' == cmd.strip():
			tiltSpeed = float(ts) / 100
		elif 'Tilt Down' == cmd.strip():
			tiltSpeed = -1 * float(ts) / 100
		elif 'Zoom In' == cmd.strip():
			zoomSpeed = float(zs) / 100
		elif 'Zoom Out' == cmd.strip():
			zoomSpeed = -1 * float(zs) / 100
		print cmd, panSpeed, tiltSpeed, zoomSpeed
		clientSock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		clientSock.connect((ip, int(op)))
		print 'PTZMotion Connect', ip, op, 'success!'
		cmdStr = 'PTZ '
		if 'PTZ Home' == cmd.strip():
			cmdStr += 'GOTO HOME '
		else:
			cmdStr += 'Continue Motion '
		cmdStr += '['+ str(panSpeed) + ' ' + str(tiltSpeed) + ' ' + str(zoomSpeed) + ']\r\n'
		print cmdStr
		clientSock.sendall(bytes(cmdStr))
		print 'send cmdStr [', cmdStr, '] success'
		clientSock.close()
	except socket.error, e:
		print "onvifClient start on", ip, op,"failed"
		print e,int(op)
		traceback.print_exc()

def vlcPlay(ipAddr, rtpPort, transType):
	try:
		'''
		sdp_m = 'm=video ' +  rtpPort + ' RTP/AVP 96\n'
		sdp_amap = 'a=rtpmap:96 H264\n'
		sdp_arate = 'a=framerate:30\n'
		sdp_c = 'c=IN IP4 127.0.0.1\n'
		sdp_data = sdp_m + sdp_amap + sdp_arate + sdp_c
		sdp_file = 'rtp.sdp'
		fp = file(sdp_file, 'w')
		fp.write(sdp_data)
		fp.close()
		vlc_cmd = 'vlc file://' + os.getcwd() + '/'+ sdp_file + ' &'
		'''
		clientSock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		clientSock.connect((ipAddr, int(rtpPort)))
		print 'test connect success'
		clientSock.close()
		tansport = ' --no-rtsp-tcp '
		if 'TCP' == transType.strip():
			tansport = ' --rtsp-tcp '
		elif 'UDP' == transType.strip():
			tansport = ' --no-rtsp-tcp '
		elif 'HTTP' == transType.strip():
			tansport = ' --rtsp-http '
		vlc_cmd = 'vlc rtsp://' + ipAddr + ':' + rtpPort + '/onvif/Streaming/channels/101' + tansport +'&'
		os.system(vlc_cmd)
	except OSError:
		print "Can NOT open vlc, Aborted!"
	except socket.error, e:
		print "connect", ipAddr, rtpPort, "failed.", e
		traceback.print_exc()

xmenu = Menu(root)
submenu = Menu(xmenu, tearoff = 0)

submenu.add_command(label = 'ONVIF user manual', command = click_help_onvif)
submenu.add_command(label = 'GB28181 user manual', command = click_help_gb28181)

xmenu.add_cascade(label = 'Help', menu = submenu)
xmenu.add_command(label = 'Exit', command = quit_window)
xmenu.add_command(label = 'AboutMe', command = click_about_me)

#3 content
# para
ParaFrame = LabelFrame(root, text='ONVIF Ctrl', height = 2, fg = 'green')
ParaFrame.grid(row=0, column=0, padx=10, pady=5)

# onvif start para
OnvifFrame = LabelFrame(ParaFrame, text=' Parameter ')
OnvifFrame.grid(row=0, column=0, padx=10, pady=5, rowspan = 5, sticky=N) 
onvifParaIndex = 1
for item in ['Ip Addr  ', 'Rtsp Port  ', 'Onvif Port  ', 'Encode Type  ', 'Res (H*W)  ', 'Img Module  ', 'Render Server  ','Cam Nickname  ']:
	Label(OnvifFrame, text=item, width = 13, height = 2, anchor='e').grid(row=onvifParaIndex,column=0)
	onvifParaIndex += 1

defRIP = StringVar(); defRIP.set(get_host_ip()); IP = Entry(OnvifFrame, textvariable = defRIP, width=23); IP.grid(row=1,column=1)
defRP = StringVar(); defRP.set(onvifDict['rtspPort']); RP = Entry(OnvifFrame, textvariable = defRP, width=23); RP.grid(row=2,column=1)
defOP = StringVar(); defOP.set(onvifDict['onvifPort']); OP = Entry(OnvifFrame, textvariable = defOP, width=23); OP.grid(row=3,column=1)
defEnc = StringVar(); encType = ttk.Combobox(OnvifFrame, textvariable=defEnc, width=21);
encType["values"] = ['h264', 'JPEG', 'h265']; encType.current(0); encType.grid(row=4,column=1)
defRes = StringVar(); resDefine = ttk.Combobox(OnvifFrame, textvariable=defRes, width=21);
resDefine["values"] = [onvifDict['HW1080P'], onvifDict['HW4K'], onvifDict['HWCustom']]; 
resDefine.current(0); resDefine.grid(row=5,column=1);
defImgShow = StringVar(); showType = ttk.Combobox(OnvifFrame, textvariable=defImgShow, width=21);
showType["values"] = ['0: normal', '1: indicate', '2: demarcate']; showType.current(0); showType.grid(row=6,column=1)
defRender = StringVar(); defRender.set(modelDict['RenderServer']);
Render = Entry(OnvifFrame, textvariable = defRender, width=23); Render.grid(row=7, column=1)
defNName = StringVar(); defNName.set(modelDict['NickName']); 
NName = Entry(OnvifFrame, textvariable = defNName, width=23); NName.grid(row=8,column=1)
CB = IntVar(); Checkbutton(OnvifFrame, text="root",variable = CB).grid(row=9,column=0, sticky=W)
defRecord = IntVar(); Checkbutton(OnvifFrame, text = "Start Record ad Default", variable = defRecord).grid(row=9, column=1, sticky=W)

# vlc live
VideoPlay = PhotoImage(file=onvifDict['Play'])
liveFrame = LabelFrame(ParaFrame, text = ' Video Player ')
liveFrame.grid(row=1, column=0, padx=10, pady=5, sticky=SW)
Label(liveFrame, text='Rtsp Transport  ', width=13, height=1, anchor='e').grid(row=0, column=0, padx=0,pady=5)
defTransport = StringVar();Transport=ttk.Combobox(liveFrame, textvariable=defTransport, width=14);
Transport["values"]=['TCP', 'UDP'];Transport.current(1);Transport.grid(row=0, column=1, padx=2,pady=5)
Button(liveFrame, image = VideoPlay, width = 41, height = 30, borderwidth=1, bg = 'green',\
		command=lambda:vlcPlay(IP.get(), RP.get(), Transport.get())).grid(row=0, column=2,padx=5,pady=5)

# button ctrl onvif
StartFrame = LabelFrame(ParaFrame, text=' Command ')
StartFrame.grid(row=0, column=1, padx=10, pady=5, sticky=N)
onvifLogo = PhotoImage(file=onvifDict['onvifLogoFile'])
Label(StartFrame, image=onvifLogo).grid(row=0, column=0, columnspan=2)
Button(StartFrame, text = 'Start ONVIF', width = 12, height = 2, borderwidth=2, bg = 'green', \
		command=lambda:click_start_onvif(CB.get(), IP.get(), RP.get(), OP.get(), \
		encType.get(), resDefine.get(), showType.get(), Render.get(), NName.get(), defRecord.get())).grid(row=1,column=0, padx=10, pady=5)
Button(StartFrame, text = 'ReInstall ONVIF', width = 12, height = 2, bg = 'green', \
		command=lambda:reInstall_onvif()).grid(row=1,column=1, padx=10, pady=5)
Button(StartFrame, text = 'Start RECORD', width = 12, height = 2, bg = 'green', \
		command=lambda:CtrlRecord(IP.get(), OP.get(), 'start')).grid(row=2,column=0, padx=10, pady=5)
Button(StartFrame, text = 'Stop RECORD', width = 12, height = 2, bg = 'green', \
		command=lambda:CtrlRecord(IP.get(), OP.get(), 'stop')).grid(row=2,column=1, padx=10, pady=5)

# ptz ctrl 
PtzFrame = LabelFrame(ParaFrame, text = ' PTZ Ctrl ')
PtzFrame.grid(row=1, column=1, padx=10, pady=5, sticky=N)
PTZLeft = PhotoImage(file=onvifDict['PTZLeft'])
PTZRight = PhotoImage(file=onvifDict['PTZRight'])
PTZUp = PhotoImage(file=onvifDict['PTZUp'])
PTZDown = PhotoImage(file=onvifDict['PTZDown'])
PTZIn = PhotoImage(file=onvifDict['PTZIn'])
PTZOut = PhotoImage(file=onvifDict['PTZOut'])
PTZStop = PhotoImage(file=onvifDict['PTZStop'])
PTZHome = PhotoImage(file=onvifDict['PTZHome'])
Label(PtzFrame, text="P").grid(row=0, column=3, padx=1)
PS=StringVar();PS.set(50);Scale(PtzFrame, from_=0, to=100, resolution=0.1,variable=PS,orient=HORIZONTAL).grid(row=0, column=4, padx=1)
Label(PtzFrame, text="T").grid(row=1, column=3, padx=1)
TS=StringVar();TS.set(50);Scale(PtzFrame, from_=0, to=100, resolution=0.1,variable=TS,orient=HORIZONTAL).grid(row=1, column=4, padx=1)
Label(PtzFrame, text="Z", width=2).grid(row=2, column=3, padx=1)
ZS=StringVar();ZS.set(50);Scale(PtzFrame, from_=0, to=100, resolution=0.1,variable=ZS,orient=HORIZONTAL).grid(row=2, column=4, padx=1)
Button(PtzFrame, width = 40, height = 40, image = PTZLeft, command=lambda:PTZMotion('Pan Left', PS.get(), TS.get(), ZS.get(), IP.get(), OP.get())\
	).grid(row=1,column=0, padx=2, rowspan = 2)
Button(PtzFrame, width = 40, height = 40, image = PTZRight, command=lambda:PTZMotion('Pan Right', PS.get(), TS.get(), ZS.get(), IP.get(), OP.get())\
	).grid(row=1,column=2, padx=2, rowspan = 2)
Button(PtzFrame, width = 40, height = 40, image = PTZUp, command=lambda:PTZMotion('Tilt Up', PS.get(), TS.get(), ZS.get(), IP.get(), OP.get())\
	).grid(row=0,column=1, padx=2)
Button(PtzFrame, width = 40, height = 40, image = PTZDown, command=lambda:PTZMotion('Tilt Down', PS.get(), TS.get(), ZS.get(), IP.get(), OP.get())\
	).grid(row=3,column=1, padx=2)
Button(PtzFrame, width = 50, height = 32, image = PTZIn, command=lambda:PTZMotion('Zoom In', PS.get(), TS.get(), ZS.get(), IP.get(), OP.get())\
	).grid(row=1,column=1, padx=2)
Button(PtzFrame, width = 50, height = 32, image = PTZOut, command=lambda:PTZMotion('Zoom Out', PS.get(), TS.get(), ZS.get(), IP.get(), OP.get())\
	).grid(row=2,column=1, padx=2)
Button(PtzFrame, width = 44, height = 44, image = PTZStop, command=lambda:PTZMotion('PTZ Stop', PS.get(), TS.get(), ZS.get(), IP.get(), OP.get())\
	).grid(row=0, column=2,rowspan=2, sticky=N)
Button(PtzFrame, width = 43, height = 43, image = PTZHome, command=lambda:PTZMotion('PTZ Home', PS.get(), TS.get(), ZS.get(), IP.get(), OP.get())\
	).grid(row=2, column=2,rowspan=2, sticky=S)

# onvif presetTour ctrl para
TourCtrlFrame = LabelFrame(root, text=' Preset Tour Ctrl ', fg = 'green')
TourCtrlFrame.grid(row=1, column=0, padx=10, pady=5, sticky=W)
PresetFrame = LabelFrame(TourCtrlFrame, text = ' Preset Parameter ')
PresetFrame.grid(row=0, column=0, padx=10, pady=5, sticky=N)
Label(PresetFrame, text="Preset Order", width=10, height = 2, anchor = 'c').grid(row=0, column=0)
Label(PresetFrame, text="Stay Time, Speed(P/T/Z)", width=20, height = 2, anchor = 'c').grid(row=0, column=1)
Label(PresetFrame, text='Preset_01', width=10, height=1, anchor='c').grid(row=1, column=0, pady=0)
preset1 = StringVar();preset1.set(onvifDict['tourDefault']);Entry(PresetFrame, textvariable=preset1, width=15).grid(row=1, column=1)
Label(PresetFrame, text='Preset_02', width=10, height=1, anchor='c').grid(row=2, column=0)
preset2 = StringVar();preset2.set(onvifDict['tourDefault']);Entry(PresetFrame, textvariable=preset2, width=15).grid(row=2, column=1)
Label(PresetFrame, text='Preset_03', width=10, height=1, anchor='c').grid(row=3, column=0)
preset3 = StringVar();preset3.set(onvifDict['tourDefault']);Entry(PresetFrame, textvariable=preset3, width=15).grid(row=3, column=1)
Label(PresetFrame, text='Preset_04', width=10, height=1, anchor='c').grid(row=4, column=0)
preset4 = StringVar();preset4.set(onvifDict['tourDefault']);Entry(PresetFrame, textvariable=preset4, width=15).grid(row=4, column=1)
Label(PresetFrame, text='Preset_05', width=10, height=1, anchor='c').grid(row=5, column=0)
preset5 = StringVar();preset5.set(onvifDict['tourDefault']);Entry(PresetFrame, textvariable=preset5, width=15).grid(row=5, column=1)
Label(PresetFrame, text='Preset_06', width=10, height=1, anchor='c').grid(row=6, column=0)
preset6 = StringVar();preset6.set(onvifDict['tourDefault']);Entry(PresetFrame, textvariable=preset6, width=15).grid(row=6, column=1)

MoveFrame = LabelFrame(TourCtrlFrame, text = ' Continuous ')
MoveFrame.grid(row=0, column=1, padx=15, pady=5, sticky=N)
moveFlag = IntVar(); Checkbutton(MoveFrame, text="Move",variable = moveFlag, width = 6).grid(row=0,column=1)
Label(MoveFrame, text="Speed", width=8, height = 2, anchor = 'e').grid(row=1, column=0)
Label(MoveFrame, text="Value", width=8, height = 2, anchor = 'w').grid(row=1, column=1)
index = 2
for item in ['Pan', 'Tilt', 'Zoom']:
	Label(MoveFrame, text=item, width=5, height=2, anchor='e').grid(row=index, column=0)
	index += 1
panSpeed = StringVar(); panSpeed.set(0);Entry(MoveFrame, textvariable=panSpeed, width=6).grid(row=2, column=1)
tiltSpeed = StringVar(); tiltSpeed.set(1);Entry(MoveFrame, textvariable=tiltSpeed, width=6).grid(row=3, column=1)
zoomSpeed = StringVar(); zoomSpeed.set(1.2);Entry(MoveFrame, textvariable=zoomSpeed, width=6).grid(row=4, column=1)

TourFrame = LabelFrame(TourCtrlFrame, text=' Command ')
TourFrame.grid(row=0, column=3, padx=10, pady=5, sticky=N)
Button(TourFrame, text = 'Start Preset Tour', width = 15, height = 2, bg = 'green', \
		command=lambda:startTour(IP.get(), OP.get(), \
		preset1.get(), preset2.get(),preset3.get(),preset4.get(),preset5.get(), preset6.get(),\
		moveFlag.get(), panSpeed.get(), tiltSpeed.get(), zoomSpeed.get())).grid(row=0,column=0, padx=10, pady=5)
Button(TourFrame, text = 'Stop Preset Tour', width = 15, height = 2, bg = 'green', \
		command=lambda:stopTour(IP.get(), OP.get())).grid(row=1,column=0, padx=10, pady=5)

# Model Configuration
ModleCfgFrame = LabelFrame(root, text=' MODEL Cfg ', fg = 'green')
ModleCfgFrame.grid(row=2, column=0, padx=10, pady=5)

# cfg MODLE ctrl
ModelFrame = LabelFrame(ModleCfgFrame, text =' Model Configuration ')
ModelFrame.grid(row=0, column=0, padx=10, pady=5, sticky=N)
PathModelFrame = LabelFrame(ModelFrame, text = ' Model Path ' )
PathModelFrame.grid(row=0, column=0, padx=10, pady=5)
Label(PathModelFrame, text="Model File ", width=8).grid(row = 0, column = 0, padx=5, pady=5)
path = StringVar();path.set(modelDict['DefModelPath'])
Entry(PathModelFrame, textvariable = path, width=22).grid(row = 0, column = 1, padx=5, pady=5)
Button(PathModelFrame, text ="Path Select", width=10, bg ='green', command = selectPath).grid(row = 0, column = 2, padx=5, pady=5)
Label(PathModelFrame, text = "NickName ", width=8).grid(row = 1, column = 0, padx=5, pady=5)
defNickName = StringVar(); defNickName.set(modelDict['NickName']);
NickName = Entry(PathModelFrame, textvariable=defNickName, width=22).grid(row=1, column=1, padx=5, pady=5)
Button(PathModelFrame, text ="Recovery", width=10, bg ='green',\
	command=lambda:recovery_model(os.path.split(path.get())[0])).grid(row = 1, column = 2, padx=5, pady=5)

#0: pagoda; 1: trapezoid; 2: panorama.
FileModelFrame = LabelFrame(ModelFrame, text = ' Model Select ')
FileModelFrame.grid(row=1, column=0, padx=10, pady=5, sticky=W)
Label(FileModelFrame, text = "Model Type", width = 8).grid(row=0,column=0, padx=5, pady=5)
defSaveAs = StringVar(); saveAs = ttk.Combobox(FileModelFrame, textvariable = defSaveAs, width = 21);
saveAs["values"] = ['pagoda', 'panorama LH', 'panorama FH']; saveAs.current(0); 
saveAs.grid(row=0, column = 1,padx=5, pady=5)
Label(FileModelFrame, text = 'Timestamp', width = 8).grid(row = 1, column=0, padx=5, pady=5)
defTimeS = StringVar(); TimeS = Entry(FileModelFrame, textvariable = defTimeS, width=22, state='readonly');
defTimeS.set(update_max_timestamp(os.path.split(path.get())[0], modelDict['ModelEdit']));
TimeS.grid(row=1, column=1, padx=5, pady=5)
Button(FileModelFrame, text = 'Custom ', width = 10, height = 1, bg = 'green', \
		command=lambda:custom_model_cfg(os.path.split(path.get())[0], saveAs.get()))\
		.grid(row=0,column=2, padx=5, pady=5)
Button(FileModelFrame, text = 'Model Adder', width=10, height=1, bg = 'green', \
		command=lambda:StartModelAdder(os.path.split(path.get())[0], defNickName.get(), saveAs.get()))\
		.grid(row=1, column=2, padx=5, pady=5)

# hint MODLE ctrl
HintModelFrame = LabelFrame(ModleCfgFrame, text = ' Calibration ')
HintModelFrame.grid(row = 0, column = 1, padx = 7, pady = 5, sticky=N)
modleLogo = PhotoImage(file=modelDict['modleLogoFile'])
Label(HintModelFrame, image=modleLogo).grid(row=0, column=0, padx = 8, pady = 8, columnspan=2)
Button(HintModelFrame, text = 'Model Calibration', width=15, height=1, bg = 'green', \
		command=StartModelEditor).grid(row=1, column=0, padx=10, pady=8)

'''
def click_start_gb():
	# start gbClien1
	if os.system(gbDict['gbBin']) == 0:
		print 'Successful START gb28181 client on', gbBin
	else:
		print 'START gb28181 client Completed'

def update_gb_content_dict():
	gb_content_dict = {}
	gb_content_dict['server_id'] = gbSid.get()
	gb_content_dict['server_ip'] = gbSip.get()
	gb_content_dict['server_port'] = gbSpo.get()
	gb_content_dict['device_id'] = gbDid.get()
	gb_content_dict['listen_port'] = gbLpo.get()
	gb_content_dict['username'] = gbUsername.get()
	gb_content_dict['password'] = defgbPwd.get()
	gb_content_dict['alarm_id'] = gbAid.get()
	gb_content_dict['media_id'] = gbMid.get()
	gb_content_dict['register_expire'] = gbRex.get()
	return gb_content_dict	

def find_old_key_val(cfgLine, var):
	reStr = '"' + var + '":"(.*)",'
	pattern = re.compile(reStr)
	vallist = pattern.findall(cfgLine)
	if vallist:
		return vallist[0]
	else:
		reStr = '"' + var + '":(.*),'
		pattern = re.compile(reStr)
		vallist = pattern.findall(cfgLine)
		if vallist:
			return vallist[0]
		else:
			reStr = '"' + var + '":(.*)'
			pattern = re.compile(reStr)
			vallist = pattern.findall(cfgLine)
			if vallist:
				return vallist[0]
			else:
				return ''
				
def get_str_value_from_file(filepath, oldStr):
	with open(filepath, "r") as f:
		for line in f:
			if oldStr in line:
				return find_old_key_val(line, oldStr)
		return ''

def replace_oldstr_value_from_file(filepath, oldStr, newStrValue):
	with open(filepath, "r") as f:
		for line in f:
			if oldStr in line:
				oldStrvalue = find_old_key_val(line, oldStr)
				if oldStrvalue:
					line = line.replace(oldStrvalue, newStrValue)
				return line

def update_gbcfg_file(filepath, file_content):
	with open(filepath, "w") as f:
		f.write(file_content)
				
def update_gb_cfg():
	gbcontent_dict = update_gb_content_dict()
	file_new_data = ''
	for index in range(len(gbCfgList)):
		file_new_data += replace_oldstr_value_from_file(gbDict['gbCfgFileName'], gbCfgList[index], gbcontent_dict[gbCfgList[index]])
	print  file_new_data
	file_content =  gbCfgFilePrefix + file_new_data +  gbCfgFileSuffix
	print file_content
	update_gbcfg_file(gbDict['gbCfgFileName'], file_content)

def check_and_create_file(dirpath, filepath):
	try:
		if not(os.path.exists(dirpath)) and not(os.path.isfile(filepath)):
			os.mkdir(dirpath)
		if not(os.path.exists(filepath) and os.path.isfile(filepath)):
			with open(filepath, 'w') as f:
				file_content =  gbCfgFilePrefix + gbCfgFileSuffix
				f.write(file_content)
	except OSError:
		print ("To detect the uninstalled mantis or GB28181, configure the environment first.")
'''
'''
#28181 Ctrl
Gb28181Frame = LabelFrame(root, text=' GB28181 Ctrl ', fg = 'green')
Gb28181Frame.grid(row=2, column=0, padx=10, pady=5)

GbFrame = LabelFrame(Gb28181Frame, text=' user_profile ')
GbFrame.grid(row=0, column=0, padx=10, pady=5)1
# check and  create gb cfg file
check_and_create_file(gbDict['gbCfgFileDir'], gbDict['gbCfgFileName'])
# gb para
for index in range(len(gbCfgList)):
	 Label(GbFrame, text=gbCfgList[index] + '  ',width = 13, height = 2, anchor='e').grid(row=index,column=0)
defgbSid = StringVar(); defgbSid.set(get_str_value_from_file(gbDict['gbCfgFileName'], 'server_id')); gbSid = Entry(GbFrame, textvariable = defgbSid, width=23); gbSid.grid(row=0, column=1, padx=10)
defgbSip = StringVar(); defgbSip.set(get_str_value_from_file(gbDict['gbCfgFileName'], 'server_ip')); gbSip = Entry(GbFrame, textvariable = defgbSip, width=23); gbSip.grid(row=1,column=1)
defgbSpo = StringVar(); defgbSpo.set(get_str_value_from_file(gbDict['gbCfgFileName'], 'server_port')); gbSpo = Entry(GbFrame, textvariable = defgbSpo, width=23); gbSpo.grid(row=2,column=1)
defgbDid = StringVar(); defgbDid.set(get_str_value_from_file(gbDict['gbCfgFileName'], 'device_id')); gbDid = Entry(GbFrame, textvariable = defgbDid, width=23); gbDid.grid(row=3,column=1)
defgbLpo = StringVar(); defgbLpo.set(get_str_value_from_file(gbDict['gbCfgFileName'], 'listen_port')); gbLpo = Entry(GbFrame, textvariable = defgbLpo, width=23); gbLpo.grid(row=4,column=1)
defgbUsername = StringVar(); defgbUsername.set(get_str_value_from_file(gbDict['gbCfgFileName'], 'username')); gbUsername = Entry(GbFrame, textvariable = defgbUsername, width=23); gbUsername.grid(row=5,column=1)
defgbPwd = StringVar(); defgbPwd.set(get_str_value_from_file(gbDict['gbCfgFileName'], 'password')); gbPwd = Entry(GbFrame, textvariable = defgbPwd, width=23, show='*'); gbPwd.grid(row=6,column=1)
defgbAid = StringVar(); defgbAid.set(get_str_value_from_file(gbDict['gbCfgFileName'], 'alarm_id')); gbAid = Entry(GbFrame, textvariable = defgbAid, width=23); gbAid.grid(row=7,column=1)
defgbMid = StringVar(); defgbMid.set(get_str_value_from_file(gbDict['gbCfgFileName'], 'media_id')); gbMid = Entry(GbFrame, textvariable = defgbMid, width=23); gbMid.grid(row=8,column=1)
defgbRex = StringVar(); defgbRex.set(get_str_value_from_file(gbDict['gbCfgFileName'], 'register_expire')); gbRex = Entry(GbFrame, textvariable = defgbRex, width=23); gbRex.grid(row=9,column=1)

# button ctrl 28181
Ctrl28181Frame = LabelFrame(Gb28181Frame, text=' Command ')
Ctrl28181Frame.grid(row=0, column=1, padx=10, pady=5, sticky=N)
gbLogo = PhotoImage(file=gbDict['gbLogoFile'])
Label(Ctrl28181Frame, image=gbLogo).grid(row=0, column=0, columnspan=2)
Button(Ctrl28181Frame, text = 'Update 28181 Cfg', width = 12, height = 2, bg = 'green', \
		command=lambda:update_gb_cfg()).grid(row=1,column=0, padx=10, pady=10)
Button(Ctrl28181Frame, text = 'Start 28181', width = 12, height = 2, bg = 'green', \
		command=lambda:click_start_gb()).grid(row=1,column=1, padx=10, pady=5)
'''

root['menu'] = xmenu

root.mainloop()
