import cvzone
import cv2 as cv
from isodate import time_isoformat
import HandTrackingModule as htm
from time import time
from random import randint

# Constants
WAIT_TIME = 3
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
ORANGE = (150, 150, 0)
FONT = cv.FONT_HERSHEY_PLAIN
WEBCAM = cv.VideoCapture(0) 
WEBCAM.set(3, WINDOW_WIDTH)
WEBCAM.set(4, WINDOW_HEIGHT)
HAND_DECTECTOR = htm.handDetector(detectionCon=0.8, maxHands=1)
IMG_ROCK = cv.imread(f'images/rock.png', cv.IMREAD_UNCHANGED)
IMG_PAPER = cv.imread(f'images/paper.png', cv.IMREAD_UNCHANGED)
IMG_SCISSORS = cv.imread(f'images/scissors.png', cv.IMREAD_UNCHANGED)

# Variables
bot_score, player_score = 0, 0
pre_time = time()
choice_player, choice_bot = None, None
choice_bot = ['rock', 'paper', 'scissors'][randint(0, 2)]
time_left = 5

def check_hand_gesture(fingers_up):
    if fingers_up == 0:
        return 'rock'
    elif fingers_up == 5:
        return 'paper'
    elif fingers_up == 2:
        return 'scissors'
    else:
        return None

def draw_text(text, text_x, text_y, text_size, color=WHITE):
    cv.putText(frame, str(text), (text_x, text_y), FONT, text_size, BLACK, 8, cv.LINE_AA)
    cv.putText(frame, str(text), (text_x, text_y), FONT, text_size, color, 4, cv.LINE_AA)

def check_winner(choice_bot, choice_player):
    if choice_player == None or choice_bot == None:
        return None
    elif choice_player == choice_bot:
        return 'draw'
    elif choice_player == 'rock' and choice_bot == 'scissors':
        return 'player'
    elif choice_player == 'paper' and choice_bot == 'rock':
        return 'player'
    elif choice_player == 'scissors' and choice_bot == 'paper':
        return 'player'
    else:
        return 'bot'

def draw_gesture(frame, gesture, x, y, flipped=False):
    if gesture is None:
        return frame
    elif gesture == 'rock':
        gesture_img = IMG_ROCK
    elif gesture == 'paper':
        gesture_img = IMG_PAPER
    elif gesture == 'scissors':
        gesture_img = IMG_SCISSORS
    if flipped:
        gesture_img = cv.flip(gesture_img, 1)
    new_frame = cvzone.overlayPNG(frame, gesture_img, [x, y])
    return new_frame

while True:
    # Calculate time and FPS
    cur_time = time()
    delta_time = cur_time - pre_time
    pre_time = cur_time
    if delta_time == 0:
        fps = 0
    else:
        fps = 1 / delta_time
    if time_left > 0:
        time_left -= delta_time
    else:
        time_left = 0.0

    # Read webcam, find + draw hands and get + update hand landmarks
    frame = cv.cvtColor(cv.flip(WEBCAM.read()[1], 1), cv.COLOR_BGR2RGB) 
    frame = HAND_DECTECTOR.find_hands(frame) 
    landmarks = len(HAND_DECTECTOR.landmarks(frame))

    # Get player's gesture
    if landmarks > 0:
        fingers_up = HAND_DECTECTOR.get_fingers_up()
        if time_left > 0:
            choice_player = check_hand_gesture(fingers_up)
    
    # Draw text ang gestuers on frame
    draw_text(f'FPS: {int(fps)}', 20, 40, 1.9)
    draw_text(f"Player's choice:", 850, 270, 2.5)
    frame = draw_gesture(frame, choice_player, 910, 270, True)
    if time_left > 0:
        draw_text(f'Countdown: {round(time_left, 1)}s'.center(51), -120, 150, 3.5)
    else:
        draw_text(f"Bots's choice:", 100, 270, 2.5)
        frame = draw_gesture(frame, choice_bot, 150, 270)  
        winner = check_winner(choice_bot, choice_player)
        draw_text(f"Press 'R' to restart", 430, 650, 2.7)
        if winner == 'player':
            draw_text(f'You won!'.center(51), -120, 150, 3.5, GREEN)
        elif winner == 'bot':
            draw_text(f'You lost...'.center(51), -110, 150, 3.5, RED)
        elif winner == 'draw':
            draw_text(f'Draw'.center(51), -120, 150, 3.5, ORANGE)
        else:
            draw_text(f'You did not have a gesture up...'.center(51), -120, 150, 3.5, RED)

    # Update frame
    cv.imshow('Rock Paper Scissors', cv.cvtColor(frame, cv.COLOR_RGB2BGR))
    
    # Handle keys
    key = cv.waitKey(1) 
    if key == ord('r'): # r key to restart
        time_left = WAIT_TIME
        choice_bot = ['rock', 'paper', 'scissors'][randint(0, 2)]
    elif  key == 27: # 27 = escape key
        cv.destroyAllWindows()
        break # exit script