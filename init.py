"""
Copyright 2023 JZH工作室
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import json, sys, urllib.request, hashlib, time, yara, shutil, psutil, ctypes, win32gui_struct, win32gui
import threading, urllib.parse, numpy, onnxruntime, pefile, urllib.parse, subprocess, win32api, win32con
import tkintertools as tkt
from pefile import *
from hashlib import md5
import xml.etree.ElementTree as et
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from PIL import Image
import tkinter as tk
import winreg as reg
from tkinter import messagebox
from tkinter import ttk, filedialog

# 开发环境检测 & 获取TrustedInstaller权限
try:
    ide = sys.argv[0].split(".py")[1] == ""
except:
    ide = False
def TrustedInstaller():
    def is_admin():
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    if is_admin():
        pass
    else:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        sys.exit()
if not ide:
    TrustedInstaller()

# 启动主防 & 显示加载界面
def OpenLoadingScreen():
    LoadingScreen = open("4.txt", "w")
    LoadingScreen.write("1")
    LoadingScreen.close()
def OffLoadingScreen():
    try:
        os.remove("4.txt")
    except:
        pass
OpenLoadingScreen()
subprocess.Popen(f'{os.path.dirname(sys.argv[0]) + "\\JZHSDZhuDongFangYu.exe"}', creationflags=subprocess.CREATE_NO_WINDOW)

# 免杀（拒绝kill我的进程）
rtcore64_sys = os.path.dirname(sys.argv[0]) + "\\RTCore64.sys"
rtcore64_exe = os.path.dirname(sys.argv[0]) + "\\PPLcontrol.exe"
def on_rtcore64(pid):
    try:
        creation_flags = subprocess.CREATE_NO_WINDOW
        subprocess.run(
            f'sc create RTCore64 type= kernel start= auto binPath= "{rtcore64_sys}" DisplayName= "Micro - Star MSI Afterburner"',
            check=True, shell=True, creationflags=creation_flags
        )
        subprocess.run('net start RTCore64', check=True, shell=True, creationflags=creation_flags)
        subprocess.run(f'"{rtcore64_exe}" set {pid} PP WinSystem', check=True, shell=True, creationflags=creation_flags)
        subprocess.run('net stop RTCore64', check=True, shell=True, creationflags=creation_flags)
        subprocess.run('sc.exe delete RTCore64', check=True, shell=True, creationflags=creation_flags)
    except:
        try:
            subprocess.run('net stop RTCore64', check=True, shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
        except:
            pass
        try:
            subprocess.run('sc.exe delete RTCore64', check=True, shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
        except:
            pass
def off_rtcore64(pid):
    try:
        creation_flags = subprocess.CREATE_NO_WINDOW
        subprocess.run(
            f'sc create RTCore64 type= kernel start= auto binPath= "{rtcore64_sys}" DisplayName= "Micro - Star MSI Afterburner"',
            check=True, shell=True, creationflags=creation_flags
        )
        subprocess.run('net start RTCore64', check=True, shell=True, creationflags=creation_flags)
        subprocess.run(f'"{rtcore64_exe}" unprotect {pid}', check=True, shell=True, creationflags=creation_flags)
        subprocess.run('net stop RTCore64', check=True, shell=True, creationflags=creation_flags)
        subprocess.run('sc.exe delete RTCore64', check=True, shell=True, creationflags=creation_flags)
    except:
        try:
            subprocess.run('net stop RTCore64', check=True, shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
        except:
            pass
        try:
            subprocess.run('sc.exe delete RTCore64', check=True, shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
        except:
            pass
for proc in psutil.process_iter(['pid', 'name', 'exe']):
    try:
        exe = proc.info['exe']
        if ide:
            if "python" in os.path.basename(exe):
                on_rtcore64(proc.pid)
        else:
            if os.path.basename(sys.argv[0]) == os.path.basename(exe):
                on_rtcore64(proc.pid)
    except:
        pass

# 准备 & 部分功能UI(会被调用)
if not ide:
    script_path = sys.argv[0]
    key = r"Software\Microsoft\Windows\CurrentVersion\Run"
    reg_key = reg.OpenKey(reg.HKEY_CURRENT_USER, key, 0, reg.KEY_WRITE)
    reg.SetValueEx(reg_key, "jzh杀毒", 0, reg.REG_SZ, script_path)
    reg.CloseKey(reg_key)
    script_path = sys.argv[0]
    # 注册表位置
    key = r"Software\Microsoft\Windows\CurrentVersion\Run"
    # 获取注册表的键值
    reg_key = reg.OpenKey(reg.HKEY_CURRENT_USER, key, 0, reg.KEY_WRITE)
    # 添加开机启动项
    reg.SetValueEx(reg_key, "JZH杀毒", 0, reg.REG_SZ, script_path)
    reg.CloseKey(reg_key)
try:
    with urllib.request.urlopen("http://www.msftconnecttest.com/connecttest.txt", timeout=5) as response:
        content = response.read().decode('utf-8')
        if "Microsoft Connect Test" in content:
            msftconnecttest = True
        else:
            msftconnecttest = False
except:
    msftconnecttest = False
try:
    with urllib.request.urlopen("https://elec.bilibili.com/", timeout=5) as response:
        content = response.read().decode('utf-8')
        if "hello elec !" in content:
            bilibili = True
        else:
            bilibili = False
except:
    bilibili = False
try:
    with urllib.request.urlopen("https://www.xn--jzh-k69dm57c4fd.xyz/connecttest.txt",
                                timeout=5) as response:
        content = response.read().decode('utf-8')
        if "Jzh Connect Test" in content:
            jzh = True
        else:
            jzh = False
except:
    jzh = False
online = msftconnecttest or bilibili or jzh
Viruses_White_exe = []
def Get_VirusesWhite():
    def delete_line(line_number):
        with open('1.txt', 'r') as file:
            lines = file.readlines()
        lines.pop(line_number - 1)
        with open('1.txt', 'w') as file:
            file.writelines(lines)

    try:
        f = open("1.txt", "r")
        m = f.read()
        f.close()
        if m[0] == '\n':
            delete_line(1)
    except:
        pass
    Viruses_White_f = open('1.txt', 'r')
    Viruses_white_fp = Viruses_White_f.read().split("\n")
    Viruses_White_f.close()
    for d in Viruses_white_fp:
        if not d == '':
            Viruses_White_exe.append(d.replace("/", "\\"))
Get_VirusesWhite()

#杀毒引擎 & 被动防御
class AntivirusEngine:
    def init_data_base(self):
        try:
            self.pyas = sys.argv[0].replace("\\", "/")
            self.dir = os.path.dirname(self.pyas)
            file_path = os.path.join(self.dir, "Model.json")
            if os.path.exists(file_path):
                self.pe = ListSimHash()
                self.pe.load_model(file_path)
        except:
            pass
    def __init__(self):
        self.p = 0
    def test(self, a):
        return True
    def AdobeMalwareClassifier_scan(self, f):
        if f.replace("/", "\\") in Viruses_White_exe:
            return False
        class PEFile:
            def __init__(self, filename):
                self.pe = pefile.PE(filename, fast_load=True)
                self.filename = filename
                self.DebugSize = self.pe.OPTIONAL_HEADER.DATA_DIRECTORY[6].Size
                self.ImageVersion = ((
                                             self.pe.OPTIONAL_HEADER.MajorImageVersion * 100) + self.pe.OPTIONAL_HEADER.MinorImageVersion) * 1000
                self.IatRVA = self.pe.OPTIONAL_HEADER.DATA_DIRECTORY[1].VirtualAddress
                self.ExportSize = self.pe.OPTIONAL_HEADER.DATA_DIRECTORY[0].Size
                self.ResourceSize = self.pe.OPTIONAL_HEADER.DATA_DIRECTORY[2].Size
                self.VirtualSize2 = self.pe.sections[1].Misc_VirtualSize
                self.NumberOfSections = self.pe.FILE_HEADER.NumberOfSections

        scan_input = PEFile(f)

        def runRidor():
            isDirty = 0
            if scan_input.DebugSize <= 14 and scan_input.ImageVersion <= 760 and scan_input.VirtualSize2 > 992 and scan_input.ExportSize <= 80.5:
                isDirty = 1
            elif scan_input.DebugSize <= 14 and scan_input.ImageVersion <= 4525 and scan_input.ExportSize <= 198.5 and scan_input.ResourceSize <= 7348 and scan_input.VirtualSize2 <= 6 and scan_input.ResourceSize > 1773:
                isDirty = 1
            elif scan_input.DebugSize <= 14 and scan_input.ImageVersion <= 4950 and scan_input.ExportSize <= 56 and scan_input.IatRVA > 256 and scan_input.VirtualSize2 > 42 and scan_input.NumberOfSections > 3.5:
                isDirty = 1
            elif scan_input.DebugSize <= 14 and scan_input.ImageVersion <= 4950 and scan_input.VirtualSize2 <= 6 and scan_input.ResourceSize > 17302:
                isDirty = 1
            elif scan_input.DebugSize <= 14 and scan_input.NumberOfSections >= 2.5 and scan_input.ResourceSize <= 1776 and scan_input.IatRVA <= 6144 and scan_input.ExportSize <= 219.5 and 2410 < scan_input.VirtualSize2 <= 61224:
                isDirty = 1
            elif scan_input.DebugSize <= 14 and scan_input.NumberOfSections >= 2.5 and scan_input.ExportSize <= 198 and scan_input.ResourceSize > 8 and scan_input.VirtualSize2 > 83 and scan_input.ResourceSize <= 976:
                isDirty = 1
            elif scan_input.DebugSize <= 14 and scan_input.NumberOfSections >= 2.5 and scan_input.ResourceSize > 1418 and scan_input.IatRVA > 6144 and scan_input.VirtualSize2 <= 4:
                isDirty = 1
            elif scan_input.DebugSize <= 14 < scan_input.VirtualSize2 and scan_input.NumberOfSections > 4.5 and scan_input.ResourceSize > 1550 and scan_input.VirtualSize2 <= 2398:
                isDirty = 1
            elif scan_input.DebugSize <= 14 < scan_input.VirtualSize2 and scan_input.NumberOfSections > 4.5 and scan_input.ExportSize > 138.5 and scan_input.ImageVersion > 1005:
                isDirty = 1
            elif scan_input.ImageVersion <= 5005 and scan_input.DebugSize <= 14 < scan_input.VirtualSize2 and scan_input.NumberOfSections <= 4.5:
                isDirty = 1
            elif scan_input.ImageVersion <= 5005 and scan_input.DebugSize <= 14 and scan_input.ImageVersion <= 5 and scan_input.NumberOfSections > 3.5 and scan_input.ExportSize <= 164.5 and scan_input.IatRVA <= 73728 and scan_input.ResourceSize <= 8722:
                isDirty = 1
            elif scan_input.ImageVersion <= 5005 and scan_input.DebugSize <= 14 and 21108 < scan_input.ResourceSize <= 37272 and scan_input.ImageVersion <= 760:
                isDirty = 1
            elif scan_input.NumberOfSections > 4.5 and scan_input.ExportSize <= 25.5 and scan_input.ImageVersion > 1505 and scan_input.ResourceSize <= 1020:
                isDirty = 1
            elif scan_input.ImageVersion <= 1500 and scan_input.NumberOfSections > 5.5 and scan_input.ExportSize <= 101 and scan_input.ResourceSize <= 3168:
                isDirty = 1
            elif scan_input.ImageVersion <= 3025 and scan_input.DebugSize <= 14 and scan_input.ResourceSize > 1182 and scan_input.VirtualSize2 > 164 and scan_input.ExportSize <= 330.5:
                isDirty = 1
            elif scan_input.ImageVersion <= 1010 and scan_input.ResourceSize > 2352 and 115254 < scan_input.VirtualSize2 <= 153258:
                isDirty = 1
            elif scan_input.ImageVersion <= 1500 and scan_input.NumberOfSections > 5.5 and scan_input.ImageVersion <= 500 and scan_input.ExportSize <= 164 and scan_input.IatRVA <= 2048:
                isDirty = 1
            elif scan_input.ImageVersion <= 1010 and scan_input.ResourceSize <= 474 and scan_input.IatRVA > 26624 and scan_input.VirtualSize2 > 1802 and scan_input.IatRVA <= 221348:
                isDirty = 1
            elif scan_input.ImageVersion <= 2500 and scan_input.DebugSize <= 14 and 78678 < scan_input.ResourceSize <= 120928 and scan_input.NumberOfSections <= 4:
                isDirty = 1
            elif scan_input.ImageVersion <= 5005 and scan_input.ExportSize <= 25.5 and scan_input.NumberOfSections > 3.5 and scan_input.ResourceSize > 35814 and scan_input.VirtualSize2 > 215352:
                isDirty = 1
            elif scan_input.ImageVersion <= 500 and scan_input.IatRVA <= 2560 and scan_input.NumberOfSections > 3.5 and 648 < scan_input.ResourceSize <= 62291:
                isDirty = 1
            elif scan_input.ExportSize <= 25.5 and scan_input.NumberOfSections > 4.5 and scan_input.VirtualSize2 > 50765 and 741012 >= scan_input.ResourceSize > 2512:
                isDirty = 1
            elif scan_input.ImageVersion <= 1010 and scan_input.ExportSize <= 25.5 and 3278 >= scan_input.VirtualSize2 > 1200 and scan_input.ResourceSize > 2032:
                isDirty = 1
            elif scan_input.ResourceSize <= 474 and scan_input.ExportSize <= 76 and scan_input.VirtualSize2 <= 1556 and scan_input.IatRVA <= 2368:
                isDirty = 1
            elif scan_input.ImageVersion <= 1500 and scan_input.VirtualSize2 <= 6 and scan_input.IatRVA > 2048:
                isDirty = 1
            else:
                isDirty = 0
            return isDirty

        def runPART():
            isDirty = 0
            if scan_input.DebugSize > 0 and scan_input.ResourceSize > 545 and scan_input.IatRVA <= 94208 and scan_input.NumberOfSections <= 5 and scan_input.ExportSize > 0 and scan_input.NumberOfSections > 3:
                isDirty = 0
            elif scan_input.DebugSize <= 0 and scan_input.ImageVersion <= 4900 and scan_input.ExportSize <= 71 and scan_input.ImageVersion <= 520 and scan_input.VirtualSize2 > 130 and scan_input.IatRVA <= 24576:
                isDirty = 1
            elif scan_input.DebugSize <= 0 and scan_input.ImageVersion <= 4900 and scan_input.ExportSize <= 211 and scan_input.ResourceSize <= 32272 and scan_input.NumberOfSections <= 10 and scan_input.VirtualSize2 <= 5 and scan_input.ImageVersion <= 3420:
                isDirty = 1
            elif scan_input.DebugSize > 0 and scan_input.ResourceSize > 598 and 105028 >= scan_input.VirtualSize2 > 1 and scan_input.ImageVersion > 5000:
                isDirty = 0
            elif scan_input.IatRVA <= 0 and scan_input.ImageVersion > 4180 and scan_input.ResourceSize > 2484:
                isDirty = 0
            elif scan_input.DebugSize <= 0 and scan_input.NumberOfSections <= 1 and scan_input.ResourceSize > 501:
                isDirty = 0
            elif scan_input.DebugSize <= 0 and scan_input.ExportSize <= 211 and scan_input.NumberOfSections > 2 and scan_input.ImageVersion > 1000 and scan_input.ResourceSize <= 12996:
                isDirty = 1
            elif scan_input.DebugSize <= 0 and scan_input.ExportSize <= 211 and scan_input.NumberOfSections > 2 and scan_input.ResourceSize > 0 and scan_input.VirtualSize2 > 1016:
                isDirty = 1
            elif scan_input.NumberOfSections > 8 and scan_input.VirtualSize2 <= 2221:
                isDirty = 1
            elif scan_input.ResourceSize <= 736 and scan_input.NumberOfSections <= 3:
                isDirty = 1
            elif scan_input.NumberOfSections <= 3 and scan_input.IatRVA > 4156:
                isDirty = 0
            elif scan_input.ImageVersion <= 6000 and scan_input.ResourceSize <= 523 and scan_input.IatRVA > 0 and scan_input.ExportSize <= 95:
                isDirty = 1
            elif scan_input.ExportSize <= 256176 and scan_input.DebugSize > 0 and scan_input.ImageVersion <= 5450 and scan_input.IatRVA > 1664 and scan_input.ResourceSize <= 2040 and scan_input.DebugSize <= 41:
                isDirty = 0
            elif scan_input.ExportSize <= 256176 and scan_input.ImageVersion > 5450:
                isDirty = 0
            elif scan_input.ExportSize > 256176:
                isDirty = 1
            elif scan_input.ImageVersion > 0 and scan_input.ResourceSize > 298216 and scan_input.IatRVA <= 2048:
                isDirty = 1
            elif scan_input.ImageVersion > 0 and scan_input.ExportSize > 74 and scan_input.DebugSize > 0:
                isDirty = 0
            elif scan_input.ImageVersion > 0 and scan_input.VirtualSize2 > 4185 and scan_input.ResourceSize <= 215376 and scan_input.IatRVA <= 2048 and scan_input.NumberOfSections <= 5:
                isDirty = 0
            elif scan_input.ImageVersion > 1010 and scan_input.DebugSize <= 56 and scan_input.VirtualSize2 <= 215376:
                isDirty = 0
            elif scan_input.ExportSize > 258 and scan_input.NumberOfSection > 3 and scan_input.DebugSize > 0:
                isDirty = 0
            elif scan_input.ExportSize > 262 and scan_input.ImageVersion > 0 and scan_input.NumberOfSections > 7:
                isDirty = 0
            elif scan_input.DebugSize > 41 and scan_input.NumberOfSections <= 4:
                isDirty = 0
            elif scan_input.ExportSize <= 262 and scan_input.NumberOfSections > 3 and scan_input.VirtualSize2 <= 37:
                isDirty = 1
            elif scan_input.VirtualSize2 > 40 and scan_input.ExportSize <= 262 and scan_input.DebugSize <= 0 and scan_input.ImageVersion <= 353 and scan_input.ExportSize <= 142:
                isDirty = 1
            elif 72384 < scan_input.VirtualSize2 <= 263848:
                isDirty = 1
            elif 106496 < scan_input.IatRVA <= 937984 and scan_input.DebugSize > 0 and scan_input.ResourceSize > 4358:
                isDirty = 0
            elif scan_input.VirtualSize2 <= 64 and scan_input.IatRVA <= 2048 and scan_input.DebugSize <= 0 and scan_input.ImageVersion <= 353 and scan_input.ExportSize <= 0 and scan_input.VirtualSize2 <= 4 and scan_input.NumberOfSections <= 2:
                isDirty = 0
            elif scan_input.DebugSize <= 0 and scan_input.NumberOfSections <= 4 and scan_input.IatRVA > 45548:
                isDirty = 1
            elif 0 < scan_input.DebugSize <= 56 and scan_input.IatRVA <= 94208 and scan_input.ResourceSize <= 4096:
                isDirty = 1
            elif scan_input.DebugSize <= 0 and scan_input.IatRVA <= 98304 and scan_input.NumberOfSections > 6 and scan_input.ResourceSize <= 864 and scan_input.ExportSize > 74 and scan_input.ImageVersion > 353 and scan_input.ExportSize <= 279:
                isDirty = 0
            elif scan_input.DebugSize <= 0 and scan_input.IatRVA <= 98304 and scan_input.NumberOfSections <= 2 and scan_input.ResourceSize <= 1264128:
                isDirty = 1
            elif scan_input.VirtualSize2 <= 64 and scan_input.IatRVA <= 2048 and scan_input.DebugSize > 0:
                isDirty = 0
            elif scan_input.ExportSize <= 276 and scan_input.NumberOfSections > 5 and scan_input.ResourceSize <= 1076:
                isDirty = 0
            elif scan_input.DebugSize > 0 and scan_input.IatRVA <= 94208 and scan_input.ExportSize <= 82 and scan_input.DebugSize <= 56 and scan_input.NumberOfSections > 2 and scan_input.ImageVersion <= 2340 and scan_input.ResourceSize <= 118280 and scan_input.VirtualSize2 > 5340:
                isDirty = 0
            elif 0 < scan_input.DebugSize <= 56 and scan_input.ImageVersion <= 2340 and scan_input.NumberOfSections > 3 and scan_input.VirtualSize2 > 360 and scan_input.NumberOfSections <= 5:
                isDirty = 1
            elif scan_input.IatRVA > 37380 and scan_input.ImageVersion <= 0 and scan_input.NumberOfSections <= 5 and scan_input.VirtualSize2 > 15864:
                isDirty = 0
            elif scan_input.DebugSize <= 0 and scan_input.VirtualSize2 <= 80 and scan_input.IatRVA <= 4096 and scan_input.ExportSize <= 0 and 4 < scan_input.VirtualSize2 <= 21:
                isDirty = 0
            elif scan_input.DebugSize <= 0:
                isDirty = 1
            elif scan_input.ExportSize <= 82 and scan_input.DebugSize <= 56 and 5 >= scan_input.NumberOfSections > 2 and scan_input.IatRVA <= 6144 and scan_input.ImageVersion > 2340:
                isDirty = 0
            elif scan_input.ImageVersion > 2340:
                isDirty = 1
            elif scan_input.ResourceSize > 5528:
                isDirty = 0
            else:
                isDirty = 1
            return isDirty

        def runJ48Graft():
            isDirty = 0
            if scan_input.DebugSize <= 0:
                if scan_input.ExportSize <= 211:
                    if scan_input.ImageVersion <= 520:
                        if scan_input.VirtualSize2 <= 130:
                            if scan_input.VirtualSize2 <= 5:
                                if scan_input.ResourceSize <= 37520:
                                    isDirty = 1
                                elif scan_input.ResourceSize > 37520:
                                    if scan_input.NumberOfSections <= 2:
                                        if scan_input.IatRVA <= 2048:
                                            if scan_input.ExportSize <= 67.5:
                                                isDirty = 0
                                            else:
                                                isDirty = 1
                                        else:
                                            isDirty = 1
                                    else:
                                        isDirty = 1
                            else:
                                if scan_input.VirtualSize <= 12:
                                    if scan_input.NumberOfSections <= 3:
                                        isDirty = 0
                                    else:
                                        isDirty = 1
                                else:
                                    isDirty = 1
                        else:
                            isDirty = 1
                    else:
                        if scan_input.ResourceSize <= 0:
                            if scan_input.ImageVersion <= 1000:
                                if scan_input.NumberOfSections <= 4:
                                    isDirty = 1
                                else:
                                    if scan_input.ExportSize <= 74:
                                        if scan_input.VirtualSize2 <= 1556:
                                            isDirty = 1
                                        else:
                                            if scan_input.IatRVA <= 5440:
                                                if scan_input.VirtualSize2 <= 126474:
                                                    if scan_input.ExportSize <= 24:
                                                        isDirty = 0
                                                    else:
                                                        isDirty = 1
                                                else:
                                                    isDirty = 1
                                            else:
                                                isDirty = 1
                                    else:
                                        isDirty = 0
                            else:
                                isDirty = 1
                        else:
                            if scan_input.NumberOfSections <= 2:
                                if scan_input.ImageVersion <= 3420:
                                    isDirty = 1
                                else:
                                    isDirty = 0
                            else:
                                isDirty = 1
                else:
                    if scan_input.ImageVersion <= 0:
                        if scan_input.ExportSize <= 23330:
                            if scan_input.IatRVA <= 98304:
                                if scan_input.NumberOfSections <= 3:
                                    isDirty = 1
                                else:
                                    if scan_input.IatRVA <= 53872:
                                        if scan_input.VirtualSize2 <= 17.5:
                                            isDirty = 1
                                        else:
                                            if scan_input.NumberOfSections <= 10.5:
                                                if scan_input.ResourceSize <= 3103192:
                                                    if scan_input.ExportSize <= 10858.5:
                                                        if scan_input.VirtualSize2 <= 116016.5:
                                                            isDirty = 0
                                                        else:
                                                            isDirty = 1
                                                    else:
                                                        isDirty = 0
                                                else:
                                                    isDirty = 1
                                            else:
                                                isDirty = 1
                                    else:
                                        if scan_input.ExportSize <= 273:
                                            isDirty = 1
                                        else:
                                            if scan_input.ResourceSize <= 1016:
                                                isDirty = 1
                                            else:
                                                isDirty = 0
                            else:
                                isDirty = 0
                        else:
                            isDirty = 1
                    else:
                        if scan_input.ExportSize <= 1006718985:
                            isDirty = 0
                        else:
                            isDirty = 1
            else:
                if scan_input.ResourceSize <= 545:
                    if scan_input.ExportSize <= 92:
                        if scan_input.NumberOfSections <= 4:
                            isDirty = 0
                        else:
                            if scan_input.ImageVersion <= 6005:
                                if scan_input.ExportSize <= 6714:
                                    isDirty = 1
                                else:
                                    isDirty = 0
                            else:
                                isDirty = 0
                else:
                    if scan_input.IatRVA <= 94208:
                        if scan_input.NumberOfSections <= 5:
                            if scan_input.ExportSize <= 0:
                                if scan_input.NumberOfSections <= 4:
                                    if scan_input.IatRVA <= 13504:
                                        if scan_input.ImageVersion <= 353:
                                            if scan_input.NumberOfSections <= 3:
                                                if scan_input.IatRVA <= 6144:
                                                    if scan_input.IatRVA <= 2048:
                                                        if scan_input.ResourceSize <= 934:
                                                            isDirty = 1
                                                        else:
                                                            if scan_input.VirtualSize2 <= 2728:
                                                                isDirty = 0
                                                            else:
                                                                isDirty = 1
                                                    else:
                                                        if scan_input.VirtualSize2 <= 496:
                                                            isDirty = 1
                                                        else:
                                                            isDirty = 0
                                                else:
                                                    isDirty = 0
                                            else:
                                                if scan_input.DebugSize <= 41:  # debug here
                                                    if scan_input.ResourceSize <= 22720:
                                                        if scan_input.IatRVA <= 2048:
                                                            isDirty = 1
                                                        else:
                                                            if scan_input.VirtualSize2 <= 46:
                                                                isDirty = 0
                                                            else:
                                                                isDirty = 1
                                                    else:
                                                        if scan_input.VirtualSize2 <= 43030:
                                                            if scan_input.ResourceSize <= 3898348:
                                                                if scan_input.IatRVA <= 2048:
                                                                    isDirty = 1
                                                                else:
                                                                    isDirty = 0
                                                            else:
                                                                isDirty = 1
                                                        else:
                                                            isDirty = 0
                                                else:
                                                    isDirty = 0
                                        else:
                                            isDirty = 0
                                    else:
                                        if scan_input.ResourceSize <= 35328:
                                            if scan_input.ImageVersion <= 4005:
                                                if scan_input.NumberOfSections <= 1.5:
                                                    isDirty = 1
                                                else:
                                                    isDirty = 0
                                            else:
                                                isDirty = 0
                                        else:
                                            if scan_input.ImageVersion <= 5510:
                                                if scan_input.DebugSize <= 42:
                                                    if scan_input.VirtualSize2 <= 144328:
                                                        if scan_input.NumberOfSections <= 3.5:
                                                            isDirty = 0
                                                        else:
                                                            isDirty = 1
                                                    else:
                                                        isDirty = 0
                                                else:
                                                    isDirty = 0
                                            else:
                                                isDirty = 0
                                else:
                                    if scan_input.IatRVA <= 2048:
                                        isDirty = 1
                                    else:
                                        isDirty = 0
                            else:
                                isDirty = 0
                        else:
                            if scan_input.IatRVA <= 1054:
                                if scan_input.ExportSize <= 218:
                                    if scan_input.IatRVA <= 704:
                                        isDirty = 1
                                    else:
                                        if scan_input.NumberOfSections <= 6:
                                            isDirty = 1
                                        else:
                                            isDirty = 0
                                else:
                                    if scan_input.ExportSize <= 1006699445:
                                        if scan_input.ImageVersion <= 5510:
                                            if scan_input.ImageVersion <= 500:
                                                isDirty = 1
                                            else:
                                                isDirty = 0
                                        else:
                                            isDirty = 0
                                    else:
                                        isDirty = 1
                            else:
                                isDirty = 0
                    else:
                        if scan_input.ExportSize <= 0:
                            if scan_input.VirtualSize2 <= 78800:
                                if scan_input.NumberOfSections <= 4:
                                    isDirty = 0
                                else:
                                    if scan_input.ImageVersion <= 2340:
                                        if scan_input.ResourceSize <= 7328:
                                            isDirty = 1
                                        else:
                                            if scan_input.VirtualSize2 <= 8288.5:
                                                isDirty = 1
                                            else:
                                                if scan_input.NumberOfSections <= 6.5:
                                                    isDirty = 0
                                                else:
                                                    isDirty = 1
                                    else:
                                        isDirty = 0
                            else:
                                if scan_input.ImageVersion <= 5515:
                                    isDirty = 1
                                else:
                                    isDirty = 0
                        else:
                            if scan_input.IatRVA <= 106496:
                                if scan_input.ResourceSize <= 2800:
                                    isDirty = 0
                                else:
                                    if scan_input.ImageVersion <= 500:
                                        if scan_input.ResourceSize <= 5360:
                                            if scan_input.NumberOfSections <= 4.5:
                                                isDirty = 0
                                            else:
                                                if scan_input.VirtualSize2 <= 22564.5:
                                                    if scan_input.ExportSize <= 191.5:
                                                        if scan_input.DebugSize <= 42:
                                                            if scan_input.ExportSize <= 162.5:
                                                                isDirty = 0
                                                            else:
                                                                if scan_input.VirtualSize2 <= 10682:
                                                                    isDirty = 0
                                                                else:
                                                                    if scan_input.ResourceSize <= 3412:
                                                                        isDirty = 0
                                                                    else:
                                                                        isDirty = 1
                                                        else:
                                                            isDirty = 0
                                                    else:
                                                        isDirty = 0
                                                else:
                                                    isDirty = 0
                                        else:
                                            isDirty = 0
                                    else:
                                        isDirty = 0
                            else:
                                isDirty = 0
            return isDirty

        def runJ48():
            isDirty = 0
            if scan_input.DebugSize <= 0:
                if scan_input.ExportSize <= 211:
                    if scan_input.ImageVersion <= 520:
                        if scan_input.VirtualSize2 <= 130:
                            if scan_input.VirtualSize2 <= 5:
                                if scan_input.ResourceSize <= 37520:
                                    isDirty = 1
                                elif scan_input.ResourceSize > 37520:
                                    if scan_input.NumberOfSections <= 2:
                                        if scan_input.IatRVA <= 2048:
                                            isDirty = 0
                                        else:
                                            isDirty = 1
                                    else:
                                        isDirty = 1
                            else:
                                if scan_input.VirtualSize2 <= 12:
                                    if scan_input.NumberOfSections <= 3:
                                        isDirty = 0
                                    else:
                                        isDirty = 1
                                else:
                                    isDirty = 1
                        else:
                            isDirty = 1
                    else:
                        if scan_input.ResourceSize <= 0:
                            if scan_input.ImageVersion <= 1000:
                                if scan_input.NumberOfSections <= 4:
                                    isDirty = 1
                                else:
                                    if scan_input.ExportSize <= 74:
                                        if scan_input.VirtualSize2 <= 1556:
                                            isDirty = 1
                                        else:
                                            isDirty = 0
                                    else:
                                        isDirty = 0
                            else:
                                isDirty = 1
                        else:
                            if scan_input.NumberOfSections <= 2:
                                if scan_input.ImageVersion <= 3420:
                                    isDirty = 1
                                else:
                                    isDirty = 0
                            else:
                                isDirty = 1
                else:
                    if scan_input.ImageVersion <= 0:
                        if scan_input.ExportSize <= 23330:
                            if scan_input.IatRVA <= 98304:
                                if scan_input.NumberOfSections <= 3:
                                    isDirty = 1
                                else:
                                    if scan_input.IatRVA <= 53872:
                                        isDirty = 0
                                    else:
                                        if scan_input.ExportSize <= 273:
                                            isDirty = 1
                                        else:
                                            if scan_input.ResourceSize <= 1016:
                                                isDirty = 1
                                            else:
                                                isDirty = 0
                            else:
                                isDirty = 0
                        else:
                            isDirty = 1
                    else:
                        isDirty = 0
            else:
                if scan_input.ResourceSize <= 545:
                    if scan_input.ExportSize <= 92:
                        if scan_input.NumberOfSections <= 4:
                            isDirty = 0
                        else:
                            isDirty = 1
                else:
                    if scan_input.IatRVA <= 94208:
                        if scan_input.NumberOfSections <= 5:
                            if scan_input.ExportSize <= 0:
                                if scan_input.NumberOfSections <= 4:
                                    if scan_input.IatRVA <= 13504:
                                        if scan_input.ImageVersion <= 353:
                                            if scan_input.NumberOfSections <= 3:
                                                if scan_input.IatRVA <= 6144:
                                                    if scan_input.IatRVA <= 2048:
                                                        isDirty = 0
                                                    else:
                                                        if scan_input.VirtualSize2 <= 496:
                                                            isDirty = 1
                                                        else:
                                                            isDirty = 0
                                                else:
                                                    isDirty = 0
                                            else:
                                                if scan_input.DebugSize <= 41:
                                                    if scan_input.ResourceSize <= 22720:
                                                        isDirty = 1
                                                    else:
                                                        isDirty = 0
                                                else:
                                                    isDirty = 0
                                        else:
                                            isDirty = 0
                                    else:
                                        if scan_input.ResourceSize <= 35328:
                                            isDirty = 0
                                        else:
                                            isDirty = 1
                                else:
                                    if scan_input.IatRVA <= 2048:
                                        isDirty = 1
                                    else:
                                        isDirty = 0
                            else:
                                isDirty = 0
                        else:
                            if scan_input.IatRVA <= 1054:
                                if scan_input.ExportSize <= 218:
                                    if scan_input.IatRVA <= 704:
                                        isDirty = 1
                                    else:
                                        if scan_input.NumberOfSections <= 6:
                                            isDirty = 1
                                        else:
                                            isDirty = 0
                                else:
                                    isDirty = 0
                            else:
                                isDirty = 0
                    else:
                        if scan_input.ExportSize <= 0:
                            if scan_input.VirtualSize2 <= 78800:
                                if scan_input.NumberOfSections <= 4:
                                    isDirty = 0
                                else:
                                    if scan_input.ImageVersion <= 2340:
                                        if scan_input.ResourceSize <= 7328:
                                            isDirty = 1
                                        else:
                                            isDirty = 0
                                    else:
                                        isDirty = 0
                            else:
                                isDirty = 1
                        else:
                            if scan_input.IatRVA <= 106496:
                                if scan_input.ResourceSize <= 2800:
                                    isDirty = 0
                                else:
                                    isDirty = 1
                            else:
                                isDirty = 0
            return isDirty

        result1 = runJ48()
        result2 = runJ48Graft()
        result3 = runPART()
        result4 = runRidor()
        if (result1 == result2) and (result2 == result3) and (result3 == result4):
            return result1
        else:
            if [result1, result2, result3, result4].count(1) >= [result1, result2, result3, result4].count(0):
                return True
            else:
                return False
    def scan_file_sha256(self, file_path):
        if file_path.replace("/", "\\") in Viruses_White_exe:
            return False
        process = subprocess.Popen(f'Scanner_SDK_HTTP2_SHA256.exe "{file_path}" Q53NMDNB2A5WN4KLLPCHMMP53U',
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
        stdout, stderr = process.communicate()
        return json.loads([item for item in
                           [item.split(" 的响应: ")[1] if " 的响应: " in item else item for item in stdout.split("\n")]
                           if '{' in item and '}' in item and ':' in item][0])["score"] >= 60
    def api_scan(self, file):
        if file_path.replace("/", "\\") in Viruses_White_exe:
            return False
        try:
            if 1 == 1:
                with open(file, "rb") as f:
                    text = str(md5(f.read()).hexdigest())
                strBody = f'-------------------------------7d83e2d7a141e\r\nContent-Disposition: form-data; name="md5s"\r\n\r\n{text}\r\n-------------------------------7d83e2d7a141e\r\nContent-Disposition: form-data; name="format"\r\n\r\nXML\r\n-------------------------------7d83e2d7a141e\r\nContent-Disposition: form-data; name="product"\r\n\r\n360zip\r\n-------------------------------7d83e2d7a141e\r\nContent-Disposition: form-data; name="combo"\r\n\r\n360zip_main\r\n-------------------------------7d83e2d7a141e\r\nContent-Disposition: form-data; name="v"\r\n\r\n2\r\n-------------------------------7d83e2d7a141e\r\nContent-Disposition: form-data; name="osver"\r\n\r\n5.1\r\n-------------------------------7d83e2d7a141e\r\nContent-Disposition: form-data; name="vk"\r\n\r\na03bc211\r\n-------------------------------7d83e2d7a141e\r\nContent-Disposition: form-data; name="mid"\r\n\r\n8a40d9eff408a78fe9ec10a0e7e60f62\r\n-------------------------------7d83e2d7a141e--'
                response = urllib.request.urlopen('http://qup.f.360.cn/file_health_info.php',
                                                  data=bytes(strBody, encoding='utf-8'), timeout=3)
                return response.status == 200 and float(
                    et.fromstring(response.read().decode('utf-8')).find('.//e_level').text) > 20
        except:
            return False
    def sign_scan(self, file):
        if file.replace("/", "\\") in Viruses_White_exe:
            return False
        try:
            p = PE(file)
            p.close()
        except:
            return False
        try:
            pe = PE(file, fast_load=True)
            pe.close()
            return pe.OPTIONAL_HEADER.DATA_DIRECTORY[
                DIRECTORY_ENTRY["IMAGE_DIRECTORY_ENTRY_SECURITY"]].VirtualAddress == 0
        except:
            return True
    def cloud_scan(self, file):
        if file.replace("/", "\\") in Viruses_White_exe:
            return False
        try:
            with open(file, 'rb') as f:
                files = {'file': f}
                url = 'http://27.147.30.238:5001/upload'
                data = urllib.parse.urlencode(files).encode('utf-8')
                req = urllib.request.Request(url, data=data)
                with urllib.request.urlopen(req) as response:
                    if response.status == 200:
                        if b"Virus" in response.read():
                            return True
                    return False
        except:
            return False
    def pe_scan(self, file):
        if file.replace("/", "\\") in Viruses_White_exe:
            return False
        try:
            m = hashlib.md5()
            f = open(file, 'rb')
            m.update(f.read())
            f.close()
            f = open('MD5.txt', 'r')
            if m.hexdigest() in f.read():
                f.close()
                return True
            f.close()
        except:
            return False
        try:
            f = open("函数.txt", "r")
            o = f.read()
            f.close()
            function_list = o.split("\n")
            fn = []
            pe = PE(file)
            pe.close()
            for entry in pe.DIRECTORY_ENTRY_IMPORT:
                for func in entry.imports:
                    fn.append(str(func.name, "utf-8"))
            for vfl in function_list:
                if len(set(fn) & set(vfl)) / len(set(fn) | set(vfl)) == 1.0:
                    return True
            return False
        except:
            return False
    def start_scan(self, file):
        if file.replace("/", "\\") in Viruses_White_exe:
            return False
        try:
            label, level = self.peC(file)
            if label and "Unknown" in label:
                if self.cloud_scan(file):
                    return True
            elif label and "White" not in label:
                if level and level >= 0.8:
                    return True
                elif self.cloud_scan(file):
                    return True
            return False
        except:
            return False
    def scan_directory(self, scan_path):
        if file_path.replace("/", "\\") in Viruses_White_exe:
            return False
        # 调用外部程序并获取输出
        command = [os.path.join(jzhsd_dir, "MalwareCheck.exe")]

        # 使用 subprocess 来调用命令并获取输入输出
        process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   text=True)

        # 向程序输入扫描路径
        process.stdin.write(scan_path + '\n')
        process.stdin.flush()

        # 捕获程序输出
        stdout, stderr = process.communicate()
        f = []
        for i in stdout.split("\n"):
            if not (
                    "请输入扫描路径：" in i or "扫描完成，危险总数：" in i or "运行用时: " in i or "安全文件: " in i or i == ""):
                try:
                    f.append(i.split("文件: ")[1])
                except:
                    pass
        return f
    def peC(self, file):
        if file.replace("/", "\\") in Viruses_White_exe:
            return False
        try:
            fn = []
            with PE(file) as pe:
                for entry in pe.DIRECTORY_ENTRY_IMPORT:
                    for func in entry.imports:
                        try:
                            fn.append(str(func.name, "utf-8"))
                        except:
                            pass
            label, level = self.pe.predict(fn)
            return label, int(level * 100)
        except:
            return False, False
    def qq(self):
        return self.p
AntivirusEngine = AntivirusEngine()
class ListSimHash:
    def __init__(self):
        self.model = {}
    def save_model(self, file_name):
        with open(file_name, 'w') as f:
            json.dump(self.model, f)
        print(f"\nModel Is Saved In {file_name}")
    def load_model(self, model_data):
        if isinstance(model_data, str):
            with open(model_data, 'r') as f:
                model_data = json.load(f)
        self.model = model_data
    def get_model(self, label):
        return self.model[label]
    def train_model(self, label, data):
        start = time.time()
        print(f"Convert {label}")
        if label not in self.model:
            self.model[label] = []
        for i, x in enumerate(data, 1):
            self.model[label].append(self.build_text(x))
            used = "{0:.2f}".format(time.time()-start)
            prefix, suffix = f'{i}/{len(data)}:', f'{used}s'
            self.progress_bar(i, len(data), prefix, suffix)
    def build_text(self, content):
        sums, batch, count = [], [], 0
        features = dict(Counter(sorted(content)))
        for f, w in features.items():
            count += w
            batch.append(hashlib.sha256(json.dumps(f).encode('utf-8')).digest() * w)
            if len(batch) >= 10000:
                sums.append(self.sum_hashes(batch))
                batch = []
        if batch:
            sums.append(self.sum_hashes(batch))
        combined_sums = numpy.sum(sums, 0)
        v = numpy.packbits(combined_sums > count / 2).tobytes()
        return int.from_bytes(v, 'big')
    def sum_hashes(self, digests):
        bitarray = numpy.unpackbits(numpy.frombuffer(b''.join(digests), dtype='>B'))
        return numpy.sum(numpy.reshape(bitarray, (-1, 256)), 0)
    def progress_bar(self, iteration, total, prefix='', suffix='', length=50, fill='█'):
        percent = min(100.0, max(0.0, 100 * (iteration / float(total))))
        end_char = '\n' if percent >= 100 else '\r'
        percent_string = "{0:.2f}".format(percent)
        filled_length = int(length * iteration // total)
        bar = fill * filled_length + ' ' * (length - filled_length)
        print(f'\r    {prefix: <10} |{bar}| {percent_string}% {suffix}', end=end_char)
    def predict_all(self, query):
        label_similarities = {}
        query_hash = self.build_text(query)
        for label in self.model:
            max_similarity = 0
            for data_point in self.model[label]:
                similarity = self.similar(data_point, query_hash)
                if similarity > max_similarity:
                    max_similarity = similarity
            label_similarities[label] = max_similarity
        return label_similarities
    def predict(self, query):
        max_similarity, max_label = 0, None
        query_hash = self.build_text(query)
        for label in self.model:
            for data_point in self.model[label]:
                similarity = self.similar(data_point, query_hash)
                if similarity > max_similarity:
                    max_similarity, max_label = similarity, label
        return max_label, max_similarity
    def similar(self, x, y):
        hamming_distance = bin(x ^ y).count('1')
        return 1 - hamming_distance / 256
class YRScan:
    def __init__(self):
        self.rules = {}
        self.network = []

    def load_rules(self, file_path):
        try:
            ftype = str(f".{file_path.split('.')[-1]}").lower()
            if ftype in [".yara", ".yar"]:
                self.rules[file_path] = yara.compile(file_path)
            elif ftype in [".yc", ".yrc"]:
                self.rules[file_path] = yara.load(file_path)
            elif ftype in [".ip", ".ips"]:
                with open(file_path, "r") as f:
                    self.network += [l.strip() for l in f.readlines()]
        except Exception as e:
            print(e)
    def yr_scan(self, file_path):
        try:
            if isinstance(file_path, str):
                with open(file_path, "rb") as f:
                    file_path = f.read()
            for name, rules in self.rules.items():
                matchs_rules = rules.match(data=file_path)
                if matchs_rules:
                    label = str(matchs_rules[0]).split("_")[0]
                    level = str(matchs_rules[0]).split("_")[-1]
                    label, level = f"Rules/{label}", level
                    if label and isinstance(level, str):
                        return True
            return False
        except Exception as e:
            return False
    def start_scan(self, file):
        if file in Viruses_White_exe:
            return False
        try:
            if isinstance(file, dict):
                match_data = file
            elif os.path.exists(file):
                match_data = model.get_type(file)
            else:
                return False
            for section, data in match_data.items():
                label, level = model.dl_scan(data)
                if label and label in model.detect:
                    return True
            label, level = self.yr_scan(file)
            if label and isinstance(level, str):
                return True
            return False
        except:
            return False
class DLScan:
    def __init__(self):
        self.models = {}
        self.shells = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '!o',
        'cry', 'test', 'ace', 'yg', 'obr', 'tvm', 'dec', 'enc', 'b1_', 'base',
        'bss', 'clr_uef', 'cursors', 'trs_age', 'engine', 'enigma', 'protect',
        'nep', 'no_bbt', 'wpp_sf', 'retpol', 'rt', 'rwexec', 'rygs', 'poolmi',
        's:@', 'pgae', 'proxy', 'wisevec', 'segm', 'transit', 'vmp', 'extjmp',
        'upx', 'tracesup', 'res', 'lzma', 'malloc_h', 'miniex', 'ndr64', 'be',
        'mssmixer', 'wow', 'press', 'fio', 'pad', 'hexpthk', 'h~;', 'icapsec',
        'sanontcp', 'secur', 'asmstub', 'nsys_wr', 'orpc', 'pack', 'wow64svc',
        'uedbg', 'viahw', 'data', 'zk', 'fothk', 'qihoo']#"""
    def load_model(self, file_path):
        try:
            ftype = str(f".{file_path.split('.')[-1]}").lower()
            if ftype in [".json", ".txt"]:
                with open(file_path, 'r') as f:
                    self.class_names = json.load(f)
            elif ftype in [".onnx"]:
                self.models[file_path] = onnxruntime.InferenceSession(file_path)
            self.labels = self.class_names['Labels']
            self.detect = self.class_names['Detect']
            self.pixels = self.class_names['Pixels']
            self.values = self.class_names['Values']
            self.suffix = self.class_names['Suffix']
        except Exception as e:
            pass
    def dl_scan(self, file_data):
        try:
            label_similarities = {label: [] for label in self.labels}
            image_data = self.preprocess_image(file_data, tuple(self.pixels))
            image_array = numpy.asarray(image_data).astype('float32') / 255.0
            image_expand = numpy.expand_dims(image_array, axis=(0, -1))
            for model_name, model in self.models.items():
                input_name = model.get_inputs()[0].name
                pre_answers = model.run(None, {input_name: image_expand})[0][0]
                for k, score in enumerate(pre_answers):
                    label_similarities[self.labels[k].strip()].append(score)
            label_percentage = {label: (sum(similarities) / len(self.models)) * 100
                                for label, similarities in label_similarities.items()}
            label, level = max(label_percentage.items(), key=lambda x: x[1])
            return label, int(level)
        except Exception as e:
            return False, False
    def start_scan(self, file): # 調用掃描引擎
        if file in Viruses_White_exe:
            return False
        self.config_json = {
            "sensitivity": 1,  # "0" (Medium), "1" (High)
            "extend_mode": 0}  # "0" (False), "1" (True)
        try:
            match_data = model.get_type(file)
            for section, data in match_data.items():
                label, level = model.dl_scan(data)
                if label and label in model.detect:
                    if self.config_json["sensitivity"]:
                        return f"{label}.{level}"
                    elif level >= model.values:
                        return f"{label}.{level}"
            if self.config_json["extend_mode"]:
                label, level = rules.yr_scan(file)
                if label and isinstance(level, str):
                    return f"{label}.{level}"
            return False
        except:
            return False

    def preprocess_image(self, file_data, target_size):
        wah = int(numpy.ceil(numpy.sqrt(len(file_data))))
        file_data = numpy.frombuffer(file_data, dtype=numpy.uint8)
        image_array = numpy.zeros((wah * wah,), dtype=numpy.uint8)
        image_array[:len(file_data)] = file_data
        image = Image.fromarray(image_array.reshape((wah, wah)), 'L')
        return image.resize(target_size, Image.Resampling.NEAREST)

    def get_type(self, file_path):
        match_data = {}
        ftype = str(f".{file_path.split('.')[-1]}").lower()
        if ftype in self.suffix:
            try:
                with pefile.PE(file_path, fast_load=True) as pe:
                    for section in pe.sections:
                        section_name = section.Name.rstrip(b'\x00').decode('latin1')
                        if (section.Characteristics & 0x00000020 and not
                        any(shell in section_name.lower() for shell in self.shells)):
                            match_data[section_name] = section.get_data()
            except:
                if ftype in [".bat", ".cmd", ".ps1", ".vbs", ".wsf", ".html", ".js",
                    ".txt", ".htm", ".hta", ".php", ".css", ".xml", ".json", ".wasm"]:
                    with open(file_path, 'rb') as file:
                        match_data[ftype] = file.read()
        return match_data
