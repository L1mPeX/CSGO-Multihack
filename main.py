# < Импорт модулей >
from PyQt5 import QtCore, QtGui, QtWidgets
from threading import Thread
from win32gui import GetWindowText, GetForegroundWindow
import tkinter as tk
import pymem, pymem.process, ctypes, requests, re, time, keyboard, pyautogui
# <...>

# < Переменные > 
_translate = QtCore.QCoreApplication.translate

pm     = ''
client = ''
engine = ''

Glow_E = False
Cham_s = False
TrigerB = False
BHo_p = False
Radar_H = False
NOFlas_h = False
Auto = False
Triger_T = 0
fov = 0



t  = ''
ct = ''

t_a   = 0
t_b   = 0
t_c   = 0

ct_a  = 0
ct_b  = 0
ct_c  = 0

t_a1   = 0
t_b1   = 0
t_c1   = 0
# <...> 

# < Оффсеты >
dwLocalPlayer       = 0
dwGlowObjectManager = 0
dwEntityList        = 0
dwForceAttack       = 0
dwForceJump         = 0

m_iCrosshairId      = 0
m_iTeamNum          = 0
m_iGlowIndex        = 0
m_fFlags            = 0
m_bSpotted          = 0
m_flFlashMaxAlpha   = 0
m_clrRender         = 0 
m_iDefaultFOV       = 0x332C

def get_sig(modname, pattern, extra = 0, offset = 0, relative = True):
    module = pymem.process.module_from_name(pm.process_handle, modname)
    bytes = pm.read_bytes(module.lpBaseOfDll, module.SizeOfImage)
    match = re.search(pattern, bytes).start()
    non_relative = pm.read_int(module.lpBaseOfDll + match + offset) + extra
    yes_relative = pm.read_int(module.lpBaseOfDll + match + offset) + extra - module.lpBaseOfDll
    return "0x{:X}".format(yes_relative) if relative else "0x{:X}".format(non_relative)
# <...>

# < Функции >

#  < Glow_ESP >
def Color():

	global t, ct, t_a, t_b, t_c, ct_a, ct_b, ct_c, t_a1, t_b1, t_c1

	t  = ui.comboBox_1.currentText()
	ct = ui.comboBox_2.currentText()

	if t == 'Без подсветки':
		t_a1 = 255
		t_a = 0
		t_b1 = 255
		t_b = 0
		t_c1 = 255
		t_c = 0
	else:
		pass

	if t == 'Красный':
		t_a = 1
		t_a1 = 250
		t_b = 0
		t_b1 = 17
		t_c = 0
		t_c1 = 5
	else:
		pass

	if t == 'Зеленый':
		t_a = 0
		t_a1 = 6
		t_b = 1
		t_b1 = 251
		t_c = 0
		t_c1 = 6
	else:
		pass

	if t == 'Синий':
		t_a = 0
		t_a1 = 50
		t_b = 0
		t_b1 = 6
		t_c = 1
		t_c1 = 245
	else:
		pass

	if t == 'Желтый':
		t_a = 1
		t_a1 = 214
		t_b = 1
		t_b1 = 240
		t_c = 0
		t_c1 = 32
	else:
		pass

	if t == 'Белый':
		t_a = 1
		t_a1 = 255
		t_b = 1
		t_b1 = 255
		t_c = 1 
		t_c1 = 255
	else:
		pass

	if t == 'Голубой':
		t_a = 0
		t_a1 = 32
		t_b = 1
		t_b1 = 238
		t_c = 1
		t_c1 = 240
	else:
		pass

	if t == 'Розовый':
		t_a = 1
		t_a1 = 237
		t_b = 0
		t_b1 = 44
		t_c = 1
		t_c1 = 231
	else:
		pass

	if ct == 'Без подсветки':
		ct_a = 0
		ct_b = 0
		ct_c = 0
	else:
		pass

	if ct == 'Красный':
		ct_a = 1
		ct_b = 0
		ct_c = 0
	else:
		pass

	if ct == 'Зеленый':
		ct_a = 0
		ct_b = 1
		ct_c = 0
	else:
		pass

	if ct == 'Синий':
		ct_a = 0
		ct_b = 0
		ct_c = 1
	else:
		pass

	if ct == 'Желтый':
		ct_a = 1
		ct_b = 1
		ct_c = 0
	else:
		pass

	if ct == 'Белый':
		ct_a = 1
		ct_b = 1
		ct_c = 1 
	else:
		pass

	if ct == 'Голубой':
		ct_a = 0
		ct_b = 1
		ct_c = 1
	else:
		pass

	if ct == 'Розовый':
		ct_a = 1
		ct_b = 0
		ct_c = 1
	else:
		pass

def ESP():
    while not Glow_E:
        time.sleep (0.009)
        glow_manager = pm.read_int(client + dwGlowObjectManager)

        for i in range(1, 32):
            entity = pm.read_int(client + dwEntityList + i * 0x10)

            if entity:
                entity_team_id = pm.read_int(entity + m_iTeamNum)
                entity_glow = pm.read_int(entity + m_iGlowIndex)

                if entity_team_id == 2:  # Terrorist
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x4, float(t_a))
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x8, float(t_b))
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0xC, float(t_c))
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x10, float(1))
                    pm.write_int(glow_manager + entity_glow * 0x38 + 0x24, 1)

                elif entity_team_id == 3:  # Counter-terrorist
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x4, float(ct_a))
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x8, float(ct_b))
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0xC, float(ct_c))
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x10, float(1))
                    pm.write_int(glow_manager + entity_glow * 0x38 + 0x24, 1)
#  <...>

#  < Chams >
def Chams_f():
    global Cham_s
    while not Cham_s:
        try:
            for ent_id in range(1, 32):
                ent = pm.read_int(client + dwEntityList + ent_id * 0x10)
                pm.write_int(ent + m_clrRender, t_a1)  # Red
                pm.write_int(ent + m_clrRender + 1, t_b1)  # Green
                pm.write_int(ent + m_clrRender + 2, t_c1)  # Blue
                pm.write_int(ent + m_clrRender + 3, 0)  # Alpha
                Cham_s = True
        except:
            pass
#  <...>

