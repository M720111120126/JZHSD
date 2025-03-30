import json, sys, urllib.request, hashlib, time, yara, psutil, ctypes, shutil
import urllib.parse, numpy, onnxruntime, pefile, urllib.parse, subprocess
from pefile import *
from hashlib import md5
import xml.etree.ElementTree as et
from ctypes import wintypes
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk
if os.path.exists("4.txt"):
    root_jiazai = tk.Tk()
    root_jiazai.overrideredirect(True)
    window_width = 800
    window_height = 500
    root_jiazai.geometry(
        f"{window_width}x{window_height}+{(root_jiazai.winfo_screenwidth() - window_width) // 2}+{(root_jiazai.winfo_screenheight() - window_height) // 2 - 50}")
    root_jiazai.attributes("-topmost", True)
    root_jiazai.wm_attributes("-transparentcolor", "white")
    root_jiazai.configure(bg='white')
    canvas = tk.Canvas(root_jiazai, width=window_width, height=window_height, bg="white", bd=0,
                       highlightthickness=0)
    canvas.pack()
    radius = 20
    canvas.create_oval(0, 0, 2 * radius, 2 * radius, fill="#000", width=0)  # 左上角圆角
    canvas.create_oval(window_width - 2 * radius, 0, window_width, 2 * radius, fill="#000", width=0)  # 右上角圆角
    canvas.create_oval(0, window_height - 2 * radius, 2 * radius, window_height, fill="#000", width=0)  # 左下角圆角
    canvas.create_oval(window_width - 2 * radius, window_height - 2 * radius, window_width, window_height,
                       fill="#000",
                       width=0)  # 右下角圆角
    canvas.create_rectangle(radius, 0, window_width - radius, window_height, fill="#000", width=0)
    canvas.create_rectangle(0, radius, window_width, window_height - radius, fill="#000", width=0)
    image_path = "path_to_your_image.jpg"  # 替换为你的图片路径
    image = Image.open("1.png")
    max_width = 200  # 最大宽度
    max_height = 600  # 最大高度
    image.thumbnail((max_width, max_height))  # 调整图片比例，保持长宽比
    image_123 = ImageTk.PhotoImage(image)
    svg = tk.Label(root_jiazai, image=image_123, fg="lightblue", bg="#000")
    svg.place(anchor="center", x=110, y=450)
    label = tk.Label(root_jiazai, text="JZH杀毒——V3 重构版", font=("Arial", 30), fg="lightblue", bg="#000")
    label.place(relx=0.5, rely=0.2, anchor="center")
    label2 = tk.Label(root_jiazai, text="""JZH杀毒优势：
        不易发现
        --python本身无毒，用较好的方法可以实现不被其他杀软报毒
        可对抗性
        --多数病毒在设计之初没有想到有一天会和python对抗
        自动内存管理
        --降低了内存泄漏等错误的风险
        良好的可维护性
        --更好的修复BUG
        异步编程
        --提高软件的性能和响应能力""", font=("Arial", 13), fg="lightblue", bg="#000", justify="left")
    label2.place(relx=0.7, rely=0.65, anchor="center")
    def a():
        print(1)
        directory = '.'
        files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        while os.path.exists("4.txt"):
            time.sleep(0.5)
        print(2)
        root_jiazai.destroy()
    root_jiazai.after(100, a)
    print(3)
    root_jiazai.mainloop()
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
        if os.path.basename(sys.argv[0]) == os.path.basename(exe):
            on_rtcore64(proc.pid)
    except:
        pass
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
Viruses_Quarantine_exe = []
def Get_VirusesQuarantine():
    def delete_line(line_number):
        with open('2.txt', 'r') as file:
            lines = file.readlines()
        lines.pop(line_number - 1)
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
    Viruses_Quarantine_f = open('2.txt', 'r')
    Viruses_Quarantine_fp = Viruses_Quarantine_f.read().split("\n")
    Viruses_Quarantine_f.close()
    for d in Viruses_Quarantine_fp:
        if not d == '':
            Viruses_Quarantine_exe.append(d)