jzhsd_dir = os.path.dirname(sys.argv[0])
model = DLScan()
rules = YRScan()
appdata_path = os.getenv('AppData')
data_path = os.path.join(jzhsd_dir, "Engine/Model")
if not os.path.isdir(appdata_path + "\\jzh"):
    os.mkdir(appdata_path + "\\jzh")
    os.mkdir(appdata_path + "\\jzh\\Engine")
    os.mkdir(appdata_path + "\\jzh\\Engine\\Model")
    os.mkdir(appdata_path + "\\jzh\\Engine\\Rules")
for root_jiazai, dirs, files in os.walk(data_path):
    for file in files:
        file_path = os.path.join(root_jiazai, file)
        shutil.copy2(file_path, appdata_path + "\\jzh" + file_path.replace(jzhsd_dir, ""))
data_path = os.path.join(jzhsd_dir, "Engine/Rules")
for root_jiazai, dirs, files in os.walk(data_path):
    for file in files:
        file_path = os.path.join(root_jiazai, file).replace("/", "\\")
        shutil.copy2(file_path, appdata_path + "\\jzh" + file_path.replace(jzhsd_dir, ""))
data_path = appdata_path + "\\jzh" + "Engine\\Model"
for root_jiazai, dirs, files in os.walk(data_path):
    for file in files:
        file_path = os.path.join(root_jiazai, file)
        model.load_model(file_path)
