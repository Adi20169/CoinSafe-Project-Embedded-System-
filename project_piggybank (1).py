#import statements
import Adafruit_BBIO.GPIO as GPIO #import GPIO functionality
import time 

#initializing variables for each of the coins
quarter = 0
nickel = 0
penny = 0
dime = 0

#using setup for the gpio pins controlling each of the coins
#and event detection for the PIR sensor
GPIO.setup("P9_18", GPIO.IN) #q
GPIO.setup("P9_17", GPIO.IN) #n
GPIO.setup("P9_19", GPIO.IN) #p
GPIO.setup("P9_20", GPIO.IN) #d
GPIO.add_event_detect("P9_18", GPIO.RISING) 
GPIO.add_event_detect("P9_17", GPIO.RISING)
GPIO.add_event_detect("P9_19", GPIO.RISING) 
GPIO.add_event_detect("P9_20", GPIO.RISING) 

#setting up the GPIO pins for the 7-segment display
GPIO.setup("P9_11", GPIO.OUT, GPIO.PUD_DOWN)
GPIO.setup("P9_12", GPIO.OUT, GPIO.PUD_DOWN)
GPIO.setup("P9_13", GPIO.OUT, GPIO.PUD_DOWN)
GPIO.setup("P9_14", GPIO.OUT, GPIO.PUD_DOWN)
GPIO.setup("P9_15", GPIO.OUT, GPIO.PUD_DOWN)
GPIO.setup("P9_16", GPIO.OUT, GPIO.PUD_DOWN)
GPIO.setup("P9_23", GPIO.OUT, GPIO.PUD_DOWN)
GPIO.setup("P9_24", GPIO.OUT, GPIO.PUD_DOWN)
GPIO.setup("P9_41", GPIO.OUT, GPIO.PUD_DOWN)
GPIO.setup("P9_26", GPIO.OUT, GPIO.PUD_DOWN)
GPIO.setup("P9_27", GPIO.OUT, GPIO.PUD_DOWN)
GPIO.setup("P9_30", GPIO.OUT, GPIO.PUD_DOWN)

def total_amount(q, d, n, p):
    total = 25*q + 10*d + 5*n + 1*p #multiples amount of coins with their respect values
    return total #returns the total value of all the coins

def led_display(num):
	pins = ["P9_12", "P9_16", "P9_26", "P9_24", "P9_23", "P9_13", "P9_11"]
	dic = {0: [1, 1, 1, 1, 1, 1, 0], 
		   1: [0, 1, 1, 0, 0, 0, 0],
		   2: [1, 1, 0, 1, 1, 0, 1],
		   3: [1, 1, 1, 1, 0, 0, 1],
		   4: [0, 1, 1, 0, 0, 1, 1],
		   5: [1, 0, 1, 1, 0, 1, 1],
		   6: [1, 1, 1, 1, 1, 0, 1],
		   7: [1, 1, 1, 0, 0, 0, 0],
		   8: [1, 1, 1, 1, 1, 1, 1],
		   9: [1, 1, 1, 0, 0, 1, 1]}  #creates a dictionary of the pin setup for each of the numbers expressed on the seven-segment display
	
	number = dic[num] #selects the correct array depending on the number number needed to be displayed
	for j in range(len(number)): #loops through array, if the content equal a 1 that segment will be turned on, otherwise it will be off
		if(number[j] == 1):
			GPIO.output(pins[j], GPIO.HIGH)
		else:
			GPIO.output(pins[j], GPIO.LOW)

def total_display_num(value):
    #tens place
	GPIO.output("P9_15", GPIO.LOW)  #controls d1
	GPIO.output("P9_27", GPIO.HIGH) #controls d2
	GPIO.output("P9_30", GPIO.HIGH) #controls d3
	GPIO.output("P9_41", GPIO.HIGH) #controls d4
	led_display(value//1000) #divides by a thousand to find tens place digit
	GPIO.output("P9_14", GPIO.LOW)  #h
	time.sleep(0.002)
	
    #ones place
	GPIO.output("P9_15", GPIO.HIGH) #controls d1
	GPIO.output("P9_27", GPIO.LOW)  #controls d2
	GPIO.output("P9_30", GPIO.HIGH) #controls d3
	GPIO.output("P9_41", GPIO.HIGH) #controls d4
	led_display((value%1000)//100) #takes the remainder from previous part and divides by 100 to find the ones place
	GPIO.output("P9_14", GPIO.HIGH) #h --> turns on the decimal as next two digits represent cents
	time.sleep(0.002)

    #tenths place
	GPIO.output("P9_15", GPIO.HIGH) #controls d1
	GPIO.output("P9_27", GPIO.HIGH) #controls d2
	GPIO.output("P9_30", GPIO.LOW)  #controls d3
	GPIO.output("P9_41", GPIO.HIGH) #controls d4
	led_display((value%100)//10)  #takes the remainder from previous part and divides by 10 to find the tenths place
	GPIO.output("P9_14", GPIO.LOW) #h
	time.sleep(0.002)
    
	#hundredths place	
	GPIO.output("P9_15", GPIO.HIGH) #controls d1
	GPIO.output("P9_27", GPIO.HIGH) #controls d2
	GPIO.output("P9_30", GPIO.HIGH) #controls d3
	GPIO.output("P9_41", GPIO.LOW)  #controls d4
	led_display(value%10) #takes the remainder of the value to find the hundredths place
	GPIO.output("P9_14", GPIO.LOW) #h
	time.sleep(0.002)
	
try:
	while True:
		if GPIO.event_detected("P9_18"): #detects whether a quarter has been inserted, adds to one count if detected
			quarter += 1
		if GPIO.event_detected("P9_17"): #detects whether a nickel has been inserted, adds to one count if detected
			nickel += 1
		if GPIO.event_detected("P9_19"): #detects whether a penny has been inserted, adds to one count if detected
			penny += 1
		if GPIO.event_detected("P9_20"): #detects whether a dime has been inserted, adds to one count if detected
			dime += 1
			
		x = total_amount(quarter, dime, nickel, penny) #takes in the number of quarters, dimes, nickels, and pennies detected
		money_str = '{:.2f}'.format(x / 100) #formats total amount into decimal places
		formatted_money = '$' + money_str #adds the money symbol to properly format the total amount
		print(formatted_money) #prints the money value
		total_display_num(x) #displays the correct value of the coins using seven-segment display

except KeyboardInterrupt:               #set up keyboard interrupt ctrl C
		GPIO.output("P9_11", GPIO.LOW)
		GPIO.output("P9_12", GPIO.LOW)
		GPIO.output("P9_13", GPIO.LOW)
		GPIO.output("P9_14", GPIO.LOW)
		GPIO.output("P9_15", GPIO.LOW)
		GPIO.output("P9_16", GPIO.LOW)
		GPIO.output("P9_23", GPIO.LOW)
		GPIO.output("P9_24", GPIO.LOW)
		GPIO.output("P9_41", GPIO.LOW)
		GPIO.output("P9_26", GPIO.LOW)
		GPIO.output("P9_27", GPIO.LOW)
		GPIO.output("P9_30", GPIO.LOW)
		GPIO.cleanup()                          #cleanup all used GPIO pins
		
print ("Ending program")                #print end of program to terminal
