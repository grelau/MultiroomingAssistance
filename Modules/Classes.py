import pyautogui
import time
import pygetwindow as gw
import pickle

class Lobby:
	def __init__(self, name, coordinates, mapp = []):
		self.name = name
		self.coordinates = coordinates
		self.map = mapp
	
	def set_window(self):
		windows = gw.getAllWindows()
		target_window = [window for window in windows if window.title == self.name]
		if len(target_window) == 1:
			self.window = target_window[0]
		else:
			raise Exception("Window not found or worst: severals!")
	
	def resize(self):
		self.set_window()
		self.window.maximize()
		self.window.resizeTo(self.coordinates[0], self.coordinates[1])
		self.window.moveTo(0,0)

	def execute_map(self):
		self.resize()
		print(self.map)
		for action in self.map:
			print(action[1][0],action[1][1])
			pyautogui.moveTo(action[1][0],action[1][1])
			pyautogui.click()
	
	
	def pickle_self(self):
		try:
			delattr(self, 'window')
		except:
			pass
		with open("PickledObjects/" + self.name + "MAPPED_LOBBY", 'wb') as file:
			pickle.dump(self, file)