data_path = appdata_path + "\\jzh" + "Engine\\Rules"
for root_jiazai, dirs, files in os.walk(data_path):
    for file in files:
        file_path = os.path.join(root_jiazai, file).replace("/", "\\")
        rules.load_rules(file_path)
def AntiVirus_file(f_path, online=online):
    print(f_path.replace("/", "\\"))
    print(Viruses_White_exe)
    print(f_path.replace("/", "\\") in Viruses_White_exe)
    if f_path.replace("/", "\\") in Viruses_White_exe:
        return False
    pe_scan = AntivirusEngine.pe_scan(f_path)
    f_da = open(f_path, "rb")
    f_data = f_da.read()
    f_da.close()
    try:
        if AntivirusEngine.sign_scan(f_path):
            return True
    except:
        pass
    try:
        if pe_scan:
            return True
    except:
        pass
    try:
        if AntivirusEngine.AdobeMalwareClassifier_scan(f_path):
            return True
    except:
        pass
    try:
        if model.start_scan(f_data):
            return True
    except:
        pass
    try:
        if rules.start_scan(f_path):
            return True
    except:
        pass
    if online:
        try:
            if AntivirusEngine.api_scan(f_path):
                return True
        except:
            pass
        try:
            if AntivirusEngine.start_scan(f_path):
                return True
        except:
            pass
        try:
            if AntivirusEngine.scan_file_sha256(f_path):
                return True
        except:
            pass
        return False
    else:
        return False