#  < TrigerBot>
def TrigerBo_t():
	while not TrigerB:
		if not GetWindowText(GetForegroundWindow()) == "Counter-Strike: Global Offensive":
			continue

		player = pm.read_int(client + dwLocalPlayer)
		entity_id = pm.read_int(player + m_iCrosshairId)
		entity = pm.read_int(client + dwEntityList + (entity_id - 1) * 0x10)

		entity_team = pm.read_int(entity + m_iTeamNum)
		player_team = pm.read_int(player + m_iTeamNum)
		if entity_id > 0 and entity_id <= 64 and player_team != entity_team:
			time.sleep (Triger_T)
			pm.write_int(client + dwForceAttack, 6)
		time.sleep(0.01)
#  <...>

#  < BunnyHop >
def BunnyHo_p():
    while not BHo_p:
        if pm.read_int(client + dwLocalPlayer):
            player = pm.read_int(client + dwLocalPlayer)
            force_jump = client + dwForceJump
            on_ground = pm.read_int(player + m_fFlags)

            if keyboard.is_pressed("space"):
                if on_ground == 257:
                    pm.write_int(force_jump, 5)
                    time.sleep(0.17)
                    pm.write_int(force_jump, 4)
#  <...>

#  < RadarHack >
def RadarHac_k():
    while not Radar_H:
        if pm.read_int(client + dwLocalPlayer):
            localplayer = pm.read_int(client + dwLocalPlayer)
            localplayer_team = pm.read_int(localplayer + m_iTeamNum)
            for i in range(64):
                if pm.read_int(client + dwEntityList + i * 0x10):
                    entity = pm.read_int(client + dwEntityList + i * 0x10)
                    entity_team = pm.read_int(entity + m_iTeamNum)
                    if entity_team != localplayer_team:
                        pm.write_int(entity + m_bSpotted, 1)
#  <...>

#  < NOFlash >
def NF1ash():
    while not NOFlas_h:
        player = pm.read_int(client + dwLocalPlayer)
        if player:
            flash_value = player + m_flFlashMaxAlpha
            if flash_value:
                pm.write_float(flash_value, float(0))
        time.sleep(1)
#  <...>

#  < AutoAccept >
root = tk.Tk()
h = root.winfo_screenwidth()     # Ширина
w = root.winfo_screenheight()    # Высота
h2 = h/2
w2 = w/2 + 30
w3 = w/2 + 60

def AutoAccep_t():
	while not Auto:
		if not GetWindowText(GetForegroundWindow()) == "Counter-Strike: Global Offensive":
			continue

		time.sleep (3)
		pyautogui.click(h2,w2)
		pyautogui.click(h2,w3)
#  <...>

#  < FOV_P >
def FOVP():
	print ('fov')
	player = pm.read_int(client + dwEntityList)
	iFOV = pm.read_int(player + m_iDefaultFOV)
	print(iFOV)
	pm.write_int(player + m_iDefaultFOV, fov)
#  <...>

# <...>``	


