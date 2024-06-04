import Adafruit_BBIO.GPIO as GPIO #import GPIO functionality
import Adafruit_BBIO.PWM as PWM # import PWM functionality
import time 
#assign variables to pins for RGB leds
R = "P9_14"
G = "P9_16"
B = "P9_21"

PWM.start(R, 0)
PWM.start(G, 0)
PWM.start(B, 0)

PWM.start("P8_13", 12.5, 50, 0) #initialize PWM on P8_13 pin with a duty cycle of 2.5, frequency of 50Hz and polarity 0

# Create a map between keypad buttons and characters
matrix_keys = [['1', '2', '3', 'A'],
               ['4', '5', '6', 'B'],
               ['7', '8', '9', 'C'],
               ['*', '0', '#', 'D']]

# PINs according to schematic - Change the pins to match with your connections
rows = ["P9_18","P9_17","P9_22","P9_15"]
columns = ["P9_23","P9_13","P9_12","P9_11"]

guess = []

# Loop to assign GPIO pins and setup input and outputs
for x in range(0,4):
    GPIO.setup(rows[x], GPIO.OUT)
    GPIO.output(rows[x], GPIO.HIGH)
    GPIO.setup(columns[x], GPIO.IN, GPIO.PUD_DOWN)
    
##############################Scan keys ####################

def map(x, in_min, in_max, out_min, out_max):
	return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

#setting color based on the RGB value
def setColor(col):   # For example : col = 0x112233
	R_val = (col & 0xff0000) >> 16
	G_val = (col & 0x00ff00) >> 8
	B_val = (col & 0x0000ff) >> 0

	R_val = map(R_val, 0, 255, 0, 100)
	G_val = map(G_val, 0, 255, 0, 100)
	B_val = map(B_val, 0, 255, 0, 100)
	
	PWM.set_duty_cycle(R, 100-R_val)     # Change duty cycle
	PWM.set_duty_cycle(G, 100-G_val)     # Change duty cycle
	PWM.set_duty_cycle(B, 100-B_val)     # Change duty cycle
   
#this function basically checks if the correct combination is entered 
#Basically if the length of the password isn’t 7 false is returned, since it can only be up to 7 #characters/numbers
#otherwise goes through the for loop which checks if the character is in the num_let array
#to validate the input, if it is increments count by 1
#the if statement following that compares the count variable(which should have the length of the #combination at this point, is the same length as the password being passed in
#then return true otherwise false
def valid_p(password):
    num_let = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "#", "*"]
    if(len(password) != 7): 
        return False
    Else: 
        count = 0
        for i in range(len(password)):
            if password[i] in num_let:
                count += 1
        if(count == len(password)):
            return True
        return False

#This section of the code checks if a button is pressed and stores it stores it in the guess list
#two variables are initialized to true, then a nested for loop is used to iterate
#through the rows and columns of the keypad. butVal stores the input
#if that input is 1 then that means a button is pressed, and the character/number
#is gotten from the matrix, no press is then false indicating that a button got pressed
#if the button is pressed and that button wasn’t pressed before, then it gets appended to the
#empty list created earlier(guess)
def button():
	noPress = True
	noPressOld = True
	
	for myRow in range(4):
		for myCol in range(4):
			GPIO.output(rows[myRow], GPIO.HIGH)
			butVal = GPIO.input(columns[myCol])
			GPIO.output(rows[myRow], GPIO.LOW)
				
			if butVal == 1:
				myChar = matrix_keys[myRow][myCol]
				noPress = False
				
			if butVal == 1 and noPress == False and noPressOld == True:
				guess.append(myChar)
				print(myChar)
			
	noPressOld = noPress
	time.sleep(0.2)

#this function checks the actual validity of the combination password
#to do so the list is converted into a string and string comparison is used to check if the
#guessed password is the same as the actual password.
#if it is then the color of the rgb leds is set to green, otherwise it’s set to red
def correct_password(p):
	p = "".join(p)
	
	if(p == password):
		print("CORRECT")
		setColor(0x00FF00)
		PWM.set_duty_cycle("P8_13", 7.5)
		return True
	else:
		setColor(0xFF0000)
		return False

#this while true, initializes the colors of the led, prompt the user to set the password(7 chars)
#then calls the valid_p function in a loop and while the user puts in a wrong password
#prints an error message, and prompts the user to create a new password
#a second while loop validates that the user puts in the right password, if they do, then
#a for loop iterates through 7(for the 7 chars and numbers that will be entered)
#and the button(), gets the button being pressed
#if the length of guess(list that stores all the values) is 7 and the password is wrong another #error message is printed
#basically a lot of verifications that the password being put in is the right length and the right #combination
try:

	while True:
		setColor(0x000000)
		password = input("Create Password (Must be 7 characters): ")
		while(valid_p(password) == False):
			print("Invalid password, please try again!")
			password = input("Create Password (Must be 7 characters): ")
		
		print("Please enter the password: ")
		
		while(valid_p(password) == True):
			for i in range(7):
				button()
				time.sleep(0.001)
		
			if(len(guess) == 7):
				if(correct_password(guess) == False):
					print("Incorrect Password! Better luck next time.")
				break
		break
				
#handles the exceptions
except KeyboardInterrupt:               #set up keyboard interrupt ctrl C
		GPIO.output("P9_11", GPIO.LOW)
		GPIO.output("P9_12", GPIO.LOW)
		GPIO.output("P9_13", GPIO.LOW)
		GPIO.output("P9_14", GPIO.LOW)
		GPIO.output("P9_15", GPIO.LOW)
		GPIO.output("P9_16", GPIO.LOW)
		GPIO.output("P9_17", GPIO.LOW)
		GPIO.output("P9_18", GPIO.LOW)
		GPIO.output("P9_19", GPIO.LOW)
		PWM.stop("P8_13")
		setColor(0x000000)
		GPIO.cleanup()                          #cleanup all used GPIO pins