def AntiVirus_files(f_paths2, online=online):
    f_paths = []
    for f in f_paths2:
        if not f in Viruses_White_exe:
            f_paths.append(f.replace("/", "\\\\"))
    VirusFile = []
    num = 0
    for f_path in f_paths:
        num += 1
        print(num)
        if AntiVirus_file(f_path, online):
            VirusFile.append(f_path)
    return VirusFile
def AntiVirus_folder(folder_path, online=online):
    scan_results = AntivirusEngine.scan_directory(folder_path)
    scan_results = []
    f_paths = []
    for root_jiazai, dirs, files in os.walk(folder_path):
        for file in files:
            f_path = os.path.join(root_jiazai, file)
            if not f_path in scan_results:
                f_paths.append(f_path)
    return scan_results + AntiVirus_files(f_paths, online)

# 系统自动修复
class SystemRecoveryEngine:
    def __init__(self):
        self.p = None
        self.q = 1
        self.jinchen = 0
    def repair_system_restrict(self):
        try:
            Permission = ["NoControlPanel", "NoDrives", "NoFileMenu", "NoFind", "NoRealMode", "NoRecentDocsMenu",
                          "NoSetFolders",
                          "NoSetFolderOptions", "NoViewOnDrive", "NoClose", "NoRun", "NoDesktop", "NoLogOff",
                          "NoFolderOptions", "RestrictRun", "DisableCMD",
                          "NoViewContexMenu", "HideClock", "NoStartMenuMorePrograms", "NoStartMenuMyGames",
                          "NoStartMenuMyMusic" "NoStartMenuNetworkPlaces",
                          "NoStartMenuPinnedList", "NoActiveDesktop", "NoSetActiveDesktop", "NoActiveDesktopChanges",
                          "NoChangeStartMenu", "ClearRecentDocsOnExit",
                          "NoFavoritesMenu", "NoRecentDocsHistory", "NoSetTaskbar", "NoSMHelp", "NoTrayContextMenu",
                          "NoViewContextMenu", "NoWindowsUpdate",
                          "NoWinKeys", "StartMenuLogOff", "NoSimpleNetlDList", "NoLowDiskSpaceChecks",
                          "DisableLockWorkstation", "NoManageMyComputerVerb",
                          "DisableTaskMgr", "DisableRegistryTools", "DisableChangePassword", "Wallpaper",
                          "NoComponents", "NoAddingComponents", "Restrict_Run"]
            win32api.RegCreateKey(
                win32api.RegOpenKey(win32con.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies",
                                    0, win32con.KEY_ALL_ACCESS), "Explorer")
            win32api.RegCreateKey(
                win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies",
                                    0, win32con.KEY_ALL_ACCESS), "Explorer")
            win32api.RegCreateKey(
                win32api.RegOpenKey(win32con.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies",
                                    0, win32con.KEY_ALL_ACCESS), "System")
            win32api.RegCreateKey(
                win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies",
                                    0, win32con.KEY_ALL_ACCESS), "System")
            win32api.RegCreateKey(
                win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies",
                                    0, win32con.KEY_ALL_ACCESS), "ActiveDesktop")
            win32api.RegCreateKey(
                win32api.RegOpenKey(win32con.HKEY_CURRENT_USER, r"SOFTWARE\Policies\Microsoft\Windows", 0,
                                    win32con.KEY_ALL_ACCESS), "System")
            win32api.RegCreateKey(
                win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE, r"SOFTWARE\Policies\Microsoft\Windows", 0,
                                    win32con.KEY_ALL_ACCESS), "System")
            win32api.RegCreateKey(win32api.RegOpenKey(win32con.HKEY_CURRENT_USER, r"Software\Policies\Microsoft", 0,
                                                      win32con.KEY_ALL_ACCESS), "MMC")
            win32api.RegCreateKey(win32api.RegOpenKey(win32con.HKEY_CURRENT_USER, r"Software\Policies\Microsoft\MMC", 0,
                                                      win32con.KEY_ALL_ACCESS),
                                  "{8FC0B734-A0E1-11D1-A7D3-0000F87571E3}")
            keys = [win32api.RegOpenKey(win32con.HKEY_CURRENT_USER,
                                        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer", 0,
                                        win32con.KEY_ALL_ACCESS),
                    win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE,
                                        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer", 0,
                                        win32con.KEY_ALL_ACCESS),
                    win32api.RegOpenKey(win32con.HKEY_CURRENT_USER,
                                        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System", 0,
                                        win32con.KEY_ALL_ACCESS),
                    win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE,
                                        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System", 0,
                                        win32con.KEY_ALL_ACCESS),
                    win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE,
                                        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\ActiveDesktop", 0,
                                        win32con.KEY_ALL_ACCESS),
                    win32api.RegOpenKey(win32con.HKEY_CURRENT_USER, r"SOFTWARE\Policies\Microsoft\Windows\System", 0,
                                        win32con.KEY_ALL_ACCESS),
                    win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE, r"SOFTWARE\Policies\Microsoft\Windows\System", 0,
                                        win32con.KEY_ALL_ACCESS),
                    win32api.RegOpenKey(win32con.HKEY_CURRENT_USER,
                                        r"Software\Policies\Microsoft\MMC\{8FC0B734-A0E1-11D1-A7D3-0000F87571E3}", 0,
                                        win32con.KEY_ALL_ACCESS)]
            for key in keys:
                for i in Permission:
                    try:
                        win32api.RegDeleteValue(key, i)
                    except:
                        pass
                win32api.RegCloseKey(key)
        except:
            pass
    def repair_system_icon(self):
        try:
            for file_type in ['exefile', 'comfile', 'txtfile', 'dllfile', 'inifile', 'VBSfile']:
                try:
                    key = win32api.RegOpenKey(win32con.HKEY_CLASSES_ROOT, file_type, 0, win32con.KEY_ALL_ACCESS)
                    win32api.RegSetValue(key, 'DefaultIcon', win32con.REG_SZ, '%1')
                except:
                    pass
                try:
                    key = win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE, 'SOFTWARE\\Classes\\' + file_type, 0,
                                              win32con.KEY_ALL_ACCESS)
                    win32api.RegSetValue(key, 'DefaultIcon', win32con.REG_SZ, '%1')
                except:
                    pass
        except:
            pass
    def repair_system_image(self):
        try:
            key = win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE,
                                      'SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Image File Execution Options',
                                      0, win32con.KEY_ALL_ACCESS | win32con.WRITE_OWNER)
            count = win32api.RegQueryInfoKey(key)[0]
            while count >= 0:
                try:
                    subKeyName = win32api.RegEnumKey(key, count)
                    win32api.RegDeleteKey(key, subKeyName)
                except:
                    pass
                count = count - 1
        except:
            pass
    def repair_system_file_type(self):
        try:
            data = [('jpegfile', 'JPEG Image'), ('.exe', 'exefile'), ('exefile', 'Application'), ('.com', 'comfile'),
                    ('comfile', 'MS-DOS Application'),
                    ('.zip', 'CompressedFolder'), ('.dll', 'dllfile'), ('dllfile', 'Application Extension'),
                    ('.sys', 'sysfile'), ('sysfile', 'System file'),
                    ('.bat', 'batfile'), ('batfile', 'Windows Batch File'), ('VBS', 'VB Script Language'),
                    ('VBSfile', 'VBScript Script File'),
                    ('.txt', 'txtfile'), ('txtfile', 'Text Document'), ('.ini', 'inifile'),
                    ('inifile', 'Configuration Settings')]
            key = win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE, 'SOFTWARE/Classes', 0,
                                      win32con.KEY_ALL_ACCESS)  # HKEY_LOCAL_MACHINE
            for ext, value in data:
                win32api.RegSetValue(key, ext, win32con.REG_SZ, value)
            win32api.RegCloseKey(key)
            key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER, 'SOFTWARE/Classes', 0,
                                      win32con.KEY_ALL_ACCESS)  # HKEY_CURRENT_USER
            for ext, value in data:
                win32api.RegSetValue(key, ext, win32con.REG_SZ, value)
                try:
                    keyopen = win32api.RegOpenKey(key, ext + r'/shell/open', 0, win32con.KEY_ALL_ACCESS)
                    win32api.RegSetValue(keyopen, 'command', win32con.REG_SZ, '"%1" %*')
                    win32api.RegCloseKey(keyopen)
                except:
                    pass
            win32api.RegCloseKey(key)
            key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER,
                                      'SOFTWARE/Microsoft/Windows/CurrentVersion/Explorer/FileExts', 0,
                                      win32con.KEY_ALL_ACCESS)  # HKEY_CURRENT_USER/SOFTWARE/Microsoft/Windows/CurrentVersion/Explorer/FileExts
            extensions = ['.exe', '.zip', '.dll', '.sys', '.bat', '.txt', '.msc']
            for ext in extensions:
                win32api.RegSetValue(key, ext, win32con.REG_SZ, '')
            win32api.RegCloseKey(key)
            key = win32api.RegOpenKey(win32con.HKEY_CLASSES_ROOT, None, 0, win32con.KEY_ALL_ACCESS)  # HKEY_CLASSES_ROOT
            for ext, value in data:
                win32api.RegSetValue(key, ext, win32con.REG_SZ, value)
                if ext in ['.cmd', '.vbs']:
                    win32api.RegSetValue(key, ext + 'file', win32con.REG_SZ, 'Windows Command Script')
                try:
                    keyopen = win32api.RegOpenKey(key, ext + r'/shell/open', 0, win32con.KEY_ALL_ACCESS)
                    win32api.RegSetValue(keyopen, 'command', win32con.REG_SZ, '"%1" %*')
                    win32api.RegCloseKey(keyopen)
                except:
                    pass
            win32api.RegCloseKey(key)
        except:
            pass
