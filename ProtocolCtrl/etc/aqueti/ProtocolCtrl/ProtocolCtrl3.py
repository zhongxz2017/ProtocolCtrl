#! /usr/bin/env python3
# _*_ coding: UTF-8 _*_ 
# Filename: ProtocolCtrl.py

import os
from tkinter import *
from tkinter.ttk import *
import webbrowser
from tkinter.filedialog import askdirectory

installDir = '/etc/aqueti/ProtocolCtrl/'
gbInstallDir = '/etc/aqueti/GB/'
pipVersion = 'pip3'

dependencyDict = {
	'netifaces27'	:	installDir + 'dependency/' + 'netifaces-0.10.6-cp27-cp27mu-linux_x86_64.whl',
	'netifaces35'	:	installDir + 'dependency/' + 'netifaces-0.10.6-cp35-cp35m-linux_x86_64.whl',
	}

try:
    import netifaces
except ImportError:
    try:		
        command_to_execute = "echo 'NOTICE:Need to install dependencies\n';sudo " + pipVersion +" install " + dependencyDict['netifaces35']
        os.system(command_to_execute)
    except OSError:
        print ("Can NOT install netifaces, Aborted!")
        sys.exit(1)
    import netifaces

# onvif cmd para define
onvifDict = {
	'onvifBin' : 'mantisONVIFServer',
	'rtspIpAddr' : '',
	'rtspPort' : '17100',
	'onvifPort' : '21100',
	'resHight'	: '1080',
	'resWight'	: '1920',
	'onvifLogoFile' : installDir + 'logo/onvifLogo.png'
	}

# 28181 cmd/cfg para define
gbCfgList = ('server_id', 'server_ip', 'server_port', 'device_id', 'listen_port', 'username', 'password', 'alarm_id', 'media_id', 'register_expire')
gbDict =  {
	'gbCfgFileName' : gbInstallDir + 'mantisGBprofile.conf',
	'gbCfgFileDir' : gbInstallDir,
	'gbBin' : 'mantisGBclient',
	'gbLogoFile' : installDir + 'logo/gb28181Logo.png'
	}

gbCfgFilePrefix = '{\n  "keepalive_timeout":10,\n  "re-register_timeout":60,\n  "keepalive_timeout_num":3,\n  "user_profile":{\n'
gbCfgFileSuffix ='  }\n}'

# modle
modelDict = {
	'modleLogoFile' : './logo/modelCtrl.png',
	'DefModelName'	: 'mantis_61231',
	'ModelDir'		: '/etc/aqueti',
	'ModelFile'		: 'model.json',
	'FHDModelFile'	: 'modelFullHD.json',
	'PanoModelFile'	: 'modelPanorama.json'
	}

