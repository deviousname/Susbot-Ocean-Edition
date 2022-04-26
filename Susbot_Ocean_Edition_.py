#susbot

#by deviousname.

#GNU Affero General Public License v3.0
'''Permissions of this strongest copyleft license are conditioned on making available complete source code of licensed works and modifications,
which include larger works using a licensed work, under the same license. Copyright and license notices must be preserved.
Contributors provide an express grant of patent rights. When a modified version is used to provide a service over a network,
the complete source code of the modified version must be made available.'''

import crewmate #username/password goes in crewmate.py
import requests
import os
import keyboard
import socketio
import threading
import math
import random
import time
import urllib.request
import pyautogui
import math
import PIL
import numpy as np
import itertools
from itertools import cycle
from numpy import sqrt 
from PIL import Image, ImageGrab
from ast import literal_eval as make_tuple
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#settings for Chromedriver to not show its errors on Sus Bot:
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument("--disable-webgl")
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(options=options)

#if you want to use FireFox, remove the # from the next line (put # back again to go back to Chrome)
#driver = webdriver.Firefox()
#and download geckodriver.exe from their official page for it:
#https://github.com/mozilla/geckodriver/releases
#and put the unzipped geckodriver.exe into the susbot folder next to chromedriver.exe
#as long as your firefox and geckodriver matches it should work

#python socket.io stuff:
sio = socketio.Client()

#OPTIONS:
reddit = "yes" #yes/no...
# if no then you must manually login to pixelplace
# and then press F9 to connect

#map settings:
board = 7 #this is the map number you want to play on
#note: you will still have to go to that map in your main tab
#after the bot has connected fully

#BOT SPEED SETTINGS:
slow_speed = 0.04 #seconds
default_speed = 0.02 #default
max_speed = 0.016  # DANGER!!! You can get autobanned for going too fast

#--|###############|--# Bot global speed:
speed = default_speed # Set speed here. 
#--|###############|--# Recommend: speed = default_speed

#PAINT RGB VALUES
paintz = ( #here is our list of pixel place colors
        (255,255,255), #the order of them also is the order
        (196,196,196), #of them on pixelplace which makes
        (136,136,136), #referencing them later a breeze
        (85,85,85),    #<<< this one is " paintz[3] " for example
        (34,34,34),    #<<< and this: " paintz.index((34,34,34)) "
        (0,0,0),       #        will equal " 4 " ^^^^^^
        (0,102,0),     #you will need to use both ways to check rgb values
        (34,177,76),   #and send correct color index to pixelplace server
        (2,190,1),     #(if you want to make your own functions that use colors)
        (81,225,25),
        (148,224,68),
        (251,255,91),
        (229,217,0),
        (230,190,12),
        (229,149,0),
        (160,106,66),
        (153,83,13),
        (99,60,31),
        (107,0,0),
        (159,0,0),
        (229,0,0),
        (255,57,4),
        (187,79,0),
        (255,117,95),
        (255,196,159),
        (255,223,204),
        (255,167,209),
        (207,110,228),
        (236,8,236),
        (130,0,128),
        (81,0,255),
        (2,7,99),
        (0,0,234),
        (4,75,255),
        (101,131,207),
        (54,186,255),
        (0,131,199),
        (0,211,221),
        (69,255,200)
        )