SystemRecoveryEngine = SystemRecoveryEngine()
def SystemRestore():
    while True:
        SystemRecoveryEngine.repair_system_restrict()
        SystemRecoveryEngine.repair_system_file_type()
        SystemRecoveryEngine.repair_system_image()
        SystemRecoveryEngine.repair_system_icon()
def Start_SystemRestore():
    SystemRestore_Start_threading = threading.Thread(target=SystemRestore)
    SystemRestore_Start_threading.daemon = True
    SystemRestore_Start_threading.start()
Start_SystemRestore()

# 主动防御
drive_list = []
for drive in range(ord('A'), ord('Z') + 1):
    drive_name = chr(drive) + ':\\'
    if os.path.exists(drive_name):
        drive_list.append(drive_name)
class FileChangeHandler(FileSystemEventHandler):
    def scscsc(self, event):
        if not event.is_directory:
            exe = event.src_path
            if AntiVirus_file(event.src_path) and (not 'System32' in exe)and (not '360' in exe) and (not 'WindowsApps' in exe):
                def fffff():
                    def chuank(bindu):
                        def shan():
                            window.destroy()
                            os.remove(bindu)

                        def bai():
                            q = open("1.txt", "a")
                            window.destroy()
                            q.write('\n')
                            q.write(bindu)
                            q.close()

                        def ge():
                            v = bindu
                            q2 = open("2.txt", "a")
                            q2.write("\n")
                            q2.write(v)
                            q2.close()
                            geli = open(v, 'rb')
                            geli2 = geli.read()
                            geli.close()
                            last_slash_index = v.rfind("\\")
                            mi = v[last_slash_index + 1:]
                            geli = open(mi + '.w', 'wb')
                            geli.write(geli2)
                            geli.close()
                            time.sleep(5)
                            shan()

                        window = tk.Tk()
                        window.title("jzh杀毒-主动防御")
                        bindu_label = tk.Label(window, text=bindu, font=("Arial", 12))
                        bindu_label.pack(side=tk.BOTTOM, pady=10)
                        delete_button = tk.Button(window, text="删除", font=("Arial", 12), command=shan)
                        whitelist_button = tk.Button(window, text="白名单", font=("Arial", 12), command=bai)
                        geli_button = tk.Button(window, text="隔离", font=("Arial", 12), command=ge)
                        confirm_button = tk.Button(window, text="确定", font=("Arial", 12), command=window.destroy)
                        delete_button.pack(side=tk.BOTTOM, pady=10)
                        whitelist_button.pack(side=tk.BOTTOM, pady=10)
                        geli_button.pack(side=tk.BOTTOM, pady=10)
                        confirm_button.pack(side=tk.BOTTOM, pady=10)
                        window.mainloop()

                    chuank(event.src_path)

                zfang = threading.Thread(target=fffff, name=event.src_path)
                zfang.start()
    def on_modified(self, event):
        self.scscsc(event)
    def on_created(self, event):
        self.scscsc(event)
