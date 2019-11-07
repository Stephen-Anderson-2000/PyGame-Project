import pygame, json, sys, win32gui, win32con

# Imports the necessary modules. The latter two are to allow
# the window to start full screen


# Sets up the class for each gate
class Gate(pygame.sprite.Sprite):

    def __init__(self, new_gate_type, new_gate_num, \
                    x_pos = 800, y_pos = 300):
        pygame.sprite.Sprite.__init__(self)
        
        # Sets the default x positions for outputs or inputs
        if new_gate_type == "OUTPUT":
            x_pos = 1400
        if new_gate_type == "INPUT":
            x_pos = 500

        # Sets the values of the new gate
        self.setgateimage(new_gate_type)
        self.num = new_gate_num
        self.gate_type = new_gate_type
        self.inp_pointer1 = -99
        self.inp_pointer2 = -99
        self.inp_val1 = False
        self.inp_val2 = False
        self.pos = (x_pos, y_pos)
        self.val = False

        # Generates the rectangle and sets its position
        self.rect = self.image.get_rect()
        self.rect.h = self.rect.h + 30
        self.rect.w = self.rect.w + 40
        self.rect.x = x_pos
        self.rect.y = y_pos

    # Selects which image is required
    def setgateimage(self, new_gate_type):
        if new_gate_type == "AND":
            self.image = pygame.image.load("AND2.png").convert()
        elif new_gate_type == "NAND":
            self.image = pygame.image.load("NAND2.png").convert()
        elif new_gate_type == "OR":
            self.image = pygame.image.load("OR2.png").convert()
        elif new_gate_type == "NOR":
            self.image = pygame.image.load("NOR2.png").convert()
        elif new_gate_type == "NOT":
            self.image = pygame.image.load("NOT2.png").convert()
        elif new_gate_type == "XOR":
            self.image = pygame.image.load("XOR2.png").convert()
        elif new_gate_type == "XNOR":
            self.image = pygame.image.load("XNOR2.png").convert()
        elif new_gate_type == "INPUT":
            self.image = pygame.image.load("INPUT (OFF).png").convert()
        elif new_gate_type == "OUTPUT":
            self.image = pygame.image.load("OUTPUT (OFF).png").convert()
        # Makes their backgrounds transparent
        self.image.set_colorkey((255,255,255))

    # Allow the correct images to update due to their value
    def updategateimage(self):
        # For the input switches
        if self.gate_type == "INPUT":
            if self.val == True:
                self.image = pygame.image.load("INPUT (ON).png").convert()
            elif self.val == False:
                self.image = pygame.image.load("INPUT (OFF).png").convert()
        # For the output LEDs
        elif self.gate_type == "OUTPUT":
            if self.val == True:
                self.image = pygame.image.load("OUTPUT (ON).png").convert()
            elif self.val == False:
                self.image = pygame.image.load("OUTPUT (OFF).png").convert()

    # Changes the input switch value when called
    def updateinputswitch(self):
        if self.val == True:
            self.val = False
        elif self.val == False:
            self.val = True
        self.updategateimage()

    # Updates the position of the gate when called
    def update(self, event):
        if self.gate_type == "OUTPUT":
            offset_x = 25
            offset_y = 25
        elif self.gate_type == "INPUT":
            offset_x = 30
            offset_y = 50
        else:
            offset_x = 50
            offset_y = 30
        self.pos = (event.pos[0] - offset_x), (event.pos[1] - offset_y)
        self.rect.x = event.pos[0] - offset_x
        self.rect.y = event.pos[1] - offset_y