class Sus_Bot(): #---------Sus_Bot main class-----------
    def __init__ (self, username, password): #lets setup the __init__ and load some future needed variables and fully load the bot:
        print('̴ı̴̴̡̡̡ ̡͌l̡̡̡ ̡͌l̡*̡̡ ̴̡ı̴̴̡ ̡̡͡|̲̲̲͡͡͡ ̲▫̲͡ ̲̲̲͡͡π̲̲͡͡ ̲̲͡▫̲̲͡͡ ̲|̡̡̡ ̡ ̴̡ı̴̡̡ ̡͌l̡̡̡̡.')
        print('Welcome to SusBot')
        print('~Ꭿ~ꇺ~')
        print('Please Stand By...')
        self.z = 1 #facing direction of ᎯmogsuS
        print("Initiliazing variables...")
        self.txty, self.bxby = None, None #For tree zone thing, and these equal None... for now...
        self.x, self.y = 0, 0 #player coordiantes
        self.lastx, self.lasty = self.x, self.y 
        self.colorfilter = [None, None, None, None, None, None, None, None, None, None]
        self.logos = True
        self.zone_commands = False
        self.count = 0
        self.numbers = 0
        self.exception = 0
        self.color = 30
        self.start = None
        self.first = True
        self.get_7()#map
        self.manualmsg = False
        self.ate_cookies = False
        self.open_treasure = None
        print('Variables initiliazed.')
        if reddit == "yes":
            print('Logging into Reddit. Stand by.')
            self.login()#login
            print('Getting Cookies...')
            self.auth_data()#cookies
            print('Finalizing...')
            self.visibility_state() #this checks the current tab you are on, and correctly sets the xpath stuff
        self.hotkeys()#activate keybinds
        print('~~~~~ꇺ~~Ꭿ~~ඞ~~~~~')
        print('')
        print('SusBot is ready.')
        print('----CONTROLS----')
        print('')
        print('d: Mongus')
        print('e: Tree')
        print('w: Water')        
        print('')
        print('Shift+E: Mark top-left region.')
        print('Shift+D: Mark bottom-right region.')
        print('')
        print('Shift R: Forest')
        print('Shift W: Wave source - w again - to relocate Wave source')
        print('Shift S: Ocean defense zone on equipped colors')
        print('Shift A: Nature defense zone on equipped colors')
        print("q: Stop.")
        print('')
        print('Shift X: Toggle guild war logos on or off.')
        print('')
        print('1 through 9 and 0 keys:')
        print('--- Will equip your selected color to the colorfilter list.')
        print('')
        print("Tilde ` or ~ will remove all equipped colors from the colorfilter list.")
        print("--- It's to the left of 1, above TAB")
        print('')
        print('ꇺᎯඞ')
        print('')
        print('~~~~~~~~Ꭿ~~~~~~~~')
        self.connection() #start pixelplace socket connection      
            
    #hotkey binds:
    def hotkeys(self):
        keyboard.on_press(self.onkeypress)#1-9 buttons equip currently selected colors
        keyboard.add_hotkey("e", lambda: self.tree('single')) #tree
        keyboard.add_hotkey("d", lambda: self.amogus("single", None, "na")) #sus
        keyboard.add_hotkey('shift+e', lambda: self.zone('top left')) #mark top left corner of zone to bot for forest and tv
        keyboard.add_hotkey('shift+d', lambda: self.zone('bottom right')) #mark bottom right corner of zone to bot for forest and tv        
        keyboard.add_hotkey('shift+x', lambda: self.toggle_logos()) #toggle guild war logos on/off
        keyboard.add_hotkey('shift+r', lambda: self.forest())#forest of trees in zone area on equipped colors
        keyboard.add_hotkey('w', lambda: self.wave_edit()) #splashes water around
        keyboard.add_hotkey('shift+w', lambda: self.ocean()) #now we are getting serious
        keyboard.add_hotkey('shift+s', lambda: self.surf_zone('ocean')) #oh no!
        keyboard.add_hotkey('shift+a', lambda: self.surf_zone('nature')) #is it magic?
        print('Hotkeys on.')
        
    def tree(self, kind): #this will draw a randomly colored tree, trying to optimize speed
        try:
            self.start = time.time()
            tree_order = ()
            if kind == 'single':
                self.get_coordinate()
                x, y = self.x, self.y
            else:
                x, y = random.randrange(self.txty[0],self.bxby[0]),random.randrange(self.txty[1],self.bxby[1])
                self.x, self.y = x, y
            trunk=next(trunks_cycle)
            for a in range(4):
                tree_order+=([x,y-a,trunk,1],) 
            leaf=next(leaves_cycle)
            y -= a
            for b in range(3):
                tree_order+=([x+b-1,y,leaf,1],)
            y -= 1
            for c in range(3):
                tree_order+=([x+c-1,y,leaf,1],)
            y -= 1
            tree_order+=([x,y,leaf,1],)
            if kind == 'single':
                self.count+=1
                self.numbers += 1
                for Y in tree_order:
                    sio.emit("p", Y)
                    time.sleep(speed - (self.start - time.time()))
                    self.start = time.time()
            else:
                if self.cache[self.x, self.y] not in trees_and_oceans + [(204,204,204)] + self.colorfilter:
                    self.count+=1
                    for Y in tree_order:
                        sio.emit("p", Y)
                        time.sleep(speed - (self.start - time.time()))
                        self.start = time.time()
        except:
            print('Timber!')
            pass
        
    def forest(self): #draws a forest
        try:
            print('Planting forest. Hold q to end task.')
            while True:
                self.tree('forest')
                if keyboard.is_pressed('q'):
                    if self.primeCheck(self.count) == "Prime":
                        print(f'Planted {self.count} trees so far...')
                        print(f"Tree {self.count} was prime.")
                    else:
                        print(f'Planted {self.count} trees so far.')
                    return
        except:
            print('Need a forest permit first.')
            print('Oh, you have one?')
            print('**You hand the officer some paperwork**')
            default_square = 16
            try:
                self.get_coordinate()
            except:
                print('The arborist was lost at sea.')
            self.txty, self.bxby = (self.x-default_square, self.y-default_square), (self.x+default_square, self.y+default_square)
            print(f'{self.txty}, {self.bxby} = ({self.x}-{default_square}, {self.y}-{default_square}), ({self.x}+{default_square}, {self.y}+{default_square})')
            self.exception += 1
            print(self.exception)
            self.forest()
        
    def primeCheck(self, n):
        # 0, 1, even numbers greater than 2 are NOT PRIME
        if n==1 or n==0 or (n % 2 == 0 and n > 2):
            return "Not prime"
        else:
            # Not prime if divisable by another number less
            # or equal to the square root of itself.
            # n**(1/2) returns square root of n
            for i in range(3, int(n**(1/2))+1, 2):
                if n%i == 0:
                    return "Not prime"
            return "Prime"
        
    def amogus(self, loc1, loc2, col): #lil sussy baka, or crewmate, who is to tell?
        try:
            self.start = time.time()
            #todo: add more directional control, currently at left and right facing, need diagonals and up/down
            self.getcurcolor()
            if loc1 != "single":
                X, Y = loc1, loc2
            else:
                self.get_coordinate()
                X, Y = self.x, self.y            
            if X >= self.lastx: #right facing
                for n in range(2):
                    sio.emit("p",[X+(n*self.z),Y,37,1])
                    time.sleep(speed - (self.start - time.time())) 
                    self.start = time.time() 
                x, y = X + self.z, Y + 2        
                body=[(x,y),(x,y-1),(x-(self.z*1),y-1),(x-(self.z*2),y),(x-(self.z*2),y-1),(x-(self.z*3),y-1),
                      (x-(self.z*3),y-2),(x-(self.z*2),y-2),(x-(self.z*2),y-3),(x-(self.z*1),y-3),(x,y-3)]
                c = cy_cols(paintz.index(self.curcol[0]))
            else: #left facing
                for n in range(2):
                    sio.emit("p",[X-(n*self.z),Y,38,1])
                    time.sleep(speed)
                x, y = X-1, Y + 2        
                body=[(x,y),(x,y-1),(x+(self.z*1),y-1),(x+(self.z*2),y),(x+(self.z*2),y-1),(x+(self.z*3),y-1),
                  (x+(self.z*3),y-2),(x+(self.z*2),y-2),(x+(self.z*2),y-3),(x+(self.z*1),y-3),(x,y-3)]
                c = cy_cols(paintz.index(self.curcol[0]))             
            for n in body:
                sio.emit("p",[n[0],n[1],c,1])
                time.sleep(speed - (self.start - time.time()))
                self.start = time.time() 
            self.lastx, self.lasty = X, Y
        except:
            print('*vented*')
            pass
        
    def wave_edit(self): #water brush -don't change, works good-
        self.start=time.time()
        self.x,self.y=self.x+(random.random()*5), self.y-(random.random()*5)
        if self.cache[self.x, self.y] not in self.colorfilter + [(204,204,204)]:
            sio.emit("p",[self.x, self.y, self.color,1])
            self.get_coordinate()
            nap=speed-(time.time()-self.start)
            try:
                time.sleep(nap)
            except:
                self.color = oceaneer(self.color)
        else:
            self.color = cy_cols(self.color)

    def ocean(self): #lake and river generator -edit- ############################
        print('-W~A-V~E~R-I~D-E~R-')
        self.color = 38        
        def r_task(xy):
            r = random.random()
            r2 = random.random()            
            if r < .5:
                self.y -= 1
                if r2 < .5:
                    self.x -= 1
                    if r + r2 > .5:
                        if r > r2:
                            self.color = oceaneer(self.color)
                else:
                    self.x += 1
            else:
                self.y += 1
                if r2 > .5:
                    self.x += 1
                    if r + r2 < .5:
                        if r < r2:
                            self.color = cy_cols(self.color) 
                else:
                    self.x -= 1
                    self.x, self.y = xy
            if self.cache[self.x, self.y] not in self.colorfilter + [(204,204,204)] + trees_and_oceans:
                sio.emit("p",[self.x, self.y, self.color, 1])
                try:
                    time.sleep(speed - (time.time() - self.start))
                except:
                    self.x, self.y = xy
                    pass                
        while True:
            if keyboard.is_pressed('w'):
                self.get_coordinate()
                xy = self.x, self.y 
            if keyboard.is_pressed('q'):
                print('~W-A~V~E-R-I-D~E~R~')
                return
            self.start = time.time()
            r_task(xy)
            
    def surf_zone(self, loc): #lake and river generator
        try:
            print('The surf breaks.')
            default_square = 1 #incase you dont have a zone in mind
            self.get_coordinate()
            xy = self.x, self.y
            self.getcurcolor()
            self.color = paintz.index(self.curcol[0])
            while True:
                if keyboard.is_pressed('q'):
                    print('The surf recedes.')
                    return
                if random.random() > 0.5:
                    if random.random() > 0.5:
                        self.x += 1
                    else:
                        self.x -= 1
                else:
                    if random.random() > 0.5:
                        self.y += 1
                    else:
                        self.y -= 1
                if self.cache[self.x, self.y] in self.colorfilter:
                    sio.emit("p",[self.x, self.y, self.color, 1])
                    if loc == 'ocean':
                        self.color = oceaneer(self.color)
                    elif loc == 'nature':
                        self.color = cy_cols(self.color)
                    try:
                        if self.x < self.txty[0] or self.y < self.txty[1] or self.x > self.bxby[0] or self.y > self.bxby[1]:
                            self.x, self.y = xy
                    except:
                        self.txty, self.bxby = (self.x-default_square, self.y-default_square), (self.x+default_square, self.y+default_square)
                    try:
                        time.sleep(default_speed - (time.time() - self.start))
                    except:
                        self.start = time.time()
                    self.start = time.time()
        except:
            pass
        
    def zone(self, hotkey): #zone constructor
        try:
            self.get_coordinate()
            if hotkey == 'top left': #top left
                self.txty = self.x, self.y, (pyautogui.position())
                print (f'Top-left marked: {self.txty}')
                try:
                    if self.bxby[0] > self.txty[0] and self.bxby[1] > self.txty[1]:
                        print ('Zone commands ready.')
                        self.zone_commands = True
                except:
                    pass
            if hotkey == 'bottom right': #bottom right
                self.bxby = self.x + 1, self.y + 1, (pyautogui.position())
                print (f'Bottom-right marked: {self.bxby}')
                try:
                    if self.bxby[0] > self.txty[0] and self.bxby[1] > self.txty[1]:
                        print ('Zone commands ready.')
                        self.zone_commands = True
                except:
                    pass
        except:
            pass
        
    def get_coordinate(self):#check the coordinate of where your cursor is on the selenium pixelplace site
        try:
            self.x, self.y = make_tuple(driver.find_element(By.XPATH,'/html/body/div[3]/div[4]').text)
        except:
             pass
        
    def onkeypress(self, event): #whatever 1-9 key you press will allow you to equip a color for filter
        if event.name == '1':
            self.getcurcolorhotkey(1)
        elif event.name == '2':
            self.getcurcolorhotkey(2)
        elif event.name == '3':
            self.getcurcolorhotkey(3)
        elif event.name == '4':
            self.getcurcolorhotkey(4)
        elif event.name == '5':
            self.getcurcolorhotkey(5)
        elif event.name == '6':
            self.getcurcolorhotkey(6)
        elif event.name == '7':
            self.getcurcolorhotkey(7)
        elif event.name == '8':
            self.getcurcolorhotkey(8)
        elif event.name == '9':
            self.getcurcolorhotkey(9)
        elif event.name == '0':
            self.getcurcolorhotkey(0)
        elif event.name == '`':
            self.removefilters()
            
    def getcurcolor(self): #gets the currently equipped color as a tuple
        try:
            self.visibility_state()
            a = self.curcol.find('(')
            b = self.curcol.find(')');b+=1
            self.curcol = self.curcol[a:b]
            self.curcol = [make_tuple(self.curcol)]
        except:
            pass
        
    def getcurcolorhotkey(self, col): #equips color to 1-9 slots
        try:
            self.visibility_state()
            a = self.curcol.find('(')
            b = self.curcol.find(')');b+=1
            curcol = self.curcol[a:b]
            self.curcol = [make_tuple(curcol)]
            self.colorfilter[col-1] = self.curcol[0]
            print(f'Equipped {self.curcol[0]} to slot {col}')
            return
        except:
            pass
    
    def removefilters(self): #removes equipped colors on the 1-9 and 0 slots
        self.colorfilter[0:] = None, None, None, None, None, None, None, None, None, None
        print("Filters dequipped.")
        
    def visibility_state(self): #ensures the current tab is correctly loaded for xpath css code stuff
        try:
            vis = driver.execute_script("return document.visibilityState") == "visible"
        except:
            driver.switch_to.window(driver.window_handles[0])
            vis = driver.execute_script("return document.visibilityState") == "visible"
        if vis == False:
            p = driver.current_window_handle
            chwd = driver.window_handles
            for w in chwd:
                if(w!=p):
                    driver.switch_to.window(w)
            self.curcol = str(driver.find_element(By.XPATH,'/html/body/div[3]/div[2]').get_attribute("style"))
        else:
            self.curcol = str(driver.find_element(By.XPATH,'/html/body/div[3]/div[2]').get_attribute("style"))
            
    def toggle_logos(self): #toggles guild war logos on and off
        self.visibility_state()
        if self.logos == True:
            for lg in range(10):
                try:
                    driver.execute_script("arguments[0].style.display = 'none';",driver.find_element(By.XPATH,f'//*[@id="areas"]/div[{lg}]'))
                    driver.execute_script("arguments[0].style.display = 'none';",driver.find_element(By.XPATH,f'/html/body/div[3]/div[1]/div[2]/div/a[{lg}]'))
                except:
                    pass
            self.logos = False
        else:
            for lg in range(10):
                try:
                    driver.execute_script("arguments[0].style.display = 'block';",driver.find_element(By.XPATH,f'//*[@id="areas"]/div[{lg}]'))
                    driver.execute_script("arguments[0].style.display = 'inline';",driver.find_element(By.XPATH,f'/html/body/div[3]/div[1]/div[2]/div/a[{lg}]'))
                except:
                    pass
            self.logos = True
        time.sleep(.5)
        
    def get_7(self):
        nummy = random.randint(9999,99999)
        url = f'https://pixelplace.io/canvas/{board}.png?t={nummy}'
        page = requests.get(url)
        f_name = f'{board}.png'
        with open(f_name, 'wb') as f:
            f.write(page.content)
        self.image = PIL.Image.open(f'{board}.png').convert('RGB')
        self.cache = self.image.load()

    def manual(self):
        driver.get(f"https://pixelplace.io/{board}")
        print("After you login in manually, press f8.")

    def manualf8(self):
        self.visibility_state()
        self.auth_data()
        self.ate_cookies = True
        keyboard.remove_hotkey('f8')
        self.connection()
        
    def connection(self):
        sio.connect('https://pixelplace.io', transports=['websocket'])        
        @sio.event
        def connect():
            sio.emit("init",{"authKey":f"{self.authkey}","authToken":f"{self.authtoken}","authId":f"{self.authid}","boardId":board})
            threading.Timer(15, connect).start()
            
        @sio.on("p")
        def update_pixels(p: tuple):
            for i in p:
                try:
                    self.cache[i[0], i[1]] = paintz[i[2]]
                except:
                    pass
                
    def login(self):
        driver.get("https://pixelplace.io/api/sso.php?type=2&action=login")
        driver.find_element(By.ID,'loginUsername').send_keys(crewmate.username)
        driver.find_element(By.ID,'loginPassword').send_keys(crewmate.password)
        driver.find_elements(By.XPATH,'/html/body/div/main/div[1]/div/div[2]/form/fieldset')[4].click()
        print('Reddit connection successful.')
        print(f'Studying chart #{board}.')
        treasure = (random.randint(0, self.image.size[0]),random.randint(0, self.image.size[1]))
        self.open_treasure = self.cache[treasure[0],treasure[1]]
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH,'/html/body/div[3]/div/div[2]/form/div/input'))).click()
        print(f'Possible treasure located: x:{treasure[0]}, y:{treasure[1]}')
        print("Sailing...")
        driver.get(f"https://pixelplace.io/{board}")
        if self.open_treasure == (204,204,204):
            print('.,;,.but nothing was found.,:,.,.')
            print('~S~u~m~m~e~r~~O~c~e~a~n~~D~a~y~s~')
        else:
            print(f'You found {self.open_treasure}...!')
            print('Hmmm, I wonder what color that is?')
            print('Maybe I can name it something?')
            print(f'Oh, and the treasure also contained this old piece of parchment paper.')
            print(f'There appears to be some writing on it...')
            print('You translate the parchment:')
            print('')
            print(f'{random.choice(tips)}')
            print("|̲̲̲͡͡͡ ̲▫̲͡ ~Ꭿ~ꇺ~̲̲̲͡͡π̲̲͡͡ ̲̲͡▫̲̲͡͡ ̲|")
            print('')
        return

    def auth_data(self):
        self.authkey = driver.get_cookie("authKey").get('value')
        self.authtoken = driver.get_cookie("authToken").get('value')
        self.authid = driver.get_cookie("authId").get('value')
        print('got cookies! yum!')
        self.ate_cookies = True
    #end of class function
        