def monitor_directory(directory):
    event_handler = FileChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, directory, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
for i in drive_list:
    def v():
        monitor_directory(i)
    t = threading.Thread(target=v, name=i)
    t.start()

# 工具
def RepairRegedit():
    subprocess.run(["regedit", "/s", jzhsd_dir + "\\Extens\\Repair\\Repair_Regedit.reg"], check=True, creationflags=subprocess.CREATE_NO_WINDOW)
    messagebox.showinfo("注册表修复完成")
def RepairSystem():
    subprocess.run([jzhsd_dir + "\\Extens\\Repair\\Repair_System.bat"], creationflags=subprocess.CREATE_NO_WINDOW)
    messagebox.showinfo("磁盘修复完成")

# UI
def is_dark_mode():
    try:
        # 访问注册表来检查系统的颜色主题
        registry_key = reg.HKEY_CURRENT_USER
        registry_path = r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
        registry_value = "AppsUseLightTheme"  # 0: Dark mode, 1: Light mode

        # 打开注册表键
        with reg.OpenKey(registry_key, registry_path) as key:
            # 获取设置的值
            value, _ = reg.QueryValueEx(key, registry_value)

            # 如果值为 0，则表示启用了深色模式
            return value == 0
    except Exception as e:
        print("Error detecting dark mode:", e)
        return False