# Sets up the class for the buttons
class Button(pygame.sprite.Sprite):

    def __init__(self, button_type, x_pos, y_pos):
        pygame.sprite.Sprite.__init__(self)
        self.setbuttonimage(button_type)
        self.btntype = button_type
        self.pos = (x_pos, y_pos)
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos

    def setbuttonimage(self, button_type):
        if button_type == "AND":
            self.image = pygame.image.load("AND.png").convert()
        elif button_type == "NAND":
            self.image = pygame.image.load("NAND.png").convert()
        elif button_type == "OR":
            self.image = pygame.image.load("OR.png").convert()
        elif button_type == "NOR":
            self.image = pygame.image.load("NOR.png").convert()
        elif button_type == "NOT":
            self.image = pygame.image.load("NOT.png").convert()
        elif button_type == "XOR":
            self.image = pygame.image.load("XOR.png").convert()
        elif button_type == "XNOR":
            self.image = pygame.image.load("XNOR.png").convert()
        elif button_type == "INPUT":
            self.image = pygame.image.load("Input (OFF).png").convert()
        elif button_type == "OUTPUT":
            self.image = pygame.image.load("Output (OFF).png").convert()
        elif button_type == "Save":
            self.image = pygame.image.load("Save.png").convert()
        elif button_type == "Load":
            self.image = pygame.image.load("Load.png").convert()
        elif button_type == "Print":
            self.image = pygame.image.load("Print.png").convert()
        elif button_type == "Connect":
            self.image = pygame.image.load("Line Tool.png").convert()
        elif button_type == "Delete Connections":
            self.image = pygame.image.load("Delete Line Tool.png").convert()
        elif button_type == "Delete":
            self.image = pygame.image.load("Delete.png").convert()


# Defines the algorithms used to calculate the value for each gate
def calcand(gate):
    if gate.inp_val1 == True and gate.inp_val2 == True:
        return True
    else:
        return False

def calcor(gate):
    if gate.inp_val1 == True or gate.inp_val2 == True:
        return True
    else:
        return False

def calcxor(gate):
    if gate.inp_val1 == True and gate.inp_val2 == False:
        return True
    elif gate.inp_val1 == False and gate.inp_val2 == True:
        return True
    else:
        return False

def calcnot(input):
    if input == True:
        return False
    elif input == False:
        return True

# Recursive algorithm to calculate each gate value
def calculateval(gate):
    if gate.num == -99:
        return False
    elif gate.gate_type == "INPUT":
        return gate.val
    else:
        for input in group_gates:
            if input.num == gate.inp_pointer1:
                gate.inp_val1 = calculateval(input)
            if input.num == gate.inp_pointer2:
                gate.inp_val2 = calculateval(input)

    if gate.gate_type == "AND":
        gate.val = calcand(gate)
    elif gate.gate_type == "NAND":
        gate.val = calcnot(calcand(gate))
    elif gate.gate_type == "OR":
        gate.val = calcor(gate)
    elif gate.gate_type == "NOR":
        gate.val = calcnot(calcor(gate))
    elif gate.gate_type == "NOT":
        gate.val = calcnot(gate.inp_val1)
    elif gate.gate_type == "XOR":
        gate.val = calcxor(gate)
    elif gate.gate_type == "XNOR":
        gate.val = calcnot(calcxor(gate))
    elif gate.gate_type == "OUTPUT":
        gate.val = gate.inp_val1
        gate.updategateimage()

    return gate.val
 
# Finds the outputs and adds the to a list
def findoutputlist():
    outputlist = []
    for item in group_gates:
        if item.gate_type == "OUTPUT":
            outputlist.append(item.num)
    return outputlist

# Calculates the gate values starting at the outputs
def updatevals():
    outputlist = findoutputlist()
    if len(outputlist) >= 1:
        for count in range(len(outputlist)):
            for gate in group_gates:
                if gate.num == outputlist[count]:
                    calculateval(gate)


# Gets the file name that the user wants to use and
# adds the suitable file extension
def getfilename():
    file_name = input("Please enter a file name\n")
    file_name = file_name + ".json"
    return file_name

# Adds the gate data to a dictionary which can then be saved
def savecircuit():
    dict_gatedata = {}
    # Iterates for each gate
    for gate in group_gates:
        gate_data = [gate.gate_type, gate.inp_pointer1, gate.inp_pointer2, \
            gate.inp_val1, gate.inp_val2, gate.pos, gate.val, gate.rect.x, \
            gate.rect.y]
        dict_gatedata.update({gate.num: gate_data})

    # Writes to the file
    while True:
        try:
            with open(getfilename(), "w") as file:
                json.dump(dict_gatedata, file)
            break
        except:
            print("Invalid file name or path")
            user_inp = input("Would you like to try again?\n")
            if user_inp.lower() != "y" or user_inp.lower() != "yes":
                break