class Ui_Main_Menu(object):
    def setupUi(self, Main_Menu):
        Main_Menu.setObjectName("Main_Menu")
        Main_Menu.resize(365, 545)
        Main_Menu.setMaximumSize(QtCore.QSize(365, 545))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("res/mini.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Main_Menu.setWindowIcon(icon)
        self.backgr = QtWidgets.QLabel(Main_Menu)
        self.backgr.setGeometry(QtCore.QRect(0, 0, 761, 561))
        self.backgr.setStyleSheet("background-color: rgb(15,15,15)")
        self.backgr.setText("")
        self.backgr.setObjectName("backgr")
        self.label = QtWidgets.QLabel(Main_Menu)
        self.label.setGeometry(QtCore.QRect(50, 10, 85, 36))
        self.label.setStyleSheet("font: 24pt \"mr_Franklin GothicG\";")
        self.label.setObjectName("label")
        self.label_4 = QtWidgets.QLabel(Main_Menu)
        self.label_4.setGeometry(QtCore.QRect(40, 50, 8, 29))
        self.label_4.setStyleSheet("font: 20pt \"mr_FranklinGothicG\";")
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(Main_Menu)
        self.label_5.setGeometry(QtCore.QRect(30, 80, 18, 29))
        self.label_5.setStyleSheet("font: 20pt \"mr_FranklinGothicG\";")
        self.label_5.setObjectName("label_5")
        self.comboBox_1 = QtWidgets.QComboBox(Main_Menu)
        self.comboBox_1.setGeometry(QtCore.QRect(60, 50, 111, 21))
        self.comboBox_1.setStyleSheet("")
        self.comboBox_1.setObjectName("comboBox_1")
        self.comboBox_1.addItem("")
        self.comboBox_1.addItem("")
        self.comboBox_1.addItem("")
        self.comboBox_1.addItem("")
        self.comboBox_1.addItem("")
        self.comboBox_1.addItem("")
        self.comboBox_1.addItem("")
        self.comboBox_1.addItem("")
        self.comboBox_2 = QtWidgets.QComboBox(Main_Menu)
        self.comboBox_2.setGeometry(QtCore.QRect(60, 80, 111, 21))
        self.comboBox_2.setStyleSheet("")
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.label_6 = QtWidgets.QLabel(Main_Menu)
        self.label_6.setGeometry(QtCore.QRect(20, 110, 32, 29))
        self.label_6.setStyleSheet("font: 20pt \"mr_FranklinGothicG\";")
        self.label_6.setObjectName("label_6")
        self.comboBox_3 = QtWidgets.QComboBox(Main_Menu)
        self.comboBox_3.setGeometry(QtCore.QRect(60, 110, 111, 22))
        self.comboBox_3.setObjectName("comboBox_3")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.pushButton_1 = QtWidgets.QPushButton(Main_Menu)
        self.pushButton_1.setGeometry(QtCore.QRect(20, 140, 71, 31))
        self.pushButton_1.setStyleSheet("QPushButton{\n"
"  color: white;\n"
"  background-color: rgb(30,30,30);\n"
"  width: 75px;\n"
"  height: 50px;\n"
"  font-size: 14px;\n"
"  font-weight: bold;\n"
"  border: none;\n"
"  text-align: center;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"  background-color: rgb(35,35,35);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"  background-color: rgb(45,45,45);\n"
"}")
        self.pushButton_1.setObjectName("pushButton_1")
        self.pushButton_2 = QtWidgets.QPushButton(Main_Menu)
        self.pushButton_2.setGeometry(QtCore.QRect(100, 140, 71, 31))
        self.pushButton_2.setStyleSheet("QPushButton{\n"
"  color: white;\n"
"  background-color: rgb(30,30,30);\n"
"  width: 75px;\n"
"  height: 50px;\n"
"  font-size: 14px;\n"
"  font-weight: bold;\n"
"  border: none;\n"
"  text-align: center;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"  background-color: rgb(35,35,35);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"  background-color: rgb(45,45,45);\n"
"}")
        self.pushButton_2.setObjectName("pushButton_2")
        self.line = QtWidgets.QFrame(Main_Menu)
        self.line.setGeometry(QtCore.QRect(10, 170, 171, 20))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.line_2 = QtWidgets.QFrame(Main_Menu)
        self.line_2.setGeometry(QtCore.QRect(170, 30, 20, 151))
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.line_3 = QtWidgets.QFrame(Main_Menu)
        self.line_3.setGeometry(QtCore.QRect(0, 30, 20, 151))
        self.line_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.line_4 = QtWidgets.QFrame(Main_Menu)
        self.line_4.setGeometry(QtCore.QRect(10, 20, 31, 21))
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.line_5 = QtWidgets.QFrame(Main_Menu)
        self.line_5.setGeometry(QtCore.QRect(150, 20, 31, 21))
        self.line_5.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.label_2 = QtWidgets.QLabel(Main_Menu)
        self.label_2.setGeometry(QtCore.QRect(50, 190, 85, 38))
        self.label_2.setStyleSheet("font: 24pt \"mr_Franklin GothicG\";")
        self.label_2.setObjectName("label_2")
        self.label_7 = QtWidgets.QLabel(Main_Menu)
        self.label_7.setGeometry(QtCore.QRect(20, 230, 48, 29))
        self.label_7.setStyleSheet("font: 20pt \"mr_FranklinGothicG\";")
        self.label_7.setObjectName("label_7")
        self.lineEdit = QtWidgets.QLineEdit(Main_Menu)
        self.lineEdit.setGeometry(QtCore.QRect(70, 230, 41, 31))
        self.lineEdit.setStyleSheet("font: 18pt \"mr_Franklin GothicG\";\n"
"color: white;\n"
"background-color: rgb(25,25,25);")
        self.lineEdit.setObjectName("lineEdit")
        self.label_8 = QtWidgets.QLabel(Main_Menu)
        self.label_8.setGeometry(QtCore.QRect(20, 270, 41, 29))
        self.label_8.setStyleSheet("font: 20pt \"mr_FranklinGothicG\";")
        self.label_8.setObjectName("label_8")
        self.pushButton_3 = QtWidgets.QPushButton(Main_Menu)
        self.pushButton_3.setGeometry(QtCore.QRect(60, 270, 75, 31))
        self.pushButton_3.setStyleSheet("QPushButton{\n"
"  color: white;\n"
"  background-color: rgb(15,15,15);\n"
"  width: 75px;\n"
"  height: 50px;\n"
"  font-size: 16px;\n"
"  font-weight: bold;\n"
"  border: none;\n"
"  text-align: center;\n"
"}\n"
"\n"
"\n"
"QPushButton:pressed {\n"
"  color: rgb(161,161,161);\n"
"}")
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(Main_Menu)
        self.pushButton_4.setGeometry(QtCore.QRect(20, 300, 71, 31))
        self.pushButton_4.setStyleSheet("QPushButton{\n"
"  color: white;\n"
"  background-color: rgb(30,30,30);\n"
"  width: 75px;\n"
"  height: 50px;\n"
"  font-size: 14px;\n"
"  font-weight: bold;\n"
"  border: none;\n"
"  text-align: center;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"  background-color: rgb(35,35,35);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"  background-color: rgb(45,45,45);\n"
"}")
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = QtWidgets.QPushButton(Main_Menu)
        self.pushButton_5.setGeometry(QtCore.QRect(100, 300, 71, 31))
        self.pushButton_5.setStyleSheet("QPushButton{\n"
"  color: white;\n"
"  background-color: rgb(30,30,30);\n"
"  width: 75px;\n"
"  height: 50px;\n"
"  font-size: 14px;\n"
"  font-weight: bold;\n"
"  border: none;\n"
"  text-align: center;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"  background-color: rgb(35,35,35);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"  background-color: rgb(45,45,45);\n"
"}")
        self.pushButton_5.setObjectName("pushButton_5")
        self.line_6 = QtWidgets.QFrame(Main_Menu)
        self.line_6.setGeometry(QtCore.QRect(10, 330, 171, 20))
        self.line_6.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_6.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_6.setObjectName("line_6")
        self.line_7 = QtWidgets.QFrame(Main_Menu)
        self.line_7.setGeometry(QtCore.QRect(170, 210, 20, 131))
        self.line_7.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_7.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_7.setObjectName("line_7")
        self.line_8 = QtWidgets.QFrame(Main_Menu)
        self.line_8.setGeometry(QtCore.QRect(0, 210, 20, 131))
        self.line_8.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_8.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_8.setObjectName("line_8")
        self.line_9 = QtWidgets.QFrame(Main_Menu)
        self.line_9.setGeometry(QtCore.QRect(10, 200, 31, 21))
        self.line_9.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_9.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_9.setObjectName("line_9")
        self.line_10 = QtWidgets.QFrame(Main_Menu)
        self.line_10.setGeometry(QtCore.QRect(150, 200, 31, 21))
        self.line_10.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_10.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_10.setObjectName("line_10")
        self.label_3 = QtWidgets.QLabel(Main_Menu)
        self.label_3.setGeometry(QtCore.QRect(70, 350, 43, 38))
        self.label_3.setStyleSheet("font: 24pt \"mr_Franklin GothicG\";")
        self.label_3.setObjectName("label_3")
        self.line_11 = QtWidgets.QFrame(Main_Menu)
        self.line_11.setGeometry(QtCore.QRect(10, 530, 171, 20))
        self.line_11.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_11.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_11.setObjectName("line_11")
        self.line_12 = QtWidgets.QFrame(Main_Menu)
        self.line_12.setGeometry(QtCore.QRect(0, 370, 20, 171))
        self.line_12.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_12.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_12.setObjectName("line_12")
        self.label_9 = QtWidgets.QLabel(Main_Menu)
        self.label_9.setGeometry(QtCore.QRect(20, 410, 41, 29))
        self.label_9.setStyleSheet("font: 20pt \"mr_FranklinGothicG\";")
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(Main_Menu)
        self.label_10.setGeometry(QtCore.QRect(20, 440, 41, 29))
        self.label_10.setStyleSheet("font: 20pt \"mr_FranklinGothicG\";")
        self.label_10.setObjectName("label_10")
        self.label_11 = QtWidgets.QLabel(Main_Menu)
        self.label_11.setGeometry(QtCore.QRect(20, 470, 46, 29))
        self.label_11.setStyleSheet("font: 20pt \"mr_FranklinGothicG\";")
        self.label_11.setObjectName("label_11")
        self.label_12 = QtWidgets.QLabel(Main_Menu)
        self.label_12.setGeometry(QtCore.QRect(20, 500, 48, 29))
        self.label_12.setStyleSheet("font: 20pt \"mr_FranklinGothicG\";")
        self.label_12.setObjectName("label_12")
        self.pushButton_6 = QtWidgets.QPushButton(Main_Menu)
        self.pushButton_6.setGeometry(QtCore.QRect(80, 410, 41, 21))
        self.pushButton_6.setStyleSheet("QPushButton{\n"
"  color: white;\n"
"  background-color: rgb(30,30,30);\n"
"  width: 75px;\n"
"  height: 50px;\n"
"  font-size: 14px;\n"
"  font-weight: bold;\n"
"  border: none;\n"
"  text-align: center;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"  background-color: rgb(35,35,35);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"  background-color: rgb(45,45,45);\n"
"}")
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_7 = QtWidgets.QPushButton(Main_Menu)
        self.pushButton_7.setGeometry(QtCore.QRect(130, 410, 41, 21))
        self.pushButton_7.setStyleSheet("QPushButton{\n"
"  color: white;\n"
"  background-color: rgb(30,30,30);\n"
"  width: 75px;\n"
"  height: 50px;\n"
"  font-size: 14px;\n"
"  font-weight: bold;\n"
"  border: none;\n"
"  text-align: center;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"  background-color: rgb(35,35,35);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"  background-color: rgb(45,45,45);\n"
"}")
        self.pushButton_7.setObjectName("pushButton_7")
        self.pushButton_8 = QtWidgets.QPushButton(Main_Menu)
        self.pushButton_8.setGeometry(QtCore.QRect(80, 500, 41, 21))
        self.pushButton_8.setStyleSheet("QPushButton{\n"
"  color: white;\n"
"  background-color: rgb(30,30,30);\n"
"  width: 75px;\n"
"  height: 50px;\n"
"  font-size: 14px;\n"
"  font-weight: bold;\n"
"  border: none;\n"
"  text-align: center;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"  background-color: rgb(35,35,35);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"  background-color: rgb(45,45,45);\n"
"}")
        self.pushButton_8.setObjectName("pushButton_8")
        self.pushButton_9 = QtWidgets.QPushButton(Main_Menu)
        self.pushButton_9.setGeometry(QtCore.QRect(130, 500, 41, 21))
        self.pushButton_9.setStyleSheet("QPushButton{\n"
"  color: white;\n"
"  background-color: rgb(30,30,30);\n"
"  width: 75px;\n"
"  height: 50px;\n"
"  font-size: 14px;\n"
"  font-weight: bold;\n"
"  border: none;\n"
"  text-align: center;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"  background-color: rgb(35,35,35);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"  background-color: rgb(45,45,45);\n"
"}")
        self.pushButton_9.setObjectName("pushButton_9")
        self.pushButton_10 = QtWidgets.QPushButton(Main_Menu)
        self.pushButton_10.setGeometry(QtCore.QRect(80, 470, 41, 21))
        self.pushButton_10.setStyleSheet("QPushButton{\n"
"  color: white;\n"
"  background-color: rgb(30,30,30);\n"
"  width: 75px;\n"
"  height: 50px;\n"
"  font-size: 14px;\n"
"  font-weight: bold;\n"
"  border: none;\n"
"  text-align: center;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"  background-color: rgb(35,35,35);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"  background-color: rgb(45,45,45);\n"
"}")
        self.pushButton_10.setObjectName("pushButton_10")
        self.pushButton_11 = QtWidgets.QPushButton(Main_Menu)
        self.pushButton_11.setGeometry(QtCore.QRect(130, 470, 41, 21))
        self.pushButton_11.setStyleSheet("QPushButton{\n"
"  color: white;\n"
"  background-color: rgb(30,30,30);\n"
"  width: 75px;\n"
"  height: 50px;\n"
"  font-size: 14px;\n"
"  font-weight: bold;\n"
"  border: none;\n"
"  text-align: center;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"  background-color: rgb(35,35,35);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"  background-color: rgb(45,45,45);\n"
"}")
        self.pushButton_11.setObjectName("pushButton_11")
        self.pushButton_12 = QtWidgets.QPushButton(Main_Menu)
        self.pushButton_12.setGeometry(QtCore.QRect(80, 440, 41, 21))
        self.pushButton_12.setStyleSheet("QPushButton{\n"
"  color: white;\n"
"  background-color: rgb(30,30,30);\n"
"  width: 75px;\n"
"  height: 50px;\n"
"  font-size: 14px;\n"
"  font-weight: bold;\n"
"  border: none;\n"
"  text-align: center;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"  background-color: rgb(35,35,35);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"  background-color: rgb(45,45,45);\n"
"}")
        self.pushButton_12.setObjectName("pushButton_12")
        self.pushButton_13 = QtWidgets.QPushButton(Main_Menu)
        self.pushButton_13.setGeometry(QtCore.QRect(130, 440, 41, 21))
        self.pushButton_13.setStyleSheet("QPushButton{\n"
"  color: white;\n"
"  background-color: rgb(30,30,30);\n"
"  width: 75px;\n"
"  height: 50px;\n"
"  font-size: 14px;\n"
"  font-weight: bold;\n"
"  border: none;\n"
"  text-align: center;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"  background-color: rgb(35,35,35);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"  background-color: rgb(45,45,45);\n"
"}")
        self.pushButton_13.setObjectName("pushButton_13")
        self.line_13 = QtWidgets.QFrame(Main_Menu)
        self.line_13.setGeometry(QtCore.QRect(170, 370, 20, 171))
        self.line_13.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_13.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_13.setObjectName("line_13")
        self.line_14 = QtWidgets.QFrame(Main_Menu)
        self.line_14.setGeometry(QtCore.QRect(130, 360, 51, 21))
        self.line_14.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_14.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_14.setObjectName("line_14")
        self.line_15 = QtWidgets.QFrame(Main_Menu)
        self.line_15.setGeometry(QtCore.QRect(10, 360, 51, 21))
        self.line_15.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_15.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_15.setObjectName("line_15")
        self.label_13 = QtWidgets.QLabel(Main_Menu)
        self.label_13.setGeometry(QtCore.QRect(250, 350, 52, 38))
        self.label_13.setStyleSheet("font: 24pt \"mr_Franklin GothicG\";")
        self.label_13.setObjectName("label_13")
        self.pushButton_15 = QtWidgets.QPushButton(Main_Menu)
        self.pushButton_15.setGeometry(QtCore.QRect(200, 460, 151, 31))
        self.pushButton_15.setStyleSheet("QPushButton{\n"
"  color: white;\n"
"  background-color: rgb(30,30,30);\n"
"  width: 75px;\n"
"  height: 50px;\n"
"  font-size: 14px;\n"
"  font-weight: bold;\n"
"  border: none;\n"
"  text-align: center;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"  background-color: rgb(35,35,35);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"  background-color: rgb(45,45,45);\n"
"}")
        self.pushButton_15.setObjectName("pushButton_15")
        self.pushButton_16 = QtWidgets.QPushButton(Main_Menu)
        self.pushButton_16.setGeometry(QtCore.QRect(200, 500, 151, 31))
        self.pushButton_16.setStyleSheet("QPushButton{\n"
"  color: white;\n"
"  background-color: rgb(30,30,30);\n"
"  width: 75px;\n"
"  height: 50px;\n"
"  font-size: 12px;\n"
"  font-weight: bold;\n"
"  border: none;\n"
"  text-align: center;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"  background-color: rgb(35,35,35);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"  background-color: rgb(45,45,45);\n"
"}")
        self.pushButton_16.setObjectName("pushButton_16")
        self.line_16 = QtWidgets.QFrame(Main_Menu)
        self.line_16.setGeometry(QtCore.QRect(180, 370, 20, 171))
        self.line_16.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_16.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_16.setObjectName("line_16")
        self.line_17 = QtWidgets.QFrame(Main_Menu)
        self.line_17.setGeometry(QtCore.QRect(190, 530, 171, 20))
        self.line_17.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_17.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_17.setObjectName("line_17")
        self.line_18 = QtWidgets.QFrame(Main_Menu)
        self.line_18.setGeometry(QtCore.QRect(350, 370, 20, 171))
        self.line_18.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_18.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_18.setObjectName("line_18")
        self.line_19 = QtWidgets.QFrame(Main_Menu)
        self.line_19.setGeometry(QtCore.QRect(190, 360, 51, 21))
        self.line_19.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_19.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_19.setObjectName("line_19")
        self.line_20 = QtWidgets.QFrame(Main_Menu)
        self.line_20.setGeometry(QtCore.QRect(310, 360, 51, 21))
        self.line_20.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_20.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_20.setObjectName("line_20")
        self.label_14 = QtWidgets.QLabel(Main_Menu)
        self.label_14.setGeometry(QtCore.QRect(230, 190, 89, 38))
        self.label_14.setStyleSheet("font: 24pt \"mr_Franklin GothicG\";")
        self.label_14.setObjectName("label_14")
        self.line_21 = QtWidgets.QFrame(Main_Menu)
        self.line_21.setGeometry(QtCore.QRect(190, 330, 171, 20))
        self.line_21.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_21.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_21.setObjectName("line_21")
        self.line_22 = QtWidgets.QFrame(Main_Menu)
        self.line_22.setGeometry(QtCore.QRect(180, 210, 20, 131))
        self.line_22.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_22.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_22.setObjectName("line_22")
        self.line_23 = QtWidgets.QFrame(Main_Menu)
        self.line_23.setGeometry(QtCore.QRect(190, 200, 31, 21))
        self.line_23.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_23.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_23.setObjectName("line_23")
        self.label_15 = QtWidgets.QLabel(Main_Menu)
        self.label_15.setGeometry(QtCore.QRect(200, 230, 58, 29))
        self.label_15.setStyleSheet("font: 20pt \"mr_FranklinGothicG\";")
        self.label_15.setObjectName("label_15")
        self.lineEdit_2 = QtWidgets.QLineEdit(Main_Menu)
        self.lineEdit_2.setGeometry(QtCore.QRect(260, 230, 61, 31))
        self.lineEdit_2.setStyleSheet("font: 18pt \"mr_Franklin GothicG\";\n"
"color: white;\n"
"background-color: rgb(25,25,25);")
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.pushButton_17 = QtWidgets.QPushButton(Main_Menu)
        self.pushButton_17.setGeometry(QtCore.QRect(200, 270, 151, 21))
        self.pushButton_17.setStyleSheet("QPushButton{\n"
"  color: white;\n"
"  background-color: rgb(30,30,30);\n"
"  width: 75px;\n"
"  height: 50px;\n"
"  font-size: 14px;\n"
"  font-weight: bold;\n"
"  border: none;\n"
"  text-align: center;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"  background-color: rgb(35,35,35);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"  background-color: rgb(45,45,45);\n"
"}")
        self.pushButton_17.setObjectName("pushButton_17")
        self.pushButton_18 = QtWidgets.QPushButton(Main_Menu)
        self.pushButton_18.setGeometry(QtCore.QRect(200, 300, 151, 31))
        self.pushButton_18.setStyleSheet("QPushButton{\n"
"  color: white;\n"
"  background-color: rgb(30,30,30);\n"
"  width: 75px;\n"
"  height: 50px;\n"
"  font-size: 14px;\n"
"  font-weight: bold;\n"
"  border: none;\n"
"  text-align: center;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"  background-color: rgb(35,35,35);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"  background-color: rgb(45,45,45);\n"
"}")
        self.pushButton_18.setObjectName("pushButton_18")
        self.line_24 = QtWidgets.QFrame(Main_Menu)
        self.line_24.setGeometry(QtCore.QRect(350, 210, 20, 131))
        self.line_24.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_24.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_24.setObjectName("line_24")
        self.line_25 = QtWidgets.QFrame(Main_Menu)
        self.line_25.setGeometry(QtCore.QRect(330, 200, 31, 21))
        self.line_25.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_25.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_25.setObjectName("line_25")
        self.pushButton_19 = QtWidgets.QPushButton(Main_Menu)
        self.pushButton_19.setGeometry(QtCore.QRect(200, 420, 151, 31))
        self.pushButton_19.setStyleSheet("QPushButton{\n"
"  color: white;\n"
"  background-color: rgb(30,30,30);\n"
"  width: 75px;\n"
"  height: 50px;\n"
"  font-size: 14px;\n"
"  font-weight: bold;\n"
"  border: none;\n"
"  text-align: center;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"  background-color: rgb(35,35,35);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"  background-color: rgb(45,45,45);\n"
"}")
        self.pushButton_19.setObjectName("pushButton_19")
        self.pushButton_20 = QtWidgets.QPushButton(Main_Menu)
        self.pushButton_20.setGeometry(QtCore.QRect(200, 390, 151, 21))
        self.pushButton_20.setStyleSheet("QPushButton{\n"
"  color: white;\n"
"  background-color: rgb(30,30,30);\n"
"  width: 75px;\n"
"  height: 50px;\n"
"  font-size: 14px;\n"
"  font-weight: bold;\n"
"  border: none;\n"
"  text-align: center;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"  background-color: rgb(35,35,35);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"  background-color: rgb(45,45,45);\n"
"}")
        self.pushButton_20.setObjectName("pushButton_20")
        self.pushButton_14 = QtWidgets.QPushButton(Main_Menu)
        self.pushButton_14.setGeometry(QtCore.QRect(330, 230, 21, 31))
        self.pushButton_14.setStyleSheet("QPushButton{\n"
"  color: white;\n"
"  background-color: rgb(30,30,30);\n"
"  width: 75px;\n"
"  height: 50px;\n"
"  font-size: 14px;\n"
"  font-weight: bold;\n"
"  border: none;\n"
"  text-align: center;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"  background-color: rgb(35,35,35);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"  background-color: rgb(45,45,45);\n"
"}")
        self.pushButton_14.setObjectName("pushButton_14")
        self.label_16 = QtWidgets.QLabel(Main_Menu)
        self.label_16.setGeometry(QtCore.QRect(190, -10, 141, 200))
        self.label_16.setText("")
        self.label_16.setPixmap(QtGui.QPixmap("res/Fon.png"))
        self.label_16.setObjectName("label_16")
        self.backgr.raise_()
        self.label.raise_()
        self.label_4.raise_()
        self.label_5.raise_()
        self.comboBox_1.raise_()
        self.comboBox_2.raise_()
        self.label_6.raise_()
        self.comboBox_3.raise_()
        self.line.raise_()
        self.line_2.raise_()
        self.line_3.raise_()
        self.line_4.raise_()
        self.line_5.raise_()
        self.label_2.raise_()
        self.label_7.raise_()
        self.lineEdit.raise_()
        self.label_8.raise_()
        self.pushButton_3.raise_()
        self.line_6.raise_()
        self.line_7.raise_()
        self.line_8.raise_()
        self.line_9.raise_()
        self.line_10.raise_()
        self.label_3.raise_()
        self.line_11.raise_()
        self.line_12.raise_()
        self.label_9.raise_()
        self.label_10.raise_()
        self.label_11.raise_()
        self.label_12.raise_()
        self.line_13.raise_()
        self.line_14.raise_()
        self.line_15.raise_()
        self.label_13.raise_()
        self.line_16.raise_()
        self.line_17.raise_()
        self.line_18.raise_()
        self.line_19.raise_()
        self.line_20.raise_()
        self.label_14.raise_()
        self.line_21.raise_()
        self.line_22.raise_()
        self.line_23.raise_()
        self.label_15.raise_()
        self.lineEdit_2.raise_()
        self.line_24.raise_()
        self.line_25.raise_()
        self.label_16.raise_()
        self.pushButton_1.raise_()
        self.pushButton_2.raise_()
        self.pushButton_4.raise_()
        self.pushButton_5.raise_()
        self.pushButton_6.raise_()
        self.pushButton_7.raise_()
        self.pushButton_12.raise_()
        self.pushButton_13.raise_()
        self.pushButton_10.raise_()
        self.pushButton_11.raise_()
        self.pushButton_8.raise_()
        self.pushButton_9.raise_()
        self.pushButton_16.raise_()
        self.pushButton_15.raise_()
        self.pushButton_19.raise_()
        self.pushButton_20.raise_()
        self.pushButton_18.raise_()
        self.pushButton_17.raise_()
        self.pushButton_14.raise_()

        self.retranslateUi(Main_Menu)
        QtCore.QMetaObject.connectSlotsByName(Main_Menu)

    def retranslateUi(self, Main_Menu):
        Main_Menu.setWindowTitle(_translate("Main_Menu", "DupliDup | Создатель: L1mPeX"))
        self.label.setText(_translate("Main_Menu", "<html><head/><body><p><span style=\" color:#0055ff;\">WallHack</span></p></body></html>"))
        self.label_4.setText(_translate("Main_Menu", "<html><head/><body><p><span style=\" font-size:18pt; color:#00ff00;\">T</span></p></body></html>"))
        self.label_5.setText(_translate("Main_Menu", "<html><head/><body><p><span style=\" font-size:18pt; color:#00ff00;\">CT</span></p></body></html>"))
        self.comboBox_1.setItemText(0, _translate("Main_Menu", "Красный"))
        self.comboBox_1.setItemText(1, _translate("Main_Menu", "Синий"))
        self.comboBox_1.setItemText(2, _translate("Main_Menu", "Зеленый"))
        self.comboBox_1.setItemText(3, _translate("Main_Menu", "Желтый"))
        self.comboBox_1.setItemText(4, _translate("Main_Menu", "Белый"))
        self.comboBox_1.setItemText(5, _translate("Main_Menu", "Голубой"))
        self.comboBox_1.setItemText(6, _translate("Main_Menu", "Розовый"))
        self.comboBox_1.setItemText(7, _translate("Main_Menu", "Без подсветки"))
        self.comboBox_2.setItemText(0, _translate("Main_Menu", "Синий"))
        self.comboBox_2.setItemText(1, _translate("Main_Menu", "Красный"))
        self.comboBox_2.setItemText(2, _translate("Main_Menu", "Зеленый"))
        self.comboBox_2.setItemText(3, _translate("Main_Menu", "Желтый"))
        self.comboBox_2.setItemText(4, _translate("Main_Menu", "Белый"))
        self.comboBox_2.setItemText(5, _translate("Main_Menu", "Голубой"))
        self.comboBox_2.setItemText(6, _translate("Main_Menu", "Розовый"))
        self.comboBox_2.setItemText(7, _translate("Main_Menu", "Без подсветки"))
        self.label_6.setText(_translate("Main_Menu", "<html><head/><body><p><span style=\" font-size:18pt; color:#ffff00;\">Type</span></p></body></html>"))
        self.comboBox_3.setItemText(0, _translate("Main_Menu", "Glow_ESP"))
        self.comboBox_3.setItemText(1, _translate("Main_Menu", "Chams"))
        self.pushButton_1.setText(_translate("Main_Menu", "ON"))
        self.pushButton_2.setText(_translate("Main_Menu", "OFF"))
        self.label_2.setText(_translate("Main_Menu", "<html><head/><body><p><span style=\" color:#0055ff;\">TrigerBot</span></p></body></html>"))
        self.label_7.setText(_translate("Main_Menu", "<html><head/><body><p><span style=\" font-size:18pt; color:#ffff00;\">Delay: </span></p></body></html>"))
        self.lineEdit.setText(_translate("Main_Menu", "0.1"))
        self.pushButton_4.setText(_translate("Main_Menu", "ON"))
        self.pushButton_5.setText(_translate("Main_Menu", "OFF"))
        self.label_3.setText(_translate("Main_Menu", "<html><head/><body><p><span style=\" color:#0055ff;\">Misc</span></p></body></html>"))
        self.label_9.setText(_translate("Main_Menu", "<html><head/><body><p><span style=\" font-size:18pt; color:#ffff00;\">Bhop </span></p></body></html>"))
        self.label_10.setText(_translate("Main_Menu", "<html><head/><body><p><span style=\" font-size:18pt; color:#ffff00;\">Radar</span></p></body></html>"))
        self.label_11.setText(_translate("Main_Menu", "<html><head/><body><p><span style=\" font-size:18pt; color:#ffff00;\">NFlash</span></p></body></html>"))
        self.label_12.setText(_translate("Main_Menu", "<html><head/><body><p><span style=\" font-size:18pt; color:#ffff00;\">Accept</span></p></body></html>"))
        self.pushButton_6.setText(_translate("Main_Menu", "ON"))
        self.pushButton_7.setText(_translate("Main_Menu", "OFF"))
        self.pushButton_8.setText(_translate("Main_Menu", "ON"))
        self.pushButton_9.setText(_translate("Main_Menu", "OFF"))
        self.pushButton_10.setText(_translate("Main_Menu", "ON"))
        self.pushButton_11.setText(_translate("Main_Menu", "OFF"))
        self.pushButton_12.setText(_translate("Main_Menu", "ON"))
        self.pushButton_13.setText(_translate("Main_Menu", "OFF"))
        self.label_13.setText(_translate("Main_Menu", "<html><head/><body><p><span style=\" color:#0055ff;\">Game</span></p></body></html>"))
        self.pushButton_15.setText(_translate("Main_Menu", "Скачать оффсеты"))
        self.pushButton_16.setText(_translate("Main_Menu", "Автономные оффсеты"))
        self.label_14.setText(_translate("Main_Menu", "<html><head/><body><p><span style=\" color:#0055ff;\">Perilously</span></p></body></html>"))
        self.label_15.setText(_translate("Main_Menu", "<html><head/><body><p><span style=\" font-size:18pt; color:#ffff00;\">FOV_P: </span></p></body></html>"))
        self.lineEdit_2.setText(_translate("Main_Menu", "90"))
        self.pushButton_17.setText(_translate("Main_Menu", "Показать деньги"))
        self.pushButton_18.setText(_translate("Main_Menu", "Консольное ВХ"))
        self.pushButton_19.setText(_translate("Main_Menu", "> Подключиться <"))
        self.pushButton_20.setText(_translate("Main_Menu", "Отключить все"))
        self.pushButton_14.setText(_translate("Main_Menu", "<"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Main_Menu = QtWidgets.QWidget()
    ui = Ui_Main_Menu()
    ui.setupUi(Main_Menu)
    Main_Menu.show()

    def Connect_Game():
    	try:
    		global pm,client,engine
    		pm = pymem.Pymem("csgo.exe")
    		client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll
    		engine = pymem.process.module_from_name(pm.process_handle, "engine.dll").lpBaseOfDll
    		ui.pushButton_19.setText(_translate("Main_Menu", "> Подключено <"))
    	except:
    		ctypes.windll.user32.MessageBoxW (None, 'Не удалось получить доступ к процессу - csgo.exe.', 'Ошибка', 0)
    		ui.pushButton_19.setText(_translate("Main_Menu", "> Подключиться <"))

    def DownOffsets():
    	global dwLocalPlayer, dwGlowObjectManager, dwEntityList, dwForceAttack, dwForceJump, m_iCrosshairId, m_iTeamNum, m_iGlowIndex, m_fFlags, m_bSpotted, m_flFlashMaxAlpha, m_clrRender
    		
    	try:
    		url = 'https://raw.githubusercontent.com/frk1/hazedumper/master/csgo.json'
    		response = requests.get(url).json()

    		dwLocalPlayer       = int(response["signatures"]["dwLocalPlayer"])
    		dwGlowObjectManager = int(response["signatures"]["dwGlowObjectManager"])
    		dwEntityList        = int(response["signatures"]["dwEntityList"])
    		dwForceAttack       = int(response["signatures"]["dwForceAttack"])
    		dwForceJump         = int(response["signatures"]["dwForceJump"])

    		m_iCrosshairId      = int(response["netvars"]["m_iCrosshairId"])
    		m_iTeamNum          = int(response["netvars"]["m_iTeamNum"])
    		m_iGlowIndex        = int(response["netvars"]["m_iGlowIndex"])
    		m_fFlags            = int(response["netvars"]["m_fFlags"])
    		m_bSpotted          = int(response["netvars"]["m_bSpotted"])
    		m_clrRender         = int(response["netvars"]["m_clrRender"])
    		print (dwLocalPlayer, dwGlowObjectManager, dwEntityList, dwForceAttack, dwForceJump, m_iCrosshairId, m_iTeamNum, m_iGlowIndex, m_fFlags, m_bSpotted, m_flFlashMaxAlpha, m_clrRender)
    	except:
    		ctypes.windll.user32.MessageBoxW (None, 'Не удалось получить доступ к сетевому файлу - https://raw.githubusercontent.com/frk1/hazedumper/master/csgo.json', 'Ошибка', 0)
    
    def AutoOffsets():
    	# < Спасибо minicx :D >
    	global dwLocalPlayer, dwGlowObjectManager, dwEntityList, dwForceAttack, dwForceJump

    	dwLocalPlayer       = int(get_sig('client.dll', rb'\x8D\x34\x85....\x89\x15....\x8B\x41\x08\x8B\x48\x04\x83\xF9\xFF', 4, 3), 0)
    	dwGlowObjectManager = int(get_sig('client.dll', rb'\xA1....\xA8\x01\x75\x4B', 4, 1),0)
    	dwEntityList        = int(get_sig('client.dll',rb'\xBB....\x83\xFF\x01\x0F\x8C....\x3B\xF8',0,1),0)
    	dwForceAttack       = int(get_sig('client.dll', rb'\x89\x0D....\x8B\x0D....\x8B\xF2\x8B\xC1\x83\xCE\x04', 0, 2), 0)
    	dwForceJump         = int(get_sig('client.dll', rb'\x8B\x0D....\x8B\xD6\x8B\xC1\x83\xCA\x02', 0, 2), 0)

    	print (dwLocalPlayer, dwGlowObjectManager, dwEntityList, dwForceAttack, dwForceJump)

    def WallHack():
    	global Glow_E, Cham_s
    	Glow_E = False
    	Cham_s = False


    	check = ui.comboBox_3.currentText()
    	print (check)
    	Color()

    	if check == 'Glow_ESP':
    		Thread(target=ESP).start()
    	else:
    		Thread(target=Chams_f).start()
    		

    def WallHack_Stop():
    	global Glow_E, Cham_s
    	check = ui.comboBox_3.currentText()
    	print (check)

    	if check == 'Glow_ESP':
    		Glow_E = True
    	else:
    		Cham_s = True
    		ctypes.windll.user32.MessageBoxW (None, 'Chams нельзя отключить :/', 'Преколяс', 0)

    		
    def TrigerBot():
    	global TrigerB, Triger_T
    	TrigerB = False
    	Triger_T = float(ui.lineEdit.text())
    	print (Triger_T)
    	Thread(target=TrigerBo_t).start()

    def TrigerBot_Stop():
    	global TrigerB
    	TrigerB = True

    def BunnyHop():
    	global BHo_p
    	BHo_p = False
    	Thread(target=BunnyHo_p).start()

    def BunnyHop_Stop():
    	global BHo_p
    	BHo_p = True

    def RadarHack():
    	global Radar_H
    	Radar_H = False
    	Thread(target=RadarHac_k).start()

    def RadarHack_Stop():
    	global Radar_H
    	Radar_H = True

    def NOF1ash():
    	ctypes.windll.user32.MessageBoxW (None, 'NOFlash не работает :(', 'Преколяс№2', 0)

    def NOF1ash_Stop():
    	ctypes.windll.user32.MessageBoxW (None, 'NOFlash не работает :(', 'Преколяс№2', 0)

    def AutoAccept():
    	global Auto
    	Auto = False
    	Thread(target=AutoAccep_t).start()

    def AutoAccept_Stop():
    	global Auto
    	Auto = True

    def FOV_P():
    	global fov
    	fov = int(ui.lineEdit_2.text())
    	Thread(target=FOVP).start()

    def ShowM():
    	pm = pymem.Pymem('csgo.exe')
    	client = pymem.process.module_from_name(pm.process_handle,'client.dll')
    	clientModule = pm.read_bytes(client.lpBaseOfDll, client.SizeOfImage)
    	address = client.lpBaseOfDll + re.search(rb'.\x0C\x5B\x5F\xB8\xFB\xFF\xFF\xFF',clientModule).start()
    	pm.write_uchar(address, 0xEB if pm.read_uchar(address) == 0x75 else 0x75)
    	pm.close_process()

    def CMD_WH():
    	pm = pymem.Pymem('csgo.exe')
    	client = pymem.process.module_from_name(pm.process_handle,'client.dll')
    	clientModule = pm.read_bytes(client.lpBaseOfDll, client.SizeOfImage)
    	address = client.lpBaseOfDll + re.search(rb'\x83\xF8.\x8B\x45\x08\x0F',clientModule).start() + 2
    	pm.write_uchar(address, 2 if pm.read_uchar(address) == 1 else 1)
    	pm.close_process()

    def gl_off():
    	WallHack_Stop()
    	TrigerBot_Stop()
    	AutoAccept_Stop()
    	BunnyHop_Stop()
    	RadarHack_Stop()





    ui.pushButton_1.clicked.connect(WallHack)
    ui.pushButton_2.clicked.connect(WallHack_Stop)
    ui.pushButton_4.clicked.connect(TrigerBot)
    ui.pushButton_5.clicked.connect(TrigerBot_Stop)
    ui.pushButton_8.clicked.connect(AutoAccept)
    ui.pushButton_9.clicked.connect(AutoAccept_Stop)

    ui.pushButton_6.clicked.connect(BunnyHop)
    ui.pushButton_7.clicked.connect(BunnyHop_Stop)
    ui.pushButton_10.clicked.connect(NF1ash)
    ui.pushButton_11.clicked.connect(NOF1ash_Stop)
    ui.pushButton_12.clicked.connect(RadarHack)
    ui.pushButton_13.clicked.connect(RadarHack_Stop)
    ui.pushButton_14.clicked.connect(FOV_P)
    ui.pushButton_19.clicked.connect(Connect_Game)
    ui.pushButton_15.clicked.connect(DownOffsets)
    ui.pushButton_16.clicked.connect(AutoOffsets)
    ui.pushButton_17.clicked.connect(ShowM)
    ui.pushButton_18.clicked.connect(CMD_WH)
    sys.exit(app.exec_())