class SysTrayIcon(object):
    QUIT = 'QUIT'
    SPECIAL_ACTIONS = [QUIT]
    FIRST_ID = 5320
    def __init__(self, icon, hover_text, menu_options, on_quit, tk_window=None, default_menu_index=None,
                 window_class_name=None):
        self.icon = icon
        self.hover_text = hover_text
        self.on_quit = on_quit
        self.root = tk_window
        menu_options = menu_options + (('退出', None, self.QUIT),)
        self._next_action_id = self.FIRST_ID
        self.menu_actions_by_id = set()
        print(menu_options,type(menu_options),'menu_options')
        self.menu_options = self._add_ids_to_menu_options(list(menu_options))
        self.menu_actions_by_id = dict(self.menu_actions_by_id)
        print(self.menu_actions_by_id, 'menu_actions_by_id')
        del self._next_action_id

        self.default_menu_index = (default_menu_index or 0)
        self.window_class_name = window_class_name or "SysTrayIconPy"

        message_map = {win32gui.RegisterWindowMessage("TaskbarCreated"): self.restart,
                       win32con.WM_DESTROY: self.destroy,
                       win32con.WM_COMMAND: self.command,
                       win32con.WM_USER + 20: self.notify, }
        # 注册窗口类。
        wc = win32gui.WNDCLASS()
        wc.hInstance = win32gui.GetModuleHandle(None)
        wc.lpszClassName = self.window_class_name
        wc.style = win32con.CS_VREDRAW | win32con.CS_HREDRAW
        wc.hCursor = win32gui.LoadCursor(0, win32con.IDC_ARROW)
        wc.hbrBackground = win32con.COLOR_WINDOW
        wc.lpfnWndProc = message_map  # 也可以指定wndproc.
        self.classAtom = win32gui.RegisterClass(wc)
    def activation(self):
        hinst = win32gui.GetModuleHandle(None)  # 创建窗口。
        style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
        self.hwnd = win32gui.CreateWindow(self.classAtom,
                                          self.window_class_name,
                                          style,
                                          0, 0,
                                          win32con.CW_USEDEFAULT,
                                          win32con.CW_USEDEFAULT,
                                          0, 0, hinst, None)
        win32gui.UpdateWindow(self.hwnd)
        self.notify_id = None
        self.refresh(title='软件已后台！', msg='JZH杀毒已隐藏至托盘', time=500)

        win32gui.PumpMessages()
    def refresh(self, title='', msg='', time=500):
        hinst = win32gui.GetModuleHandle(None)
        hicon = win32gui.LoadIcon(0, win32con.IDI_APPLICATION)

        if self.notify_id:
            message = win32gui.NIM_MODIFY
        else:
            message = win32gui.NIM_ADD

        self.notify_id = (self.hwnd, 0,  # 句柄、托盘图标ID
                          win32gui.NIF_ICON | win32gui.NIF_MESSAGE | win32gui.NIF_TIP | win32gui.NIF_INFO,
                          # 托盘图标可以使用的功能的标识
                          win32con.WM_USER + 20, hicon, self.hover_text,  # 回调消息ID、托盘图标句柄、图标字符串
                          msg, time, title,  # 提示内容、提示显示时间、提示标题
                          win32gui.NIIF_INFO  # 提示用到的图标
                          )
        win32gui.Shell_NotifyIcon(message, self.notify_id)
    def show_menu(self):
        menu = win32gui.CreatePopupMenu()
        self.create_menu(menu, self.menu_options)

        pos = win32gui.GetCursorPos()
        win32gui.SetForegroundWindow(self.hwnd)
        win32gui.TrackPopupMenu(menu,
                                win32con.TPM_LEFTALIGN,
                                pos[0],
                                pos[1],
                                0,
                                self.hwnd,
                                None)
        win32gui.PostMessage(self.hwnd, win32con.WM_NULL, 0, 0)
    def _add_ids_to_menu_options(self, menu_options):
        result = []
        for menu_option in menu_options:
            option_text, option_icon, option_action = menu_option
            if callable(option_action) or option_action in self.SPECIAL_ACTIONS:
                self.menu_actions_by_id.add((self._next_action_id, option_action))
                result.append(menu_option + (self._next_action_id,))
            else:
                result.append((option_text,
                               option_icon,
                               self._add_ids_to_menu_options(option_action),
                               self._next_action_id))
            self._next_action_id += 1
        print(result,'result')
        return result
    def restart(self, hwnd, msg, wparam, lparam):
        self.refresh()
    def destroy(self, hwnd=None, msg=None, wparam=None, lparam=None, self_exit=1):
        nid = (self.hwnd, 0)
        win32gui.Shell_NotifyIcon(win32gui.NIM_DELETE, nid)
        win32gui.PostQuitMessage(0)  # 终止应用程序。
        if self_exit and self.on_quit:
            self.on_quit()  # 需要传递自身过去时用 s.on_quit(s)
        else:
            self.root.deiconify()  # 显示tk窗口
    def notify(self, hwnd, msg, wparam, lparam):
        if lparam == win32con.WM_LBUTTONDBLCLK:  # 双击左键
            pass
        elif lparam == win32con.WM_RBUTTONUP:  # 右键弹起
            self.show_menu()
        elif lparam == win32con.WM_LBUTTONUP:  # 左键弹起
            self.destroy(self_exit=0)
        return True
    def create_menu(self, menu, menu_options):
        for option_text, option_icon, option_action, option_id in menu_options[::-1]:
            if option_icon:
                option_icon = self.prep_menu_icon(option_icon)

            if option_id in self.menu_actions_by_id:
                item, extras = win32gui_struct.PackMENUITEMINFO(text=option_text,
                                                                hbmpItem=option_icon,
                                                                wID=option_id)
                win32gui.InsertMenuItem(menu, 0, 1, item)
            else:
                submenu = win32gui.CreatePopupMenu()
                self.create_menu(submenu, option_action)
                item, extras = win32gui_struct.PackMENUITEMINFO(text=option_text,
                                                                hbmpItem=option_icon,
                                                                hSubMenu=submenu)
                win32gui.InsertMenuItem(menu, 0, 1, item)
    def prep_menu_icon(self, icon):
        # 加载图标。
        ico_x = win32api.GetSystemMetrics(win32con.SM_CXSMICON)
        ico_y = win32api.GetSystemMetrics(win32con.SM_CYSMICON)
        hicon = win32gui.LoadImage(0, icon, win32con.IMAGE_ICON, ico_x, ico_y, win32con.LR_LOADFROMFILE)

        hdcBitmap = win32gui.CreateCompatibleDC(0)
        hdcScreen = win32gui.GetDC(0)
        hbm = win32gui.CreateCompatibleBitmap(hdcScreen, ico_x, ico_y)
        hbmOld = win32gui.SelectObject(hdcBitmap, hbm)
        brush = win32gui.GetSysColorBrush(win32con.COLOR_MENU)
        win32gui.FillRect(hdcBitmap, (0, 0, 16, 16), brush)
        win32gui.DrawIconEx(hdcBitmap, 0, 0, hicon, ico_x, ico_y, 0, 0, win32con.DI_NORMAL)
        win32gui.SelectObject(hdcBitmap, hbmOld)
        win32gui.DeleteDC(hdcBitmap)

        return hbm
    def command(self, hwnd, msg, wparam, lparam):
        self_id = win32gui.LOWORD(wparam)
        self.execute_menu_option(self_id)
    def execute_menu_option(self, self_id):
        menu_action = self.menu_actions_by_id[self_id]
        if menu_action == self.QUIT:
            win32gui.DestroyWindow(self.hwnd)
        else:
            menu_action(self)