# global variables
trees_and_oceans = [(0,102,0),(34,177,76),(2,190,1),(81,225,25),(148,224,68),
		    (229,149,0),(160,106,66),(153,83,13),(99,60,31),(187,79,0),
                    (81,0,255),(2,7,99),(0,0,234),(4,75,255),(101,131,207),
                    (54,186,255),(0,131,199),(0,211,221),(69,255,200)]

#global list
leaves = [paintz.index(k) for k in paintz if paintz.index(k) in range(6,10+1)] #the +1 ensures the end of range is accounted for
leaves_cycle = cycle(leaves)
trunks = [paintz.index(k) for k in paintz if paintz.index(k) in range(15,17+1)] + [22]
trunks_cycle = cycle(trunks)

# global functions        
def oceaneer(a): #good for Oceans
    if random.random() > .5:
        a += 1        
    else:
        a -= 1
    if a < 30:
        a = 38
    if a > 38:
        a = 30
    return a

def cy_cols(a): #50/50 chance to go forward or backward
    if random.random() > .5: 
        a += 1
        if a == 6:
            a = 4
        elif a > 38:
            a = 0
    else:
        a -= 1
        if a == 5:
            a = 7
        elif a == 38:
            a = 1    
    if a > 38:
        a = 0
    elif a < 0:
        a = 37
    if a > 38:
        a = 0
    return a #"return" "a" means that you can say the function itself is equal to something, for example "variable = cy_cols(1)" has a chance to equal 0 or 2
    #more similar global functions like cy_cols toward bottom of code

#tips
tips = ["Equip your  color with the 1 through 9 keys. Pressing 0 will remove them. These can modify other abilities.",
        "Successfully creating a region with u and y will allow you to grow trees there with Shift R, except for on browns, blues, greens, and equipped colors.",
        "Pressing Shift W will unleash a Water front at your mouse location. Pressing w again will move it to your new location. q will stop the current. ",
        "If you want to paint underneath the guild war logos, toggle them off with Shift X.",
        '"The Copy and Paste feature is coming soon." TM',
        'If you try to draw manually while planting a forest or other tasks, you may get speed debuffed, be careful. Pressing q will end any tasks.']

#start the program
goto = Sus_Bot(crewmate.username, crewmate.password) #start an instance of the Sus_Bot class as 'goto'
