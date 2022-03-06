import tkinter as tk
import pygetwindow as gw
import pyautogui
import time
from Modules.Classes import Lobby
from Modules.TableAgencement import organize_playground
from PIL import ImageTk, Image, ImageOps, ImageEnhance
import pywinauto
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'Tesseract-OCR\tesseract.exe'
import cv2
import os

class Application(tk.Frame):
	def __init__(self):
		self.root = tk.Tk()
		tk.Frame.__init__(self)
		self.root.geometry("500x600")
		self.grid()

		self.home = tk.Button(self, text="START")
		self.home.bind('<Button-1>', self.go_home)
		self.home.grid()

	def go_home(self, event):
		for element in self.grid_slaves():
			element.grid_forget()
		self.root.geometry("500x600")		
		self.launcher = tk.Button(self, text="Launch_Session")
		self.launcher.bind('<Button-1>', self.launch_session)
		self.launcher.grid()
		self.get_BR_button = tk.Button(self, text="Get Bankroll")
		self.get_BR_button.bind('<Button-1>', self.get_bankroll)
		self.get_BR_button.grid()
		self.cashout_button = tk.Button(self, text="Add Cashout to DB")
		self.cashout_button.bind('<Button-1>', self.cashout)
		self.cashout_button.grid()
		self.reorganize_button = tk.Button(self, text="Reorganize tables")
		self.reorganize_button.bind('<Button-1>', organize_playground)
		self.reorganize_button.grid()

		self.minus9bb = tk.Button(self, text = "Push 5-9BB")
		self.minus9bb.bind("<Button-1>", lambda event: self.range_display(event, path = '5-9bb'))
		self.minus9bb.grid()

		self.minus14bb = tk.Button(self, text = "Push 10-14BB")
		self.minus14bb.bind("<Button-1>", lambda event: self.range_display(event, path = '10-14bb'))
		self.minus14bb.grid()

		self.minus19bb = tk.Button(self, text = "Push 15-19BB")
		self.minus19bb.bind("<Button-1>", lambda event: self.range_display(event, path = '15-19bb'))
		self.minus19bb.grid()

		self.minus25bb = tk.Button(self, text = "Push 20-25BB")
		self.minus25bb.bind("<Button-1>", lambda event: self.range_display(event, path = '20-25bb'))
		self.minus25bb.grid()		


	def range_display(self, event, path):
		for element in self.grid_slaves():
			element.grid_forget()	
		self.root.geometry("900x1000")
		path = 'Ranges_screenshots/' + path
		files = ['SB.jpg', 'BTN.jpg', 'CO.jpg', 'HJ.jpg', 'LJ.jpg', 'UTG.jpg', 'UTG1.jpg', 'UTG2.jpg', 'legend.jpg']
		self.canvas = tk.Canvas(self, width = 900, height = 900)
		coords = [(150,150),(450,150),(750,150),(150,450),(450,450),(750,450),(150,750),(450,750),(750,750)]
		self.img_list = [Image.open(path + '/' + f).resize((300, 300), Image.ANTIALIAS) for f in files]
		self.img_list = [ImageTk.PhotoImage(im) for im in self.img_list]
		for i, img in enumerate(self.img_list):
			self.canvas.create_image(coords[i][0], coords[i][1], image = img)
		self.canvas.grid()

		self.home = tk.Button(self, text="BACK")
		self.home.bind('<Button-1>', self.go_home)
		self.home.grid()

	def launch_session(self, event):
		print("launch session...")
		pywinauto.application.Application(backend="uia").start(r"C:\Users\grego\Winamax\Winamax Poker\Winamax Poker.exe")
		pywinauto.application.Application(backend="uia").start(r"C:\Program Files (x86)\PokerStars.FR\PokerStars.exe")
		pywinauto.application.Application(backend="uia").start(r"C:\PMU\PMU.exe -P=PMUPoker")		
		print("session launch over")

	def focus_to_window(self, window):
		if window.isActive == False:
			pywinauto.application.Application(backend="uia").connect(handle=window._hWnd).top_window().set_focus()	

	def digitListToFloat(self, digitslist):
		digitslist.insert(-2, '.')
		return float(''.join(digitslist))
	
	def getWinaBR(self, Window):
		now = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
		if Window.isMinimized:
			Window.maximize()
		self.focus_to_window(Window)
		Window.resizeTo(1280,720)
		Window.moveTo(440,160)
		pyautogui.moveTo(601,307)
		pyautogui.click()
		time.sleep(1)
		img = pyautogui.screenshot('Bankroll_screenshots/wina_test_{}.jpg'.format(now),region=(685, 316, 78, 20))
		pyautogui.moveTo(513,230)
		pyautogui.click()
		img = cv2.imread('Bankroll_screenshots/wina_test_{}.jpg'.format(now))
		img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

		text = pytesseract.image_to_string(img)
		print(text)
		digitsonly = [l for l in text if l.isdigit()]
		#digitsonly.pop() 
		#le vient de quand le signe € est pris pour un 3 par pytesseract donc:
		#if not "€" in text:
			#text.pop()
		#pseudo code a changer
		if not "€" in text:
			digitsonly.pop()
		print(digitsonly)
		return self.digitListToFloat(digitsonly)

	def getPsBR(self, Window):
		now = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
		if Window.isMinimized:
		    Window.maximize()
		self.focus_to_window(Window)
		Window.resizeTo(1280, 729)
		Window.moveTo(280,130)
		img = pyautogui.screenshot('Bankroll_screenshots/PS_test_{}.jpg'.format(now),region=(1336, 213, 95, 20))
		img = cv2.imread('Bankroll_screenshots/PS_test_{}.jpg'.format(now))
		img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
		img = cv2.bitwise_not(img)

		text = pytesseract.image_to_string(img)
		print(text)
		digitsonly = [l for l in text if l.isdigit()]
		print(digitsonly)
		return self.digitListToFloat(digitsonly)

	def getPmuBR(self, Window):
		#bug chelou: active pas la fenetre si elle est pas à minima visible sur l'écran
		now = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
		Window = gw.getWindowsWithTitle('PMU Poker : Écran principal du poker')[0]
		if Window.isMinimized:
		    Window.maximize()
		self.focus_to_window(Window)
		Window.resizeTo(1356, 727)
		Window.moveTo(250,150)

		pyautogui.moveTo(1523, 209)
		pyautogui.click()
		time.sleep(2)
		img = pyautogui.screenshot('Bankroll_screenshots/PMU_test_{}.jpg'.format(now), region=(1053, 441, 108, 32))

		img = cv2.imread('Bankroll_screenshots/PMU_test_{}.jpg'.format(now))
		img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
		text = pytesseract.image_to_string(img)
		print(text)
		digitsonly = [l for l in text if l.isdigit()]
		print(digitsonly)
		return self.digitListToFloat(digitsonly)

	def cashout(self, event):
		self.x = tk.Entry(self, text='amount to cashout')
		self.x.grid()
		self.x_validation = tk.Button(self, text ='write cash out to db')
		self.x_validation.bind('<Button-1>', self.write_cashout_to_db)
		self.x_validation.grid()

	def write_cashout_to_db(self, event):
		import sqlite3
		import time
		print(self.x.get())
		db = sqlite3.connect('DATASTORE/appDB.db') #la crée si elle n'existe pa
		cur = db.cursor()
		cur.execute('CREATE TABLE IF NOT EXISTS Cashout\
		(id INTEGER PRIMARY KEY, date TEXT, amount REAL)')

		cur.execute("INSERT INTO Cashout (date, amount) values (?, ?)",
		            (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),self.x.get()))
		db.commit()
		import pandas as pd
		print(pd.read_sql_query('SELECT * FROM Cashout', db))

	def get_bankroll(self, event):
		try:
			self.BR_result.grid_forget()
			self.start_BR_to_db.grid_forget()
			self.end_BR_to_db.grid_forget()
			self.ungrid_shits.grid_forget()

		except:
			pass
		for x in pyautogui.getAllWindows():  
			print(x.title)
		
		Lobby_list = gw.getWindowsWithTitle('Lobby')
		print(Lobby_list)
		Winamax = [l for l in Lobby_list if l.title == 'Lobby'][0]
		
		PokerStars = gw.getWindowsWithTitle('Pokerstars Lobby')[0]
		PMU = gw.getWindowsWithTitle('PMU Poker : Écran principal du poker')[0]
		BR_PMU = self.getPmuBR(PMU)
		BR_PS = self.getPsBR(PokerStars)
		BR_W = self.getWinaBR(Winamax)
		
		total_BR = BR_W + BR_PMU + BR_PS
		total_BR_string = "Bankroll Winamax: {} \nBankroll PokerStars: {}  \nBankroll PMU: {}: \n Total Bankroll: {}".format(BR_W, BR_PS, BR_PMU, total_BR)


		self.BR_result = tk.Label(self, text=total_BR_string)
		self.BR_result.grid()
		
		self.start_BR_to_db = tk.Button(self, text = "Write Sarting Bankroll to DB")
		self.start_BR_to_db.bind("<Button-1>", lambda event: self.write_BR_to_db(event, BR = total_BR, start = 1))
		self.start_BR_to_db.grid()

		self.end_BR_to_db = tk.Button(self, text = "Write Ending Bankroll to DB")
		self.end_BR_to_db.bind("<Button-1>", lambda event: self.write_BR_to_db(event, BR = total_BR, start = 0))
		self.end_BR_to_db.grid()

		self.ungrid_shits = tk.Button(self, text = "Ungrid shits")
		self.ungrid_shits.bind("<Button-1>", self.ungrid)
		self.ungrid_shits.grid()
		
	def ungrid(self, event):
		self.BR_result.grid_forget()
		self.start_BR_to_db.grid_forget()
		self.end_BR_to_db.grid_forget()
		self.ungrid_shits.grid_forget()

	def write_BR_to_db(self, event, BR, start):
		import sqlite3
		import time

		db = sqlite3.connect('DATASTORE/appDB.db') #la crée si elle n'existe pa
		cur = db.cursor()
		cur.execute('CREATE TABLE IF NOT EXISTS BR\
		(id INTEGER PRIMARY KEY, date TEXT, bankroll REAL, start INT)')

		cur.execute("INSERT INTO BR (date, bankroll, start) values (?, ?, ?)",
		            (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),BR, start))
		db.commit()
		import pandas as pd
		print(pd.read_sql_query('SELECT * FROM BR', db))

	def start(self):
		self.root.mainloop()

Application().start()