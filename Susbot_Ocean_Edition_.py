#susbot
#open source software for Python 3.8.10

############################
# Todo:
# Add universal copy/paste
# Add improved TV function
# Add more direction control for mongus
# Improve effeciency of the water brush *there also is another water brush now, press s after you use the bucket fill to change to bucket ocean fill, (set each blue color to your colorfilter before hand and you will have space for 1 more color, which the ocean won't cross.
# Add restoration tool again
############################

#map settings:
chart = 7 #this is the map number you want to play on

#BOT speed SETTINGS:
slow_speed = 0.04 # seconds
default_speed = 0.02 # default
max_speed = 0.016  # DANGER!!! *You can get autobanned for going too fast.

#--|###############|--# Bot global speed:
speed = max_speed # Set speed here
#--|###############|--# Recommend: speed = default_speed

#Hotkeys you can rebind...
#Make sure they aren't already being used!
stop_key = 'Ctrl+Q' #hold this button to stop some of the many functions that auto-paint for you, such as the forest or ocean brush or bucket fill
foresty_hotkey = 'Shift+R' # this one is for planting a forest inside your zone,
#I plan to add more variables for the different fuctions in this area once I get to it.
#But for now the rest of the hotkey rebinds are down below in the function, 'def hotkeys(self):'

unit_measurement = 'mile' #used for RP dialog, you can change this to anything and it will call a pixels length that
#such as 'pixel' or 'kilometer' or 'icecream cakes' it doesn't matter, as long as it is a string or something, hmm maybe int() would work there too?

