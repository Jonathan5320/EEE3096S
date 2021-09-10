# Import libraries
import RPi.GPIO as GPIO
import random
import ES2EEPROMUtils
import os

# some global variables that need to change as we run the program
end_of_game = None  # set if the user wins or ends the game
guess = 0
scores = 0
ran_num = 1

# DEFINE THE PINS USED HERE
LED_value = [11, 13, 15]
LED_accuracy = 32
btn_submit = 16
btn_increase = 18
buzzer = 33
eeprom = ES2EEPROMUtils.ES2EEPROM()
PWM_one = None
PWM_two = None 


# Print the game banner
def welcome():
    os.system('clear')
    print(" _   _                 _                  _____ _            __  __ _")
    print("| \ | |               | |                / ____| |          / _|/ _| |")
    print("|  \| |_   _ _ __ ___ | |__   ___ _ __  | (___ | |__  _   _| |_| |_| | ___ ")
    print("| . ` | | | | '_ ` _ \| '_ \ / _ \ '__|  \___ \| '_ \| | | |  _|  _| |/ _ \\")
    print("| |\  | |_| | | | | | | |_) |  __/ |     ____) | | | | |_| | | | | | |  __/")
    print("|_| \_|\__,_|_| |_| |_|_.__/ \___|_|    |_____/|_| |_|\__,_|_| |_| |_|\___|")
    print("")
    print("Guess the number and immortalise your name in the High Score Hall of Fame!")


# Print the game menu
def menu():
    global end_of_game, ran_num
    option = input("Select an option:   H - View High Scores     P - Play Game       Q - Quit\n")
    option = option.upper()
    if option == "H":
        os.system('clear')
        print("HIGH SCORES!!")
        s_count, ss = fetch_scores()
        display_scores(s_count, ss)
    elif option == "P":
        os.system('clear')
        print("Starting a new round!")
        print("Use the buttons on the Pi to make and submit your guess!")
        print("Press and hold the guess button to cancel your game")
        ran_num = generate_number()
        print (ran_num)
        while not end_of_game:
            pass
    elif option == "Q":
        print("Come back soon!")
        GPIO.cleanup()
        exit()
    else:
        print("Invalid option. Please select a valid one!")


def display_scores(count, raw_data):
    # print the scores to the screen in the expected format
    print("There are {} scores. Here are the top 3!".format(*count))
    # print out the scores in the required format
    pass