# Converts the dictionary of gate data to Gate objects
def convertdict(dict_gatedata):
    for count in range(1, (len(dict_gatedata) + 1)):
        pointer = str(count)
        new_gate = Gate(dict_gatedata[pointer][0], count)
        new_gate.num = count
        new_gate.inp_pointer1 = dict_gatedata[pointer][1]
        new_gate.inp_pointer2 = dict_gatedata[pointer][2]
        new_gate.inp_val1 = dict_gatedata[pointer][3]
        new_gate.inp_val2 = dict_gatedata[pointer][4]
        new_gate.pos = dict_gatedata[pointer][5]
        new_gate.val = dict_gatedata[pointer][6]
        new_gate.rect.x = dict_gatedata[pointer][7]
        new_gate.rect.y = dict_gatedata[pointer][8]
        group_gates.add(new_gate)

# Loads the dictionary that was saved to a file
def loadcircuit():
    dict_gatedata = {}
    while True:
        try:
            with open(getfilename(), "r") as file:
                dict_gatedata = json.load(file)
            break
        except IOError:
            print("Incorrect file name or path")
            user_inp = input("Would you like to try again?\n")
            if user_inp.lower() != "y" or user_inp.lower() != "yes":
                break
    # Converts the dictionary to Gate objects if the dictionary isn't empty
    if dict_gatedata != {}:
        group_gates.empty()
        convertdict(dict_gatedata)

# Makes a new Gate object
def makenewgate(new_gate_type, new_gate_num):
    new_gate = Gate(new_gate_type, new_gate_num)
    group_gates.add(new_gate)

# Generates the pre-designed buttons
def makebuttons():
    btn_and = Button("AND", 70, 200)
    btn_nand = Button("NAND", 230, 200)
    btn_or = Button("OR", 70, 300)
    btn_nor = Button("NOR", 230, 300)
    btn_xor = Button("XOR", 70, 400)
    btn_xnor = Button("XNOR", 230, 400)
    btn_not = Button("NOT", 150, 500)
    btn_input = Button("INPUT", 90, 628)
    btn_output = Button("OUTPUT", 250, 650)
    btn_save = Button("Save", 50, 30)
    btn_load = Button("Load", 150, 30)
    #btn_print = Button("Print", 290, 30)
    btn_connect = Button("Connect", 50, 850)
    btn_del_connect = Button("Delete Connections", 170, 850)
    btn_delete = Button("Delete", 290, 850)
    group_buttons.add(btn_and)
    group_buttons.add(btn_nand)
    group_buttons.add(btn_or)
    group_buttons.add(btn_nor)
    group_buttons.add(btn_xor)
    group_buttons.add(btn_xnor)
    group_buttons.add(btn_not)
    group_buttons.add(btn_input)
    group_buttons.add(btn_output)
    group_buttons.add(btn_save)
    group_buttons.add(btn_load)
    #group_buttons.add(btn_print)
    group_buttons.add(btn_connect)
    group_buttons.add(btn_del_connect)
    group_buttons.add(btn_delete)

# Returns the type of button that collided with the mouse
def findbuttoncollision(event):
    for button in group_buttons:
        if button.rect.collidepoint(event.pos):
            button_type = button.btntype
            return button_type

# Returns the name of the gate that collided with the mouse
def findgatecollision(event):
    for gate in group_gates:
        if gate.rect.collidepoint(event.pos):
            gate_name = gate.num
            return gate_name
    return ""


# Connects to gates together
def connectgates(gate_num1, gate_num2):
    for gate in group_gates:
        if gate.num == gate_num2:
            gate_inp = gate_num1
            if gate.inp_pointer1 == -99 and gate_inp != gate.num:
                gate.inp_pointer1 = gate_inp
            elif gate.inp_pointer2 == -99 and gate_inp != gate.num:
                gate.inp_pointer2 = gate_inp

# Removes all of the connections going to and from a gate
def deleteconnections(gate):
    gate.inp_pointer1 = -99
    gate.inp_pointer2 = -99
    for object in group_gates:
        if object.inp_pointer1 == gate.num:
            object.inp_pointer1 = -99
            object.inp_val1 = False
        if object.inp_pointer2 == gate.num:
            object.inp_pointer2 = -99
            obejct.inp_val2 = False

# Deletes a gate
def deletegate(gate):
    deleteconnections(gate)
    group_gates.remove(gate)


def drawconnectors(screen):
    # Iterates for each gate
    for gate in group_gates:
        # Can't have inputs as an input switch
        if gate.gate_type != "INPUT":
            # If the first connector is empty
            if gate.inp_pointer1 != -99:
                drawfirstconnector(gate, screen)
          
        # Second connections can't be drawn to an input, output or 
        # a not gate
        if gate.gate_type != "INPUT" and gate.gate_type != "OUTPUT" \
           and gate.gate_type != "NOT":
            # If the second connector is empty
            if gate.inp_pointer2 != -99:
                drawsecondconnector(gate, screen)

        # Makes sure the inputs and outputs have the right images
        gate.updategateimage()

    pygame.display.update()
  