class _Main:  # 调用SysTrayIcon的Demo窗口
    def __init__(self):
        self.cv = []
        self.SysTrayIcon = None  # 判断是否打开系统托盘图标
    def main(self):
        self.s = tkt.Tk(title="jzh杀毒")  # tk窗口
        self.s.iconbitmap(os.path.dirname(sys.argv[0])+"\\2.ico")
        self.s.center()
        self.s.resizable(False, False)
        def shua_xin():
            for i in self.cv:
                i.destroy()
            self.cv = []
        shua_xin()
        def kscs():
            shua_xin()
            self.cv.append(tkt.Button(cv, (1050, 80), (170, 50), text="查杀文件", command=cs))
            self.cv.append(tkt.Text(cv, (420, 80), text="病毒扫描", fontsize=40))
            self.cv.append(tkt.Text(cv, (420, 170), text="扫描结果：", fontsize=30))
            self.cv.append(tkt.Text(cv, (400, 210), text="——————————————————————————", fontsize=30))
            self.s.mainloop()
        def cs():
            def xz(i):
                def sc():
                    os.remove(theLB.get(tk.ACTIVE))
                    theLB.delete(tk.ACTIVE)
                def gl():
                    IsolationList = open("2.txt", "a")
                    Virus = open(theLB.get(tk.ACTIVE), 'rb')
                    Virus_trust = Virus.read()
                    Virus.close()
                    last_slash_index = theLB.get(tk.ACTIVE).rfind("\\")
                    mi = theLB.get(tk.ACTIVE)[last_slash_index + 1:]
                    Virus = open(mi + '.w', 'wb')
                    Virus.write(Virus_trust)
                    IsolationList.write("\n")
                    IsolationList.write(theLB.get(tk.ACTIVE))
                    IsolationList.close()
                    Virus.close()
                    while True:
                        try:
                            with open(mi + '.w', 'r+'):
                                break
                        except:
                            time.sleep(0.5)
                    os.remove(theLB.get(tk.ACTIVE))
                    theLB.delete(tk.ACTIVE)
                def xr():
                    WhiteList = open("1.txt", "a")
                    WhiteList.write("\n")
                    WhiteList.write(theLB.get(tk.ACTIVE).replace("/", "\\"))
                    Viruses_White_exe.append(theLB.get(tk.ACTIVE).replace("/", "\\"))
                    theLB.delete(tk.ACTIVE)
                shua_xin()
                self.cv.append(tkt.Button(cv, (1050, 80), (170, 50), text="查杀文件", command=cs))
                self.cv.append(tkt.Text(cv, (420, 80), text="病毒扫描", fontsize=40))
                self.cv.append(tkt.Text(cv, (420, 170), text="扫描结果：", fontsize=30))
                self.cv.append(tkt.Text(cv, (400, 210), text="——————————————————————————", fontsize=30))
                self.cv.append(tkt.Button(cv, (1050, 160), (80, 50), text="删除", command=sc))
                self.cv.append(tkt.Button(cv, (1140, 160), (80, 50), text="隔离", command=gl))
                self.cv.append(tkt.Button(cv, (960, 160), (80, 50), text="信任", command=xr))
                if i == 0:
                    f = filedialog.askopenfilename(title="jzh杀毒-文件选择")
                    print(f.replace("/", "\\"))
                    print(Viruses_White_exe)
                    print(f.replace("/", "\\") in Viruses_White_exe)
                    a = AntiVirus_file(f)
                    print(a)
                    print(1)
                    if is_dark_mode():
                        print(2)
                        theLB = tk.Listbox(self.s, bg="black", fg="white", width=75, height=20)
                    else:
                        theLB = tk.Listbox(self.s, bg="white", fg="black", width=75, height=20)
                    theLB.place(x=390, y=200)
                    print(3)
                    if a:
                        for item in [f]:
                            theLB.insert(tk.END, item)
                    else:
                        for item in []:
                            theLB.insert(tk.END, item)
                else:
                    folder_path = filedialog.askdirectory(title="jzh杀毒-文件夹选择")
                    if is_dark_mode():
                        theLB = tk.Listbox(self.s, bg="black", fg="white", width=75, height=20)
                    else:
                        theLB = tk.Listbox(self.s, bg="white", fg="black", width=75, height=20)
                    theLB.place(x=390, y=200)
                    for item in AntiVirus_folder(folder_path):
                        theLB.insert(tk.END, item)
                self.cv.append(theLB)
                self.s.mainloop()
            shua_xin()
            self.cv.append(tkt.Text(cv, (420, 80), text="病毒扫描", fontsize=40))
            self.cv.append(tkt.Text(cv, (420, 170), text="扫描结果：", fontsize=30))
            self.cv.append(tkt.Text(cv, (400, 210), text="——————————————————————————", fontsize=30))
            self.cv.append(tkt.SegmentedButton(cv, (1050, 80), text=("文件扫描", "路径扫描"), command=xz))
            self.s.mainloop()
        def kscses():
            shua_xin()
            def delete_line(line_number):
                with open('2.txt', 'r') as file:
                    lines = file.readlines()
                lines.pop(line_number - 1)  # 删除指定行
                with open('2.txt', 'w') as file:
                    file.writelines(lines)
            try:
                f = open("2.txt", "r")
                m = f.read()
                f.close()
                if m[0] == '\n':
                    delete_line(1)
            except:
                pass
            f = open('2.txt', 'r')
            fp = f.read().split("\n")
            f.close()
            fr = []
            for d in fp:
                if not d == '':
                    fr.append(d)
            def hf(v, n):
                last = v.rfind("\\")
                mi = v[last + 1:] + '.w'
                f2 = open(mi, 'rb')
                f3 = open(v, 'wb')
                f3.write(f2.read())
                f2.close()
                f3.close()
                os.remove(mi)
                delete_line(n + 1)
                return ''
            if is_dark_mode():
                theLB = tk.Listbox(self.s, bg="black", fg="white", width=75, height=20)
            else:
                theLB = tk.Listbox(self.s, bg="white", fg="black", width=75, height=20)
            theLB.place(x=390, y=200)
            for item in fr:
                theLB.insert(tk.END, item)
            def sc():
                selected_item = theLB.get(tk.ACTIVE)  # 获取当前选中的项
                selected_indices = theLB.curselection()
                a, = selected_indices
                hf(selected_item, a)
                theLB.delete(tk.ACTIVE)  # 删除当前选中的
                kscses()
            self.cv.append(tkt.Text(cv, (420, 80), text="找回隔离文件", fontsize=40))
            self.cv.append(tkt.Text(cv, (420, 170), text="全部隔离文件：", fontsize=30))
            self.cv.append(tkt.Button(cv, (1140, 160), (80, 50), text="恢复", command=sc))
            self.cv.append(theLB)
            self.s.mainloop()
        def WhitelistManagement():
            shua_xin()
            def delete_line(line_number):
                with open('1.txt', 'r') as file:
                    lines = file.readlines()
                lines.pop(line_number - 1)  # 删除指定行
                with open('1.txt', 'w') as file:
                    file.writelines(lines)
            try:
                f = open("1.txt", "r")
                m = f.read()
                f.close()
                if m[0] == '\n':
                    delete_line(1)
            except:
                pass
            f = open('1.txt', 'r')
            fr = f.read().split("\n")
            if is_dark_mode():
                theLB = tk.Listbox(self.s, bg="black", fg="white", width=75, height=20)
            else:
                theLB = tk.Listbox(self.s, bg="white", fg="black", width=75, height=20)
            theLB.place(x=390, y=200)
            for item in fr:
                theLB.insert(tk.END, item)
            def sc():
                selected_item = theLB.get(tk.ACTIVE).replace("/", "\\")  # 获取当前选中的项
                Viruses_White_exe.remove(selected_item)
                theLB.delete(tk.ACTIVE)
                with open('1.txt', 'w') as file:
                    file.writelines("\n".join(Viruses_White_exe))
                WhitelistManagement()
            def cs():
                v = filedialog.askopenfilename(title="jzh杀毒-文件选择")
                Viruses_White_exe.append(v)
                q = open("1.txt", "a")
                q.write("\n")
                q.write(v)
                q.close()
                WhitelistManagement()
            self.cv.append(tkt.Button(cv, (1050, 160), (80, 50), text="删除", command=sc))
            self.cv.append(tkt.Button(cv, (1140, 160), (80, 50), text="添加", command=cs))
            self.cv.append(tkt.Text(cv, (420, 80), text="管理白名单", fontsize=40))
            self.cv.append(tkt.Text(cv, (420, 170), text="白名单内容：", fontsize=30))
            self.cv.append(theLB)

            f.close()
        def sz():
            shua_xin()
            self.cv.append(tkt.Text(cv, (420, 80), text="设置", fontsize=40))
        def xgj():
            shua_xin()
            self.cv.append(tkt.Text(cv, (420, 80), text="小工具", fontsize=40))
            self.cv.append(tkt.Button(cv, (420, 170), (820, 70), text="注册表修复", command=RepairSystem))
            self.cv.append(tkt.Button(cv, (420, 250), (820, 70), text="磁盘修复", command=RepairRegedit))
            self.s.mainloop()
        cv = tkt.Canvas(self.s, zoom_item=True, keep_ratio="min", free_anchor=True)
        cv.place(width=1300, height=800, x=640, y=360, anchor="center")
        self.cv.append(tkt.Button(cv, (1050, 80), (170, 50), text="查杀文件", command=cs))
        self.cv.append(tkt.Text(cv, (420, 80), text="病毒扫描", fontsize=40))
        self.cv.append(tkt.Text(cv, (420, 170), text="扫描结果：", fontsize=30))
        self.cv.append(tkt.Text(cv, (400, 210), text="——————————————————————————", fontsize=30))
        tkt.Button(cv, (20, 40), (340, 100), text="快速查杀", command=kscs)
        tkt.Button(cv, (20, 150), (340, 100), text="白名单", command=WhitelistManagement)
        tkt.Button(cv, (20, 260), (340, 100), text="找回隔离文件", command=kscses)
        tkt.Button(cv, (20, 370), (340, 100), text="小工具", command=xgj)
        tkt.Button(cv, (20, 480), (340, 100), text="设置", command=sz)
        self.s.bind("<Unmap>", lambda event: self.Hidden_window() if self.s.state() == 'iconic' else False)
        self.s.protocol('WM_DELETE_WINDOW', self.guanbi)
        self.s.mainloop()
    def guanbi(self):
        res = messagebox.askokcancel('提示', '是否退出JZH杀毒与所有其提供的保护？')
        if res:
            LoadingScreen = open("4.txt", "w")
            LoadingScreen.write("1")
            LoadingScreen.close()
            for proc in psutil.process_iter(['pid', 'name', 'exe']):
                try:
                    exe = proc.info['exe']
                    if ide:
                        if "python" in os.path.basename(exe):
                            off_rtcore64(proc.pid)
                            proc.kill()
                    else:
                        if os.path.basename(sys.argv[0]) == os.path.basename(exe):
                            off_rtcore64(proc.pid)
                            proc.kill()
                except:
                    pass
            self.s.destroy()
            sys.exit()
        sys.exit()
    def show_msg(self, title='标题', msg='内容', time=500):
        self.SysTrayIcon.refresh(title=title, msg=msg, time=time)
    def switch_icon(self, _sysTrayIcon, icon='2.ico'):
        # 点击右键菜单项目会传递SysTrayIcon自身给引用的函数，所以这里的_sysTrayIcon = s.sysTrayIcon
        # 只是一个改图标的例子，不需要的可以删除此函数
        _sysTrayIcon.icon = icon
        _sysTrayIcon.refresh()
    def Hidden_window(self, icon='aaa.ico', hover_text="JZH杀毒"):
        self.s.protocol('WM_DELETE_WINDOW', self.exit)
        # 托盘图标右键菜单, 格式: ('name', None, callback),下面也是二级菜单的例子
        # 24行有自动添加‘退出’，不需要的可删除
        menu_options = ()
        self.s.withdraw()  # 隐藏tk窗口
        if not self.SysTrayIcon: self.SysTrayIcon = SysTrayIcon(
            icon,  # 图标
            hover_text,  # 光标停留显示文字
            menu_options,  # 右键菜单
            on_quit=self.exit,  # 退出调用
            tk_window=self.s,  # Tk窗口
        )
        self.SysTrayIcon.activation()
        self.s.protocol('WM_DELETE_WINDOW', self.guanbi)
    def exit(self, _sysTrayIcon=None):
        self.guanbi()
Main = _Main()
OffLoadingScreen()
Main.main()