#(more global variables toward very bottom of script)
# Main class "Sus_Bot":
class Sus_Bot(): #---------Sus_Bot---------
    def __init__ (self): #lets setup the __init__ and load some future needed variables and fully load the bot:
        print('|̲̲̲͡͡͡ ̲▫̲͡ ̲̲̲͡͡π̲̲͡͡ ̲̲͡▫̲̲͡͡ ̲|')
        print('Welcome to SusBot')
        print('~Ꭿ~ꇺ~')
        self.z = 1 #facing direction of ᎯmogsuS
        print("Building ship...")
        self.work_order = ()
        self.txty, self.bxby = None, None #For tree zone thing, and these equal None... for now...
        self.x, self.y = 0, 0 #player coordiantes
        self.lastx, self.lasty = self.x, self.y
        self.colorfilter = [None, None, None, None, None, None, None, None, None, None]
        self.logos = True
        self.zone_commands = False
        self.forestry_permit = False
        self.ocean_activated = False
        self.count = 0
        self.exception = 0
        self.color = random.randint(0, 39)
        self.start = None #this is needed for the timing system that decides how long to sleep between each pixel placement
        self.get_7()#load the selected map into your computers cache
        self.authid= None #this sets the cookie variable as empty so that while its empty we can wait for login to be complete
        print('Ship construction complete.')
        driver.get(f"https://pixelplace.io/{chart}")
        #driver.maximize_window() #not sure if we need this, uncomment if you want it to auto full screen susbot, lazy dirt sussy
        print(f'Studying sea charts.')
        self.treasure = (random.randint(0, self.image.size[0]),random.randint(0, self.image.size[1]))
        print(f'Possible treasure located: x:{self.treasure[0]}, y:{self.treasure[1]}')
        print("Setting course.")
        #driver.set_window_position(int(pyautogui.size()[0]/4), 0, windowHandle='current')
        while self.authid == None: #while cookies empty, do this stuff:
            try:
                self.auth_data() #try to get cookies
                print('got cookies, yum!')
                self.visibility_state()
                print('Land ho!')
                if chart != 7: #checks if you are playing on default map
                    driver.get(f"https://pixelplace.io/{chart}")
                    print(f'Arrived at: Island #{chart}')
                else:
                    print(f'Found island...')
            except: #if we dont have the cookies the above code excepts into this:
                print('Another day passes...') 
                time.sleep(7) #sleep then send back to start of cookie check loop
                pass 
        print('Searching for treasure...') #got the cookies, now we can look for booty
        treasure = self.cache[self.treasure[0],self.treasure[1]] #treasure chest yarr ye matey
        if treasure == (204,204,204): #if its that border/ocean color, then no treasure
            print('.,;,.but nothing was found.,:,.,.')
            print('~S~u~m~m~e~r~~O~c~e~a~n~~D~a~y~s~')
            time.sleep(5)
        else: #otherwise say what the color of that pixel is
            print(f'You found {treasure}...!')
            print('Hmmm, I wonder what that is?')
            print('Maybe I can name it something?')
            print(f'Oh, and the treasure also contained this old piece of parchment paper.')
            print(f'There appears to be some writing on it...')
            print('You translate the parchment:')
            print('')
            print(f'{random.choice(tips)}') #print a random tip (the tip list is at the bottom of the script)
            print('')
            print("|̲̲̲͡͡͡ ̲▫̲͡ ~Ꭿ~ꇺ~̲̲̲͡͡π̲̲͡͡ ̲̲͡▫̲̲͡͡ ̲|")
            time.sleep(10) #take a long enough break that they can read the random tip
        self.hotkeys()#activate keybinds
        print('~~~~~ꇺ~~Ꭿ~~ඞ~~~~~')
        print('')
        print('SusBot is ready.')
        print('----CONTROLS----')
        print('')
        print('d: Mongus')
        print('w: Plant Tree')        
        print('')
        print("Hold 'v' and drag your mouse to create a zone")
        print("Hold 'a' and drag your mouse to create a line")
        print("Hold 'q' and drag your mouse to create a circle outline")
        print("Press 'shift+q' to fill in an area with your current color.")
        print('')
        print(f"To stop any of the following Shift commands press and hold: '{stop_key}'")
        print(f'{foresty_hotkey}: Forest')
        print('Shift S: Ocean brush')
        print('Shift A: Nature brush')
        print('Shift E: Selected color brush')
        print('')
        print('')
        print('Shift X: Toggle Guild War Logos on or off.')
        print('')
        print('1 through 9 and 0 keys:')
        print('--- Will equip your selected color. ---')
        print('')
        print("Tilde ` or ~ will remove all equipped colors.")
        print("--- It's to the left of 1, above TAB ---")
        print('Ꭿ')
        print(f"Your {stop_key} is your stop key and can be rebound in the code.")
        print(f"It will stop the Ocean, Nature, and Color brushes, the forest, and the paster functions.\nAlong with circles, lines, bucket fill and basically anything that paints for you.")
        print('')
        print('ꇺᎯඞ')
        print('')
        print('~~~~~~~~Ꭿ~~~~~~~~')
        self.connection() #start pixelplace socket connection
        #init complete
        # "Fun"ction Time
        # Ꭿ+ඞ=ꇺ
        
    #First class function after init is the ---> HOTKEYS <--- section, you can change them here easily...
        """
        1. Just change the thing inside the first set of quiotes, for example: "f9"
        2... something that makes sense for you like "Ctrl+Shift+Alt+X+B+1" if you want.
        3. Or just something simple like "x" if you want it easy.
        4. The downside to that is that typing in chat will accidently activate some of the tools.
        5. TODO: Add chat selection detection to temporarily disable the hotkeys while typing.
        """
	
	# here they are, experiment with what works:
    #hotkey binds:
    def hotkeys(self):
        keyboard.on_press(self.onkeypress)#1-9 buttons equip currently selected colors
        keyboard.add_hotkey("w", lambda: self.forest('single')) #single tree
        keyboard.add_hotkey("d", lambda: self.amogus("single", None, "na")) #sus
        keyboard.add_hotkey('v', lambda: self.zone()) #drag v to size zone
        keyboard.add_hotkey('shift+x', lambda: self.toggle_logos()) #toggle guild war logos on/off
        keyboard.add_hotkey(foresty_hotkey, lambda: self.forest('forest'))#whole forest
        keyboard.add_hotkey('shift+s', lambda: self.surf_zone('ocean'))
        keyboard.add_hotkey('shift+a', lambda: self.surf_zone('nature'))
        keyboard.add_hotkey('shift+e', lambda: self.surf_zone('color'))
        keyboard.add_hotkey('shift+v', lambda: self.copypaste('copy'))
        keyboard.add_hotkey('shift+b', lambda: self.copypaste('paste'))
        keyboard.add_hotkey('shift+]', lambda: self.draw_bezier_line())
        keyboard.add_hotkey('ctrl+z', lambda: self.draw_ellipse(self.get_color_index(), 'single'))
        keyboard.add_hotkey('shift+z', lambda: self.circle_solid(self.get_color_index(), 8, 'single'))
        keyboard.add_hotkey('alt+z', lambda: self.circle_solid(self.get_color_index(), 8, 'loop'))
        keyboard.add_hotkey("q", lambda: self.circle_outline()) #drag q to size circle
        keyboard.add_hotkey("a", lambda: self.line()) #drag a to draw line
        keyboard.add_hotkey("shift+insert", lambda: self.change_speed('decrease'))
        keyboard.add_hotkey("shift+del", lambda: self.change_speed('increase'))
        keyboard.add_hotkey("shift+q", lambda: self.fill_tool())
        keyboard.add_hotkey("f9", lambda: self.barnsley_fern())
        print('Hotkeys on.')    
	
	#now onto some of the functions that the hotkeys (and other parts of the code) will be using:
	
    #this function changes your speed either +0.001 or -0.001 and then cuts of the remaining weight
    def change_speed(self, opt): #works great
        global speed
        if opt == 'decrease':
            speed += 0.001
            speed = float('%.3f'%speed)
            print(speed)
        elif opt == 'increase':
            speed -= 0.001
            speed = float('%.3f'%speed)
            print(speed)
        if speed < 0.01:
            print(f"Going too fast now, defaulting to {default_speed} to prevent perma ban.")
            speed = default_speed

    # can return currently equipped color as int() in 0 to 38 range, you can use this in place of int when sending color to pixelplace
    def get_color_index(self): #TODO: should combine this with self.getcurcolor() into single function
        self.getcurcolor()
        return paintz.index(self.curcol[0])

    #fills an area with your selected color which ends when it fills
    # all areas within selected color + colorfilters + ocean/border color boundary
    def fill_tool(self): #works great
        self.start = time.time()
        self.get_coordinate()
        color = self.get_color_index()
        fill_list = []
        fill_list.append([self.x, self.y])
        print('Filling.')
        self.start = time.time()

        #self.oceaneer() #returns self.color as a random blue color
        
        while len(fill_list) > 0:
            if keyboard.is_pressed(stop_key):
                break
            if keyboard.is_pressed('s'): #this nested if statement switches the ocean brush on/off during fill use
                if self.ocean_activated == False:             
                    self.ocean_activated = True
                    print('Ocean mode...')
                else:
                    self.ocean_activated = False
                    print('Color mode...')
                time.sleep(.25)
            if (r := random.random()) < .042:
                random.shuffle(fill_list)
            #elif r < .01:
            #    fill_list.reverse()
            x, y = fill_list.pop()
            if (col:=self.cache[x, y]) not in paintz or col in self.colorfilter:
                pass
            elif paintz.index(col) == color:
                pass
            else: #print( type(x := f"Ꭿ+ඞ+ꇺ equals: {int((Ꭿ:=.33)+(ඞ:=.34)+(ꇺ:=.31))}"),x,Ꭿ,ඞ,ꇺ, "should equal 0.98 but somehow thinks its zero now that's sus")
                sio.emit('p',[x, y, (color := self.oceaneer()) if self.ocean_activated == True else (color := self.get_color_index()), 1])
                fill_list.append([x+1, y])
                fill_list.append([x-1, y])
                fill_list.append([x, y+1])
                fill_list.append([x, y-1])
                time.sleep(speed - (self.start - time.time()))
                self.start = time.time()
        print('Done filling.')
    
    def draw_bezier_line(self): #needs intuitive control improvements
        try:
            self.get_coordinate()
            start = [self.txty[0], self.txty[1]]
            end = [self.bxby[0], self.bxby[1]]
            control = [self.x, self.y]
            points = []
            resolution = ((self.bxby[1] - self.txty[1]) + (self.bxby[0] - self.txty[0]) // 2)
            resolution += ((abs(self.x - self.txty[0]) + abs(self.y - self.txty[1])) // 2)
            for i in range(resolution):
                t = i / resolution
                x = (1-t)**2 * start[0] + 2 * t * (1-t) * control[0] + t**2 * end[0]
                y = (1-t)**2 * start[1] + 2 * t * (1-t) * control[1] + t**2 * end[1]
                points.append([int(x), int(y)])      
            for i in points:
                sio.emit('p',[i[0], i[1], self.get_color_index(), 1])
                time.sleep(speed)
        except:
            pass
        
    def line(self): #works great
        self.get_coordinate()
        x1, y1 = self.x, self.y
        while True: #press and hold q and drag mouse and release q to set circle size intuitively
            if not keyboard.is_pressed('a'):
                self.get_coordinate()
                x2, y2 = self.x, self.y
                break
        dx = x2 - x1
        dy = y2 - y1
        if abs(dx) > abs(dy):
            step = abs(dx)
        else:
            step = abs(dy)
        x_inc = dx / (step if step != 0 else 1)
        y_inc = dy / (step if step != 0 else 1)
        self.start = time.time()
        for i in range(step+1):
            if keyboard.is_pressed(stop_key):
                break
            if self.cache[int(x1), int(y1)] not in [(204,204,204)] + self.colorfilter + [paintz[self.get_color_index()]]:
                sio.emit('p',[int(x1), int(y1), self.get_color_index(), 1])
                time.sleep(speed - (self.start - time.time()))
                self.start = time.time()
            x1 += x_inc
            y1 += y_inc
        print(f"Created {step+1} {unit_measurement} long line.")
            
    def draw_ellipse(self, color, option): #needs intuitive control improvements
        try:
            rad_x = (self.bxby[0]-self.txty[0]) // 2
            rad_y = (self.bxby[1]-self.txty[1]) // 2
            self.get_coordinate()
            if option == 'loop':
                print('loop')
                while True:
                    if keyboard.is_pressed(stop_key):
                        break
                    ellipse_list = []
                    for x in range(self.x - rad_x, self.x + rad_x):
                        for y in range(self.y - rad_y, self.y + rad_y):
                            if (x - self.x) ** 2 / rad_x ** 2 + (y - self.y) ** 2 / rad_y ** 2 <= 1:
                                ellipse_list+=[[x, y],]
                    ellipse_list.sort(key=lambda x: (x[0] - 100) ** 2 + (x[1] - 100) ** 2) #skewed print            
                    for i in ellipse_list:
                        try:
                            clr = paintz.index(self.cache[i[0], i[1]])
                        except:
                            clr = color
                        if clr != color:
                            sio.emit('p',[i[0], i[1], abs(self.get_color_index()-clr), 1])
                            time.sleep(speed)
                        if keyboard.is_pressed(stop_key):
                            break
            else:
                ellipse_list = []
                for x in range(self.x - rad_x, self.x + rad_x):
                    for y in range(self.y - rad_y, self.y + rad_y):
                        if (x - self.x) ** 2 / rad_x ** 2 + (y - self.y) ** 2 / rad_y ** 2 <= 1:
                            ellipse_list+=[[x, y],]
                ellipse_list.sort(key=lambda x: (x[0] - 100) ** 2 + (x[1] - 100) ** 2) #skewed print           
                for i in ellipse_list:
                    try:
                        clr = paintz.index(self.cache[i[0], i[1]])
                    except:
                        clr = color
                    if clr != color:
                        sio.emit('p',[i[0], i[1], abs(self.get_color_index()-clr), 1])
                        time.sleep(speed)
                    if keyboard.is_pressed(stop_key):
                        break
        except:
            pass
            
    def circle_outline(self): #works great
        self.get_coordinate()
        x2, y2 = self.x, self.y
        while True: #press and hold q and drag mouse and release q to set circle size intuitively
            if not keyboard.is_pressed('q'):
                self.get_coordinate()
                x1, y1 = self.x, self.y
                break
        r = int((((x2-x1)**2 + (y2-y1)**2))**0.5) #radius of circle from center to corner point of square drawn around it (hypotenuse)
        x = r-1 #starts one pixel before the radius so it doesn't draw a line on the bottom and right side of the circle
        y = 0
        dx = 1
        dy = 1
        err = dx - (r << 1)
        self.getcurcolor()
        while x >= y:
            if keyboard.is_pressed(stop_key):
                break
            sio.emit('p',[x1 + x, y1 + y, self.get_color_index(), 1])
            time.sleep(speed)
            sio.emit('p',[x1 + y, y1 + x, self.get_color_index(), 1])
            time.sleep(speed)
            sio.emit('p',[x1 - y, y1 + x, self.get_color_index(), 1])
            time.sleep(speed)
            sio.emit('p',[x1 - x, y1 + y, self.get_color_index(), 1])
            time.sleep(speed)
            sio.emit('p',[x1 - x, y1 - y, self.get_color_index(), 1])
            time.sleep(speed)
            sio.emit('p',[x1 - y, y1 - x, self.get_color_index(), 1])
            time.sleep(speed)
            sio.emit('p',[x1 + y, y1 - x, self.get_color_index(), 1])
            time.sleep(speed)
            sio.emit('p',[x1 + x, y1 - y, self.get_color_index(), 1])
            time.sleep(speed)
            if err <= 0:
                y += 1
                err += dy
                dy += 2
            if err > 0:
                x -= 1
                dx += 2
                err += dx - (r << 1)
        
    def circle_solid(self, color, radius, option): #needs intuitive control improvements
        try:
            radius = ((self.bxby[0]-self.txty[0])+(self.bxby[1]-self.txty[1])) // 2
        except:
            pass        
        self.get_coordinate()
        if option == 'loop':
            print('loop')
            while True:
                if keyboard.is_pressed(stop_key):
                    break
                circle_list = []
                for x in range(self.x - radius, self.x + radius):
                    for y in range(self.y - radius, self.y + radius):
                        if (x - self.x) ** 2 + (y - self.y) ** 2 <= radius ** 2:
                            circle_list+=[[x, y],]             
                circle_list.sort(key=lambda x: (x[0] - 100) ** 2 + (x[1] - 100) ** 2) #skewed print           
                for i in circle_list:
                    try:
                        clr = paintz.index(self.cache[i[0], i[1]])
                    except:
                        clr = color
                    if clr != color:
                        sio.emit('p',[i[0], i[1], abs(self.get_color_index()-clr), 1])
                        time.sleep(speed)
                    if keyboard.is_pressed(stop_key):
                        break
        else:
            circle_list = []
            for x in range(self.x - radius, self.x + radius):
                for y in range(self.y - radius, self.y + radius):
                    if (x - self.x) ** 2 + (y - self.y) ** 2 <= radius ** 2:
                        circle_list+=[[x, y],]
            circle_list.sort(key=lambda x: (x[0] - 100) ** 2 + (x[1] - 100) ** 2) #skewed print             
            for i in circle_list:
                try:
                    clr = paintz.index(self.cache[i[0], i[1]])
                except:
                    clr = color
                if clr != color:
                    sio.emit('p',[i[0], i[1], abs(self.get_color_index()-clr), 1])
                    time.sleep(speed)
                if keyboard.is_pressed(stop_key):
                    break
                
    # Trees, 3 types so far...
    # Style 1 (small tree)
    def tree_style_1(self, kind):
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
                    
    # Style 2 (medium tree)
    def tree_style_2(self, kind):
        self.start = time.time()
        tree_order = ()
        if kind == 'single':
            self.get_coordinate()
            x, y = self.x, self.y
        else:
            x, y = random.randrange(self.txty[0],self.bxby[0]),random.randrange(self.txty[1],self.bxby[1])
            self.x, self.y = x, y
        trunk=next(trunks_cycle)
        for a in range(5):
            tree_order+=([x,y-a,trunk,1],) 
        leaf=next(leaves_cycle)
        y -= a
        for b in range(3):
            tree_order+=([x+b-1,y,leaf,1],)
        y -= 1
        for c in range(3):
            tree_order+=([x+c-1,y,leaf,1],)
        y -= 1
        for d in range(3):
            tree_order+=([x+d-1,y,leaf,1],)
        y -= 1
        tree_order+=([x,y,leaf,1],)
        if kind == 'single':
            self.count+=1
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
                    
    # Style 3 (large tree)
    def tree_style_3(self, kind):
        self.start = time.time()
        tree_order = ()
        if kind == 'single':
            self.get_coordinate()
            x, y = self.x, self.y
        else:
            x, y = random.randrange(self.txty[0],self.bxby[0]),random.randrange(self.txty[1],self.bxby[1])
            self.x, self.y = x, y
        trunk=next(trunks_cycle)
        for a in range(6):
            tree_order+=([x,y-a,trunk,1],) 
        leaf=next(leaves_cycle)
        y -= a
        for b in range(3):
            tree_order+=([x+b-1,y,leaf,1],)
        y -= 1
        for c in range(3):
            tree_order+=([x+c-1,y,leaf,1],)
        y -= 1
        for d in range(3):
            tree_order+=([x+d-1,y,leaf,1],)
        y -= 1
        for e in range(3):
            tree_order+=([x+e-1,y,leaf,1],)
        y -= 1
        tree_order+=([x,y,leaf,1],)
        if kind == 'single':
            self.count+=1
            for Y in tree_order:
                sio.emit("p", Y)
                time.sleep(speed - (self.start - time.time()))
                self.start = time.time()
                
    def forest(self, option): #draws a forest
        try:
            if option != 'single':
                print(f'Planting forest. Hold {stop_key} to end task.')
            while True:
                rng = random.randint(1, 3)
                if rng == 1:
                    self.tree_style_1(option)
                elif rng == 2:
                    self.tree_style_2(option)
                elif rng == 3:
                    self.tree_style_3(option)
                if keyboard.is_pressed(stop_key):
                    print(f'Planted {self.count} trees so far. What now boss?')
                    break
                if option == 'single':
                    break
        except:
            print('Do not have forestry permit yet.')
        if self.primeCheck(self.count) == "Prime":
            print(f"#{self.count}")
        
    def primeCheck(self, n): #checks if prime int
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
                    sio.emit("p",[X-(n*self.z),Y,36,1])
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
        
    def terrain(self): #cycles terrain colors
        r = random.random()
        if r > .7:
            self.color = next(terrain_cy)
        elif r < .3: 
            self.color = next(reverse_terrain_cy)
        return self.color
            
    def oceaneer(self): #cycles ocean colors
        r = random.random()
        if r > .7:
            self.color+=1
        elif r < .3:
            self.color-=1
        if self.color < 30:
            self.color = 38
        if self.color > 38:
            self.color = 30
        return self.color

    def surf_zone(self, loc): #lake and river brush
        print('The surf breaks.')

        #init variables
        default_square = 4//2 #incase you dont have a zone in mind
        self.get_coordinate()
        self.getcurcolor()
        self.color = paintz.index(self.curcol[0])
        xy = self.x, self.y
        
        def rdxy(): #random direction for x, y
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
            try:
                (returnal := self.cache[self.x, self.y])
            except:
                returnal = None
                pass
            return returnal if returnal in paintz else None
        
        def emit_and_sleep(loc): #this sub function runs the brush code inside a retiming timer to optimize the sleeps for brush speed settings
            if loc == 'ocean':
                self.oceaneer()
            elif loc == 'nature':
                self.terrain()
            elif loc == 'color':
                pass
            else:
                print('W-what?')
                return
            sio.emit("p",[self.x, self.y, self.color, 1])                
            time.sleep(speed - (self.start - time.time()))  
            self.start = time.time()#the idea is to start your timer as soon as the last sleep was finished and base your next sleeps duration off that 
            
        def bound_check(): #this checks if you are inside your region
            if [self.txty, self.bxby] != [None, None]:
                if self.x < self.txty[0] or self.y < self.txty[1] or self.x > self.bxby[0] or self.y > self.bxby[1]:
                    try:
                        self.get_coordinate()
                        xy = self.x, self.y
                    except:
                        self.x, self.y = xy
            else:
                try:
                    self.get_coordinate()
                    self.txty = self.x-default_square, self.y-default_square
                    self.bxby = self.x+default_square, self.y+default_square
                except:
                    print('Try again.')
                    pass
                
        def localize():
            self.get_coordinate()
            xy = self.x, self.y
            
        self.start = time.time()       
        while True: 
            
            if keyboard.is_pressed(stop_key):
                print('The surf recedes.')
                return
            elif keyboard.is_pressed('s'):
                localize()
            
            pixels = rdxy()
            clr = paintz.index(pixels if pixels in paintz else (0,0,0))
            
            if self.colorfilter != [None, None, None, None, None, None, None, None, None, None]:
                if pixels in self.colorfilter:
                    emit_and_sleep(loc)
                    bound_check()
            else:
                if loc != 'color':
                    if clr not in terrain_tiles + [self.color] + [paintz.index(k) for k in trees_and_oceans]:
                        emit_and_sleep(loc)
                        bound_check()
                else:
                    if pixels != paintz[self.color]:
                        emit_and_sleep(loc)
                        bound_check()
                
    def copypaste(self, option): #this is the copy/paster
        try:
            if option == "copy": #-----copy section-----#
                if self.zone_commands != True:
                    print('Make a region first boss.')
                else:
                    print('Copying...')
                    self.work_order = ()
                    cx = (self.bxby[0] - self.txty[0]) // 2
                    cy = (self.bxby[1] - self.txty[1]) // 2
                    for X in range(self.txty[0], self.bxby[0]):
                        for Y in range(self.txty[1], self.bxby[1]):
                            if self.cache[X, Y] not in self.colorfilter + [(204,204,204)]:
                                self.work_order += ((X-self.txty[0]-cx, Y-self.txty[1]-cy, paintz.index(self.cache[X, Y])),)
                    print('Done.')
                    
            elif option == "paste": #-----paste section-----#
                if self.work_order != ():
                    self.get_coordinate()
                    self.getcurcolor()
                    for i in self.work_order:
                        if keyboard.is_pressed(stop_key):
                            print('Canceling job.')
                            return
                        if self.cache[i[0]+self.x, i[1]+self.y] not in self.colorfilter + [(204,204,204)]+ [paintz[i[2]]]:
                            sio.emit("p",[i[0]+self.x, i[1]+self.y, i[2], 1])
                            try:
                                time.sleep(speed - (time.time() - self.start))
                                self.start = time.time()
                            except:
                                time.sleep(speed)
                                self.start = time.time()
                else:
                    print('Need to copy a region first boss.')
        except:
            print('Failed.')
            pass
    
    def zone(self): #zone constructor
        self.get_coordinate()
        self.txty = self.x, self.y
        while True: #press and hold v and drag mouse and release v
            if not keyboard.is_pressed('v'):
                self.get_coordinate()
                self.bxby = self.x + 1, self.y + 1
                break
        if self.bxby[0] > self.txty[0] and self.bxby[1] > self.txty[1]:
            print ('Zoning complete.')
            self.zone_commands = True
            if self.forestry_permit == False:
                self.forestry_permit = True
                print('Issued a forestry permit.')
        else:
            print ('Zoned out.')
        
    def get_coordinate(self):#check the coordinate of where your cursor is on the selenium pixelplace site
        try:
            self.x, self.y = make_tuple(driver.find_element(By.XPATH,'/html/body/div[3]/div[4]').text)
            return self.x, self.y
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
        elif event.name in ['`', '~']:
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
        #self.color_xpath = driver.find_element(By.XPATH,'/html/body/div[3]/div[2]')
        #print(self.color_xpath)
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
        
    def get_7(self): #get the current selected map for the cache
        with open(f'{chart}.png', 'wb') as f:
            f.write(requests.get(f'https://pixelplace.io/canvas/{chart}.png?t={random.randint(9999,99999)}').content)
        self.image = PIL.Image.open(f'{chart}.png').convert('RGB')
        self.cache = self.image.load()
        
    def connection(self): #two different functions to maintain during connection, the cookies, and the pixel cache
        sio.connect('https://pixelplace.io', transports=['websocket'])        
        @sio.event
        def connect():#socket connection method for pixelplace which uses the cookis you get from auth_data()
            sio.emit("init",{"authKey":f"{self.authkey}","authToken":f"{self.authtoken}","authId":f"{self.authid}","boardId":chart})
            threading.Timer(15, connect).start()
            
        @sio.on("p") 
        def update_pixels(p: tuple): #this collects all the pixels people draw on the map into self.cache so your computer can access it quickly for the painting features
            for i in p:
                try:
                    self.cache[i[0], i[1]] = paintz[i[2]]
                except:
                    pass
    
    def auth_data(self): #get pixelplace cookies to use for maintaining socket connection
        self.authkey = driver.get_cookie("authKey").get('value')
        self.authtoken = driver.get_cookie("authToken").get('value')
        self.authid = driver.get_cookie("authId").get('value')
        
    #end of class function
        
# imports
import requests #pip install requests
import os
import json 
import keyboard #pip install keyboard
import socketio #pip install python-socketio[client]==4.6.1
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
from PIL import Image, ImageGrab, ImageDraw, ImageFont
from ast import literal_eval as make_tuple
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#Okay so... Firefox is the default browser now for Sus Bot because, quite frankly, it's just way faster than Chrome.
#If you don't have Firefox you can download it by copy and pasting this link: https://www.mozilla.org/en-US/firefox/new/
#Susbot includes the Geckodriver.exe which opens an automated browser for it to run the python code with by using one of
#the various libraries, which are above these comments.
driver = webdriver.Firefox()
sio = socketio.Client()

#But if you really want to or need to use Chrome instead, uncomment the following block of code
# at the beginning and end of its code(first and last line of it, it should be 8 lines, 2 of which you gonna delete:

'''#<remove this line>
settings for Chromedriver to not show its errors on Sus Bot:
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument("--disable-webgl")
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(options=options)
'''#<remove this line>

#And then it will be set to using Chrome instead. Just reverse what you did to get it back to Firefox, or uncomment the next two lines:
#driver = webdriver.Firefox()
#sio = socketio.Client()

#Now we are setting up the paint value stuff that the various functions will use, basically sets of colors:
#PAINT RGB VALUES
paintz =((255,255,255),(196,196,196),(136,136,136),(85,85,85),(34,34,34),
        (0,0,0),(0,102,0),(34,177,76),(2,190,1),(81,225,25),(148,224,68),
        (251,255,91),(229,217,0),(230,190,12),(229,149,0),(160,106,66),
        (153,83,13),(99,60,31),(107,0,0),(159,0,0),(229,0,0),(255,57,4),
        (187,79,0),(255,117,95),(255,196,159),(255,223,204),(255,167,209),
        (207,110,228),(236,8,236),(130,0,128),(81,0,255),(2,7,99),(0,0,234),
        (4,75,255),(101,131,207),(54,186,255),(0,131,199),(0,211,221),(69,255,200))

trees_and_oceans = [(0,102,0),(34,177,76),(2,190,1),(81,225,25),(148,224,68),
		    (229,149,0),(160,106,66),(153,83,13),(99,60,31),(187,79,0),
                    (81,0,255),(2,7,99),(0,0,234),(4,75,255),(101,131,207),
                    (54,186,255),(0,131,199),(0,211,221),(69,255,200)]

leaves = [paintz.index(k) for k in paintz if paintz.index(k) in range(6,10+1)] #the +1 ensures the end of range is accounted for
leaves_cycle = cycle(leaves)
trunks = [paintz.index(k) for k in paintz if paintz.index(k) in range(15,17+1)] + [22]
trunks_cycle = cycle(trunks)
terrain_tiles=[1,2,3,4,13,23,24] + leaves + trunks
terrain_cy = cycle(terrain_tiles)
terrain_tiles_reversed = terrain_tiles[::-1]
reverse_terrain_cy = cycle(terrain_tiles_reversed)

circle_modes = ['skewed','dot']
circle_m = cycle(circle_modes)

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
#and done, all is left are the tips, I tried to make the feel like something a pirate on the high seas might find, since this is Sus Bot Ocean Edition. Cya!
#ps if you use the bucket fill tool, you can also use colorfilters with it to black its path.
chrono = """A final word:
 His name went unmentioned.
 Points, player...
 the domain of the automatic ones are the quantities, in other words of the dead.
 order one against order the other, these automata play automata out. They picture the whole of their life and that of the dead. They serve them and support them as pillars. Nothing in them lets think of effort, or of lie. They are that - or seem to be at least - what the Order needs, or desires, or authorizes, or wishes. An implacable, a perfect police. They don't think. Nor do they want to. Without visions. Without dreams. Even without religion. A perpetual present."""
#tips
tips = ["Equip your  color with the 1 through 9  and 0 keys. Pressing ` or ~ will remove them. These can modify other abilities.",
        f"Successfully creating a zone for the first time will award you with a forest permit, allowing you to plant entire forest with {foresty_hotkey}",
        "If you want to paint underneath the guild war logos, toggle them off with Shift X.",
        'If you equip a color to the colorfilter using the 0-9 keys, and then copy something, it will not copy the equipped colors. This allows for transparency effects.',
        f'If you try to draw manually while planting a forest or other tasks, you may get speed debuffed, be careful. Pressing {stop_key} will end any tasks.',chrono,
        'If you change your speed down too much with the hotkey, it will automatically reset back to the default_value which is normally 0.02 seconds per pixel.',
        (x := f"Ꭿ+ඞ+ꇺ equals: {(Ꭿ:=.315)+(ඞ:=.35)+(ꇺ:=.335)}"),x,Ꭿ,ඞ,ꇺ,
        'You found a message in a bottle in the treasure chest as well!:\n\n"We are dead brothers.\nWe seem to be buried in the East Wet Pit.\nNot only that, but we have not yet reached this age.\nThe gentlemen buried here would have no hope of life if it were not for the ribbons you brought.\nIt is not easy to nurture a life sprouting from light.\nWe urge sincere prayers to the Lord of Light to appreciate the grace of mercy.\nPromise the Lord of Light, build the mountains through which the route passes, and continue to form.\nbrothers! No matter where you are located, there are certain things we need to follow.\nPray for this, and they will do their best to answer.\nWe look forward to eternal life, the source of which is hidden below.\n\n\nꇺ_Y~_~_O_~_~_Y~>\Ꭿ/<Y\nBrother of Graffiti."']

#start the program
susbot = Sus_Bot() #start an instance of the Sus_Bot class as 'susbot'