Get_VirusesQuarantine()
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
def PreventVirusStartup(process):
    off_rtcore64(process.pid)
    process.kill()
    root = tk.Tk()
    root.geometry("450x250")
    root.resizable(False, False)
    root.attributes('-topmost', True)
    root.overrideredirect(True)
    virus_path = process.exe()
    style = ttk.Style()
    style.configure("TLabel", font=("Microsoft YaHei", 14), foreground="red")
    label = ttk.Label(root, text="有风险程序正在启动，建议删除")
    label.pack(pady=20)
    label = tk.Label(root, text=f"风险程序: {virus_path}", font=("Arial", 12))
    label.pack(pady=20)
    local_time = time.localtime()
    label = tk.Label(root, text=f"拦截时间：{time.strftime("%Y.%m.%d %H:%M", local_time)}", font=("Arial", 12))
    label.pack(pady=20)
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)
    def on_ignore():
        root.quit()
        root.destroy()
    ignore_button = tk.Button(button_frame, text="暂不处理", command=on_ignore, width=12)
    ignore_button.grid(row=0, column=0, padx=10)
    def on_delete():
        os.remove(process.exe())
        root.quit()
        root.destroy()
    delete_button = tk.Button(button_frame, text="删除", command=on_delete, width=12)
    delete_button.grid(row=0, column=1, padx=0)
    def on_show_more_options():
        if option_menu_visible[0]:
            option_menu_visible[0] = False
            triangle_button.config(text="▼")
            option_menu.unpost()
        else:
            option_menu_visible[0] = True
            triangle_button.config(text="▲")
            option_menu.post(triangle_button.winfo_rootx(),
                             triangle_button.winfo_rooty() + triangle_button.winfo_height())

    button_height = delete_button.winfo_height()
    triangle_button = tk.Button(button_frame, text="▼", command=on_show_more_options, height=1)
    triangle_button.grid(row=0, column=2, padx=0)  # 与删除按钮紧密连接
    def on_add_to_white_list():
        WhiteList = open("1.txt", "a")
        WhiteList.write("\n")
        WhiteList.write(process.exe)
        root.quit()
        root.destroy()
    def on_isolate_file():
        IsolationList = open("2.txt", "a")
        Virus = open(process.exe(), 'rb')
        Virus_trust = Virus.read()
        Virus.close()
        last_slash_index = process.exe().rfind("\\")
        mi = process.exe()[last_slash_index + 1:]
        Virus = open(mi + '.w', 'wb')
        Virus.write(Virus_trust)
        IsolationList.write("\n")
        IsolationList.write(process.exe())
        IsolationList.close()
        Virus.close()
        while True:
            try:
                with open(mi + '.w', 'r+'):
                    break
            except:
                time.sleep(0.5)
        os.remove(process.exe())
        root.quit()
        root.destroy()
    option_menu = tk.Menu(root, tearoff=0)
    option_menu.add_command(label="添加至白名单", command=on_add_to_white_list)
    option_menu.add_command(label="隔离文件", command=on_isolate_file)
    option_menu_visible = [False]
    def hide_menu(event):
        if option_menu_visible[0]:
            option_menu_visible[0] = False
            triangle_button.config(text="▼")
            option_menu.unpost()
    root.bind("<Button-1>", hide_menu)
    root.mainloop()

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
    def scan_ANK(self, file_path):
        if file_path.replace("/", "\\") in Viruses_White_exe:
            return False
        process = subprocess.Popen(f'"{os.path.dirname(sys.argv[0])}\\ANK_OEMSERVE\\OEM_ANKCORE.exe" "{file_path}"',
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=f'{os.path.dirname(sys.argv[0])}\\ANK_OEMSERVE', creationflags=subprocess.CREATE_NO_WINDOW)
        stdout, stderr = process.communicate()
        return float(stderr) >= 0.9
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
data_path = appdata_path + "\\Local\\mlnet-resources\\Text\\Sswe"
shutil.copy2(jzhsd_dir + "\\sentiment.emd", appdata_path.replace("\\Roaming", "") + "\\Local\\mlnet-resources\\Text\\Sswe\\sentiment.emd")
def AntiVirus_file(f_path, online=online):
    try:
        if f_path.replace("/", "\\") in Viruses_White_exe:
            return False
        pe_scan = AntivirusEngine.pe_scan(f_path)
        f_da = open(f_path, "rb")
        f_data = f_da.read()
        f_da.close()
        try:
            if AntivirusEngine.scan_ANK(f_path):
                return True
        except:
            pass
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
    except:
        return False
def ActiveDefense(AntivirusEngine):
    kernel32 = ctypes.windll.kernel32
    HANDLE = wintypes.HANDLE
    SuspendThread = kernel32.SuspendThread
    ResumeThread = kernel32.ResumeThread
    THREAD_SUSPEND_RESUME = 0x2
    def start_and_suspend_process(process):
        threads = process.threads()
        if AntivirusEngine(process.exe()) and not "JZH" in process.exe() and not "jzh" in process.exe() and not "Scanner_SDK_HTTP2_SHA256" in process.exe() and not "Sys" in process.exe():
            PreventVirusStartup(process)
        else:
            for thread in threads:
                thread_handle = kernel32.OpenThread(THREAD_SUSPEND_RESUME, False, thread.id)
                if thread_handle:
                    ResumeThread(thread_handle)
                else:
                    print(process.exe()+"ffff")
    current_procs_old = []
    for proc in psutil.process_iter(['pid', 'name', 'exe']):
        try:
            current_procs_old.append(proc)
        except:
            pass
    while True:
        if os.path.exists("4.txt"):
            for proc in psutil.process_iter(['pid', 'name', 'exe']):
                try:
                    exe = proc.info['exe']
                    if os.path.basename(sys.argv[0]) == os.path.basename(exe):
                        off_rtcore64(proc.pid)
                        proc.kill()
                except:
                    pass
        current_procs_new = []
        for proc in psutil.process_iter(['pid', 'name', 'exe']):
            try:
                if not proc in current_procs_old:
                    current_procs_new.append(proc)
                    current_procs_old.append(proc)
                    threads = proc.threads()
                    for thread in threads:
                        thread_handle = kernel32.OpenThread(THREAD_SUSPEND_RESUME, False, thread.id)
                        if thread_handle:
                            SuspendThread(thread_handle)
            except:
                pass
        print(current_procs_old+[1])
        print(current_procs_new+[2])
        for proc in current_procs_new:
            try:
                start_and_suspend_process(proc)
            except:
                pass
ActiveDefense(AntiVirus_file)