helpDocDict = {
	'onvifHelp' : installDir + 'help/Mantis_ONVIF_help' + '.docx',
	'gb28181Help' : installDir + 'help/Mantis_ONVIF_help' + '.docx',
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
 * MODEL
 *	1. Select model file
 *	2. Modify model file
 * GB28181
 *	1. Modify gb28181 config
 *	2. Update gb28181 config
 *	3. Start gb28181
 *
****************************************************************************************'''

ContactNotice = '''***************************************************************************************
 *
 * Lynn, Zhong
 * 2018-06-08
 * xiaozhen.zhong@aqueti.com
 *
****************************************************************************************'''

root = Tk()
#root.geometry('450x400')
root.resizable(True, False)
root.attributes("-alpha",0.6)
#1 title
root.title('ProtocolCtrl')

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
	#NoticeFrame = LabelFrame(top, text=' Notice ', width = 60, height = 2, fg = 'green')
	#NoticeFrame.grid(row=0, column=0, padx=10, pady=10)
	LicenseFrame = LabelFrame(top, text=' Permission statement ')
	LicenseFrame.grid(row=0, column=0, padx=10, pady=10)
	Label(LicenseFrame, text = LisenceNotice, wraplength = 720, justify = 'left').grid(row = 0, column = 0, padx=10, pady=10)
	FunctionFrame = LabelFrame(top, text=' Software Features  ')
	FunctionFrame.grid(row=1, column=0, padx=10, pady=10)
	Label(FunctionFrame, text = FunctionNotice, wraplength = 720, justify = 'left').grid(row = 0, column = 0, padx=10, pady=10)
	ContactFrame = LabelFrame(top, text=' Contact Us ')
	ContactFrame.grid(row=2, column=0, padx=10, pady=10)
	Label(ContactFrame, text = ContactNotice, wraplength = 720, justify = 'left').grid(row = 0, column = 0, padx=10, pady=10)

def click_start_onvif(sudo, rip, rp, op, enc, show):
	print ("click_start_onvif", sudo, rip, rp, op, enc, show)

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
	if '0: trapezoid' == show.strip():
		start_onvif_commad += ' -Show 0'
	elif '1: pagoda' == show.strip():
		start_onvif_commad += ' -Show 1'
	else:
		start_onvif_commad += ' -Show 2'

	print ('Start onvifServer CMD [' + start_onvif_commad + "]")
	# start onvifServer
	if os.system(start_onvif_commad) == 0:
		print ('Successful START onvifServer on', start_onvif_commad)
	else:
		print ('START onvifServer Completed')
	
def reInstall_onvif():
	print (os.system("pwd"));
	rebuild_commad = 'sudo dpkg -r mantis_onvifserver;'
	#rebuild_commad += 'make ONVIFServer;'
	rebuild_commad += 'sudo dpkg -i /etc/aqueti/ProtocolCtrl/mantis_ONVIFServer-0.*.0.*_.deb'
	
	# start onvifServer
	if os.system(rebuild_commad) == 0:
		print ('Successful ReInstall onvifServer on', rebuild_commad)
	else:
		print ('ReInstall onvifServer Completed')

def click_start_gb():
	# start gbClient
	if os.system(gbDict['gbBin']) == 0:
		print ('Successful START gb28181 client on', gbBin)
	else:
		print ('START gb28181 client Completed')

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
	print  (file_new_data)
	file_content =  gbCfgFilePrefix + file_new_data +  gbCfgFileSuffix
	print (file_content)
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

def get_ip_list():
	netCardList = netifaces.interfaces()
	ipv4List = []
	for netCardName in netCardList:
		ipv4 = get_ip_address(netCardName)
		if ipv4.strip():
			ipv4List.append(ipv4)
	return ipv4List

def get_ip_address(ifname):
	ipStr = ''
	try:
		ipStr = netifaces.ifaddresses(ifname)[2][0]['addr']
	except:
		print ("Err:Please check whether the network card [" + ifname + "] is properly configured with address information.")
	return ipStr

def selectPath():
	path_ = askdirectory()
	path.set(path_)

def select_model_cfg(dirpath):
	try:
		if not(os.path.isfile(dirpath)):
			print ("Err: Invalid path dir " + dirpath)
			return
		modelfile = os.path.split(dirpath)[0] + '/' + modelDict['ModelFile']
		os.rename(dirpath, modelfile)
		backup = 'cp' + ' ' + modelfile + ' ' + dirpath
		os.system(backup)
		print (os.path.split(dirpath)[1] + " should be used to render")
	except OSError:
		print ("open modelFile ", dirpath, " abnormal.")
		return

xmenu = Menu(root)
submenu = Menu(xmenu, tearoff = 0)

submenu.add_command(label = 'ONVIF user manual', command = click_help_onvif)
submenu.add_command(label = 'GB28181 user manual', command = click_help_gb28181)

xmenu.add_cascade(label = 'Help', menu = submenu)
xmenu.add_command(label = 'Exit', command = quit_window)
xmenu.add_command(label = 'AboutMe', command = click_about_me)

#3 content
# para
ParaFrame = LabelFrame(root, text='ONVIF Ctrl', height = 2)
ParaFrame.grid(row=0, column=0, padx=10, pady=10)

# onvif start para
OnvifFrame = LabelFrame(ParaFrame, text=' Parameter ')
OnvifFrame.grid(row=0, column=0, padx=10, pady=10) 

onvifParaIndex = 1
for item in ['Permission  ', 'Ip Addr  ', 'Rtsp Port  ', 'Onvif Port  ', 'Encode Type   ', 'Img Module  ']:
	Label(OnvifFrame, text=item, width = 13, anchor='e').grid(row=onvifParaIndex,column=0, padx=5, pady=5)
	onvifParaIndex += 1

CB = IntVar(); Checkbutton(OnvifFrame, text="Enabled",variable = CB).grid(row=1,column=1, padx=5, pady=5)
defRIP = StringVar(); ipv4List = Combobox(OnvifFrame, textvariable=defRIP, width=21); 
ipv4List["values"]= get_ip_list(); ipv4List.current(1); ipv4List.grid(row=2,column=1, padx=5, pady=5)
defRP = StringVar(); defRP.set(onvifDict['rtspPort']); RP = Entry(OnvifFrame, textvariable = defRP, width=23); RP.grid(row=3,column=1, padx=5, pady=5)
defOP = StringVar(); defOP.set(onvifDict['onvifPort']); OP = Entry(OnvifFrame, textvariable = defOP, width=23); OP.grid(row=4,column=1, padx=5, pady=5)
defEnc = StringVar(); encType = Combobox(OnvifFrame, textvariable=defEnc, width=21);
encType["values"] = ['h264', 'JPEG', 'h265']; encType.current(1); encType.grid(row=5,column=1)
defImgShow = StringVar(); showType = Combobox(OnvifFrame, textvariable=defImgShow, width=21);
showType["values"] = ['2: panorama', '0: trapezoid', '1: pagoda']; showType.current(0); showType.grid(row=6,column=1)

# button ctrl onvif
StartFrame = LabelFrame(ParaFrame, text=' Command ')
StartFrame.grid(row=0, column=1, padx=10, pady=10, sticky=N)
onvifLogo = PhotoImage(file=onvifDict['onvifLogoFile'])
Label(StartFrame, image=onvifLogo).grid(row=0, column=0, columnspan=2)
Button(StartFrame, text = 'Start ONVIF', width = 14, \
		command=lambda:click_start_onvif(CB.get(), ipv4List.get(), RP.get(), OP.get(), encType.get(), showType.get())).grid(row=1,column=0, padx=10, pady=10)
Button(StartFrame, text = 'ReInstall ONVIF', width = 14, \
		command=lambda:reInstall_onvif()).grid(row=1,column=1, padx=10, pady=10)

# Model Configuration
ModleCfgFrame = LabelFrame(root, text=' MODEL Cfg ')
ModleCfgFrame.grid(row=1, column=0, padx=10, pady=10)

# cfg MODLE ctrl
ModelFrame = LabelFrame(ModleCfgFrame, text =' Model Configuration ')
ModelFrame.grid(row=0, column=0, padx=10, pady=10)
PathModelFrame = LabelFrame(ModelFrame, text = ' Path' )
PathModelFrame.grid(row=0, column=0, padx=10, pady=10)
Label(PathModelFrame, text="Model Dir ", width = 12, anchor='e').grid(row = 0, column = 0, padx=5, pady=5)
identify = StringVar(); identify.set(modelDict['DefModelName'])
Entry(PathModelFrame, textvariable = identify).grid(row = 0, column = 1, padx=5, pady=5)
Label(PathModelFrame, text="Mantis Work ", width = 12, anchor='e').grid(row = 1, column = 0, padx=5, pady=5)
path = StringVar();path.set(modelDict['ModelDir'])
Entry(PathModelFrame, textvariable = path).grid(row = 1, column = 1, padx=5, pady=5)
Button(PathModelFrame, text = "Path Select", command = selectPath).grid(row = 1, column = 2, padx=5, pady=5)

#0: pagoda; 1: trapezoid; 2: panorama.
CfgModelFrame = LabelFrame(ModelFrame, text = ' Model select ')
CfgModelFrame.grid(row=1, column=0, padx=10, pady=10)
Button(CfgModelFrame, text = 'FullHD ', width = 10, \
		command=lambda:select_model_cfg(path.get() + '/' + identify.get() + '/' + modelDict['FHDModelFile']))\
		.grid(row=0,column=0, padx=10, pady=10)
Button(CfgModelFrame, text = 'Panorama ', width = 10, \
		command=lambda:select_model_cfg(path.get() + '/' + identify.get() + '/' + modelDict['PanoModelFile']))\
		.grid(row=0,column=1, padx=10, pady=10)
Button(CfgModelFrame, text = 'Custom ', width = 10, \
		command=lambda:select_model_cfg(path.get() + '/' + identify.get() + '/' + modelDict['ModelFile']))\
		.grid(row=0,column=2, padx=10, pady=10)

# hint MODLE ctrl
HintModelFrame = LabelFrame(ModleCfgFrame, text = ' Hint ')
HintModelFrame.grid(row = 0, column = 1, padx = 10, pady = 10, sticky=N)
modleLogo = PhotoImage(file=modelDict['modleLogoFile'])
Label(HintModelFrame, image=modleLogo).grid(row=0, column=0, padx = 8, pady = 8, columnspan=2)

#28181 Ctrl
Gb28181Frame = LabelFrame(root, text=' GB28181 Ctrl ')
Gb28181Frame.grid(row=2, column=0, padx=10, pady=10)

GbFrame = LabelFrame(Gb28181Frame, text=' user_profile ')
GbFrame.grid(row=0, column=0, padx=10, pady=10)

# check and  create gb cfg file
check_and_create_file(gbDict['gbCfgFileDir'], gbDict['gbCfgFileName'])
# gb para
for index in range(len(gbCfgList)):
	 Label(GbFrame, text=gbCfgList[index] + '  ',width = 13, anchor='e').grid(row=index,column=0,padx=5, pady=5)
defgbSid = StringVar(); defgbSid.set(get_str_value_from_file(gbDict['gbCfgFileName'], 'server_id')); gbSid = Entry(GbFrame, textvariable = defgbSid, width=23); gbSid.grid(row=0, column=1, padx=5)
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
Ctrl28181Frame.grid(row=0, column=1, padx=10, pady=10, sticky=N)
gbLogo = PhotoImage(file=gbDict['gbLogoFile'])
Label(Ctrl28181Frame, image=gbLogo).grid(row=0, column=0, columnspan=2)
Button(Ctrl28181Frame, text = 'Update 28181 Cfg', width = 14, \
		command=lambda:update_gb_cfg()).grid(row=1,column=0, padx=10, pady=10)
Button(Ctrl28181Frame, text = 'Start 28181', width = 14, \
		command=lambda:click_start_gb()).grid(row=1,column=1, padx=10, pady=10)

root['menu'] = xmenu

root.mainloop()