# Draws the connector to the first input
def drawfirstconnector(gate, screen):
    for in_gate in group_gates:
        if in_gate.num == gate.inp_pointer1:
            # Calculates default offsets
            # From input gate's output
            x_offset_out = 94
            y_offset_out = 24

            # To input of connecting gate
            x_offset_in = 5
            y_offset_in = 14

            # Changes the required offsets as necessary
            if in_gate.gate_type == "INPUT":
                x_offset_out = 55
                y_offset_out = 39
            if gate.gate_type == "OUTPUT":
                x_offset_in = 3
                y_offset_in = 24
            if gate.gate_type == "NOT":
                y_offset_in = 25

            # Calculates the start and end points, then draws the line
            start_point = (in_gate.rect.x + x_offset_out, in_gate.rect.y + y_offset_out)
            end_point = (gate.rect.x + x_offset_in, gate.rect.y + y_offset_in)
            pygame.draw.line(screen, (0, 0, 0), start_point, end_point, 2)

# Draws the connector to the second input
def drawsecondconnector(gate, screen):
    for in_gate in group_gates:
        if in_gate.num == gate.inp_pointer2:
            # Calculates default offsets
            # From input gate's output
            x_offset_out = 94
            y_offset_out = 24

            # To input of connecting gate
            x_offset_in = 5
            y_offset_in = 34

            # Changes the required offsets as necessary
            if in_gate.gate_type == "INPUT":
                x_offset_out = 55
                y_offset_out = 39
            if gate.gate_type == "OUTPUT":
                x_offset_in = 3
                y_offset_in = 24
            if gate.gate_type == "NOT":
                y_offset_in = 25

            # Calculates the start and end points, then draws the line
            start_point = (in_gate.rect.x + x_offset_out, in_gate.rect.y + y_offset_out)
            end_point = (gate.rect.x + x_offset_in, gate.rect.y + y_offset_in)
            pygame.draw.line(screen, (0, 0, 0), start_point, end_point, 2)

    
def findmidpoint(start_point, end_point):
    if start_point < end_point:
        temp = end_point - start_point
    elif start_x > end_x:
        temp = start_point - end_point
    temp_x = temp_x / 2
    mid_point = start_point + temp
    return mid_point

# Finds what action to take
# Changes the necessary boolean values or makes the correct gate
def mousedown(event, connecting, deleting, deleting_connections, moving):
    # Gets the button type that the mouse collided with
    button_type = findbuttoncollision(event)
    # Changes boolean vars based on the buttons pressed
    if button_type == "Delete":
        connecting = False
        deleting = True
        deleting_connections = False
        moving = False
    elif button_type == "Connect":
        connecting = True
        deleting = False
        deleting_connections = False
        moving = False
    elif button_type == "Delete Connections":
        connecting = False
        deleting = False
        deleting_connections = True
        moving = False
    # Generates the required gate
    elif button_type == "AND":
        makenewgate("AND", (len(group_gates) + 1))
    elif button_type == "NAND":
        makenewgate("NAND", (len(group_gates) + 1))
    elif button_type == "OR":
        makenewgate("OR", (len(group_gates) + 1))
    elif button_type == "NOR":
        makenewgate("NOR", (len(group_gates) + 1))
    elif button_type == "XOR":
        makenewgate("XOR", (len(group_gates) + 1))
    elif button_type == "XNOR":
        makenewgate("XNOR", (len(group_gates) + 1))
    elif button_type == "NOT":
        makenewgate("NOT", (len(group_gates) + 1))
    elif button_type == "INPUT":
        makenewgate("INPUT", (len(group_gates) + 1))
    elif button_type == "OUTPUT":
        makenewgate("OUTPUT", (len(group_gates) + 1))
    # Left mouse button pressed
    elif event.button == 1:
        # Checks and updates the necessary boolean vars
        if connecting == True:
            connecting = True
            moving = False
        elif deleting_connections == True:
            deleting_connections = True
            moving = False
        elif deleting == True:
            deleting = True
            moving = False
        else:
            connecting = False
            deleting = False
            deleting_connections = False
            moving = True
    # Middle mouse button pressed
    elif event.button == 2:
        # Mimics the delete connection button
        connecting = False
        deleting = False
        deleting_connections = True
        moving = False
    # Right mouse button pressed
    elif event.button == 3:
        # Disables the current tool
        connecting = False
        deleting = False
        deleting_connections = False
        moving = False
    return(connecting, deleting, deleting_connections, moving)

