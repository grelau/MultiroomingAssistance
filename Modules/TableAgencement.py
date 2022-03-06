import pygetwindow as gw
import pyautogui
import pywinauto
from screeninfo import get_monitors
import pyautogui
import pygetwindow as gw


def organize_playground(event):
	class Monitor:
	    def __init__(self, coords):
	        self.x = coords['x']
	        self.xmax = coords['x_max']
	        self.y = coords['y']
	        self.ymax = coords['y_max']
	        
	        self.x3slice = int((self.xmax - self.x)/3)
	        self.x2slice = int((self.xmax - self.x)/2)
	        self.y2slice = int((self.ymax - self.y)/2)
	        
	        self.sixcoords = [



	            (self.x, self.y),
	            (self.x + self.x3slice, self.y),
	            (self.x, self.y + self.y2slice),
	            (self.x + self.x3slice, self.y + self.y2slice),
	            (self.x + self.x3slice*2, self.y),
	            (self.x + self.x3slice*2, self.y + self.y2slice),

	        ]
	        self.twocoords = [
	            (self.x, self.y),
	            (self.x + self.x2slice, self.y)
	        ]
	        self.six_tables_size = [
	            self
	        ]

	monitors = get_monitors()

	width =  0
	for m in monitors:
	    if m.width_mm > width:
	        width = m.width_mm
	        first_monitor = m

	fmc = [first_monitor.x, first_monitor.y, first_monitor.width, first_monitor.height]
	fmc = {
	    'x': fmc[0],
	    'x_max': fmc[0] + fmc[2],
	    'y': fmc[1],
	    'y_max': fmc[1] + fmc[3]}

	fm = Monitor(fmc)

	try:
	    fmi = monitors.index(first_monitor)
	    second_monitor = monitors[1 - fmi]
	    smc= [second_monitor.x, second_monitor.y, second_monitor.width, second_monitor.height]
	    smc = {
	    'x': smc[0],
	    'x_max': smc[0] + smc[2],
	    'y': smc[1],
	    'y_max': smc[1] + smc[3]}
	    
	    sm = Monitor(smc)

	except:
	    pass

	import random
	wina_keyword = "NL Holdem"
	pmu_keyword = "NLHold'em"
	ps_keyword = "Tournoi"

	keywords = [wina_keyword, pmu_keyword, ps_keyword, "NL Hold'em", "Hold'em No Limit"]

	windows = gw.getAllTitles()

	matched_windows = []
	for window in windows:
	    for keyword in keywords:
	        if keyword in window:
	            matched_windows.append(window)
	            break
	random.shuffle(matched_windows)
	nb_tables = len(matched_windows)

	if nb_tables == 2:
	    coordinates = fm.twocoords
	    for i in range(nb_tables):
	        table = gw.getWindowsWithTitle(matched_windows[i])[0]
	        pywinauto.application.Application(backend="uia").connect(handle=table._hWnd).top_window().set_focus()
	        table.resizeTo(fm.x2slice,fm.y2slice + round(fm.y2slice/3.5)) #ligne douteuse il faudrati resize correctement
	        x,y = coordinates[i]
	        table.moveTo(x,y)
	            
	elif nb_tables > 2 and nb_tables <= 6:
	    coordinates = fm.sixcoords
	    for i in range(nb_tables):
	        table = gw.getWindowsWithTitle(matched_windows[i])[0]
	        pywinauto.application.Application(backend="uia").connect(handle=table._hWnd).top_window().set_focus()
	        table.resizeTo(fm.x3slice,fm.y2slice - round((fm.y2slice/7)))
	        x,y = coordinates[i]
	        table.moveTo(x,y)
	        
	elif nb_tables > 6 and nb_tables <= 8:
	    coordinates = fm.sixcoords + sm.twocoords#[: nb_table-6]
	    for i in range(nb_tables):
	        table = gw.getWindowsWithTitle(matched_windows[i])[0]
	        pywinauto.application.Application(backend="uia").connect(handle=table._hWnd).top_window().set_focus()
	        if i <= 5:
	            table.resizeTo(fm.x3slice,fm.y2slice - round((fm.y2slice/7)))
	        else:
	            table.resizeTo(sm.x2slice, sm.y2slice + round(sm.y2slice/3.5)) #ligne douteuse il faudrati resize correctement
	        x,y = coordinates[i]
	        table.moveTo(x,y)
	        
	elif nb_tables > 8:
	    coordinates = fm.sixcoords + sm.sixcoords
	    for i in range(nb_tables):
	        table = gw.getWindowsWithTitle(matched_windows[i])[0]
	        pywinauto.application.Application(backend="uia").connect(handle=table._hWnd).top_window().set_focus()
	        if i <= 5:
	            table.resizeTo(fm.x3slice,fm.y2slice - round((fm.y2slice/7)))
	        else:
	            table.resizeTo(sm.x3slice,sm.y2slice - round((sm.y2slice/7))) #ligne douteuse il faudrati resize correctement
	        x,y = coordinates[i]
	        table.moveTo(x,y)