# Setup Pins
def setup():

    global PWM_one,PWM_two
    # Setup board mode
    GPIO.setmode(GPIO.BOARD)
    # Setup regular GPIO
    GPIO.setup(LED_value[0],GPIO.OUT)
    GPIO.setup(LED_value[1],GPIO.OUT)
    GPIO.setup(LED_value[2],GPIO.OUT)
    GPIO.output(LED_value[0],0)
    GPIO.output(LED_value[1],0)
    GPIO.output(LED_value[2],0)

    GPIO.setup(LED_accuracy,GPIO.OUT)
    PWM_one = GPIO.PWM(LED_accuracy,1000)
    PWM_one.start(0)
    # Buzzer PWM channel
    GPIO.setup(buzzer,GPIO.OUT)
    PWM_two =GPIO.PWM(buzzer,1)
    PWM_two.start(50)
    # Setup PWM channels EEPROM
    GPIO.setup(5,GPIO.OUT)
    GPIO.setup(3,GPIO.OUT)
    # Setup debouncing and callbacks
    GPIO.setup(btn_submit,GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(btn_increase,GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(btn_submit, GPIO.FALLING, btn_guess_pressed, bouncetime=5000)
    GPIO.add_event_detect(btn_increase, GPIO.RISING, btn_increase_pressed, bouncetime=400)
    pass


# Load high scores
def fetch_scores():
    # get however many scores there are
    global score_count
    score_count = read_byte(30)
    # Get the scores
    a=0
    wo = None
    while a <= 29:
        while a<=8:
            number = read_byte(a)
            wo[0:a] = chr(number)
            a = a+1
        word_1 = "".join(wo)
        score_1 = chr(read_byte(9))
        a= a+1

        while 10<a<=18:
            number = read_byte(a)
            wo[0:a] = chr(number)
            a = a+1
        word_2 = "".join(wo)
        score_2 = chr(read_byte(19))
        a= a+1

        while 20<a<=28:
            number = read_byte(a)
            wo[0:a] = chr(number)
            a= a+1
        word_3 = "".join(wo)
        score_3 = chr(read_byte(29))

    # convert the codes back to ascii
    scores = [[word_1, score_1],[word_2, score_2],[word_3, score_3]]
    # return back the results
    return score_count, scores


# Save high scores
def save_scores():
    # fetch scores
    score_count,scores = fetch_scores()
    # include new score
    # sort
    # update total amount of scores
    # write new scores




    pass


# Generate guess number
def generate_number():
    return random.randint(0, pow(2, 3)-1)


# Increase button pressed
def btn_increase_pressed(channel):
    # Increase the value shown on the LEDs
    # You can choose to have a global variable store the user's current guess,
    # or just pull the value off the LEDs when a user makes a guess
    global guess, LED_value
    GPIO.output(LED_value[0],0)
    GPIO.output(LED_value[1],0)
    GPIO.output(LED_value[2],0)

    if guess<=6:
        guess +=1
        print ("guess + 1 = ",guess)
    else:
#        print ("Max guess number set guess back to 0")
        guess = 0

    if (guess == 1):
        GPIO.output(LED_value[0],1)
        trigger_buzzer()
        accuracy_leds()
    elif (guess == 2):
        GPIO.output(LED_value[1],1)
        trigger_buzzer()
        accuracy_leds()
    elif (guess == 3):
        GPIO.output(LED_value[0],1)
        GPIO.output(LED_value[1],1)
        trigger_buzzer()
        accuracy_leds()
    elif (guess == 4):
        GPIO.output(LED_value[2],1)
        trigger_buzzer()
        accuracy_leds()
    elif (guess == 5):
        GPIO.output(LED_value[0],1)
        GPIO.output(LED_value[2],1)
        trigger_buzzer()
        accuracy_leds()
    elif (guess == 6):
        GPIO.output(LED_value[1],1)
        GPIO.output(LED_value[2],1)
        trigger_buzzer()
        accuracy_leds()
    elif (guess ==7):
        GPIO.output(LED_value[0],1)
        GPIO.output(LED_value[1],1)
        GPIO.output(LED_value[2],1)
        trigger_buzzer()
        accuracy_leds()
pass


# Guess button
def btn_guess_pressed(channel):
    # If they've pressed and held the button, clear up the GPIO and take them back to the menu screen
    # Compare the actual value with the user value displayed on the LEDs
    # Change the PWM LED
    # if it's close enough, adjust the buzzer
    # if it's an exact guess:
    # - Disable LEDs and Buzzer
    # - tell the user and prompt them for a name
    # - fetch all the scores
    # - add the new score
    # - sort the scores
    # - Store the scores back to the EEPROM, being sure to update the score count

    print ("hello")
    


pass


# LED Brightness
def accuracy_leds():
    # Set the brightness of the LED based on how close the guess is to the answer
    # - The % brightness should be directly proportional to the % "closeness"
    # - For example if the answer is 6 and a user guesses 4, the brightness should be at 4/6*100 = 66%
    # - If they guessed 7, the brightness would be at ((8-7)/(8-6)*100 = 50%

    global guess, PWM_one, ran_num
    PWM_one.start(50)
    if (guess <= ran_num):
        PWM_one.ChangeDutyCycle(int(round((guess/ran_num)*100)))
        print ("guess <= ran_num", int(round((guess/ran_num)*100)))
    else:
        PWM_one.ChangeDutyCycle(int(round(((8-guess)/(8-ran_num))*100)))
        print ("else", int(round(((8-guess)/(8-ran_num))*100)))
pass

# Sound Buzzer
def trigger_buzzer():
    # The buzzer operates differently from the LED
    # While we want the brightness of the LED to change(duty cycle), we want the frequency of the buzzer to change
    # The buzzer duty cycle should be left at 50%
    # If the user is off by an absolute value of 3, the buzzer should sound once every second
    # If the user is off by an absolute value of 2, the buzzer should sound twice every second
    # If the user is off by an absolute value of 1, the buzzer should sound 4 times a second

    global guess, PWM_two, ran_num
    
    PWM_one.start(50)
    a = abs(guess-ran_num)
    
    if a == 1:
        PWM_two.ChangeFrequency(4)
        print ("fre 1")
    elif a == 2:
        PWM_one.ChangeFrequency(2)
        print ("fre 2")
    elif a == 3:
        PWM_one.ChangeFrequency(1)
        print ("fre 3")
    else:
        PWM_one.ChangeFrequency(0.5)
    print ("a=",a)
    print (ran_num)
    pass


if __name__ == "__main__":
    try:
        # Call setup function
        setup()
        welcome()
        while True:
            menu()
            pass
    except Exception as e:
        print(e)
    finally:
        GPIO.cleanup()