# The main PyGame function
def drawscreen(screen):
    # Defines the required variables
    clock = pygame.time.Clock() 
    click_timer = pygame.time.Clock()
    connecting = False
    deleting = False
    deleting_connections = False
    moving = False
    con_first_gate = ""
    con_second_gate = ""
    last_click = 0
    # Runs until PyGame is shut
    while True:
        # Draws the required components
        screen.fill((255, 255, 255))
        pygame.draw.rect(screen, (0, 162, 232), (0, 0, 400, 1080))
        updatevals()
        group_buttons.draw(screen)
        group_gates.draw(screen)
        drawconnectors(screen)
        # Selects the correct section PyGame event occurs
        for event in pygame.event.get():
            # Quits the PyGame window
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                break
            # Resizes the PyGame window when interacted with
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            # Finds what to do when a mouse button is pressed
            elif event.type == pygame.MOUSEBUTTONDOWN:

                # Code to time between clicks to see if the user double-clicked
                # Taken from StackOverFlow
                if event.button == 1:
                    current_click = pygame.time.get_ticks()
                    if current_click - last_click <= 500:
                        gate_name = findgatecollision(event)
                        for gate in group_gates:
                            if gate.num == gate_name and gate.gate_type == "INPUT":
                                gate.updateinputswitch()
                    last_click = pygame.time.get_ticks()

                # Runs the save function
                if findbuttoncollision(event) == "Save":
                    savecircuit()
                # Runs the load function
                elif findbuttoncollision(event) == "Load":
                    loadcircuit()
                # Updates the boolean variables
                connecting, deleting, deleting_connections, moving = mousedown(event, connecting, deleting, deleting_connections, moving)
                # Starts connecting two gates
                if connecting == True:
                    # Finds the number of the gate that is being used
                    gate_name = findgatecollision(event)
                    for gate in group_gates:
                        # Sets the first or second gate pointer
                        if gate.num == gate_name and first_gate == "":
                            first_gate = gate.num
                        elif gate.num == gate_name and second_gate == "":
                            second_gate = gate.num
                    # Connects the gates as long as two are selected
                    if first_gate != "" and second_gate != "":
                        connectgates(first_gate, second_gate)
                        first_gate = ""
                        second_gate = ""
                # Resets the gate pointers if not currently connecting
                elif connecting == False:
                    first_gate = ""
                    second_gate = ""
                # Starts deleting the connections to and from a gate
                if deleting_connections == True:
                    gate_name = findgatecollision(event)
                    for gate in group_gates:
                        # Finds the gate to delete the connections of
                        if gate.num == gate_name:
                            deleteconnections(gate)
                # Deletes a selected gate
                if deleting == True:
                    gate_name = findgatecollision(event)
                    for gate in group_gates:
                        if gate.num == gate_name:
                            deletegate(gate)
            # Starts moving a gate by following the mouse
            elif event.type == pygame.MOUSEMOTION:
                if moving == True:
                    gate_name = findgatecollision(event)
                    for gate in group_gates:
                        if gate.num == gate_name:
                            # Updates the Gate's co-ordinates
                            gate.pos = event.pos
                            gate.rect.x, gate.rect.y = event.pos
                            gate.update(event)  

            # Stops moving a Gate
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    moving = False
                
                    
        pygame.display.update()
        # Sets the refresh rate
        clock.tick(60)

def main():
    # Defines all of the global variables
    global group_gates
    global group_buttons
    global dict_gates
    global gate_counter
    global connecting
    global deleting
    global deleting_connections
    global moving
    # Initialises and sets up the PyGame window
    pygame.init()
    screen = pygame.display.set_mode((500, 500), pygame.RESIZABLE)
    hwnd = win32gui.GetForegroundWindow()

    # Maximises the window
    # Taken from stack overflow
    win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)

    # Makes the sprite groups and the pre designed buttons
    group_gates = pygame.sprite.Group()
    group_buttons = pygame.sprite.Group()
    makebuttons()
    drawscreen(screen)


main()