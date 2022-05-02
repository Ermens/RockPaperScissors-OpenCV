# RockPaperScissor-OpenCV

This is a simple rock paper scissor game, made using python, OpenCV and mediapipe for hand-tracking.

This contains a HandTrackingModule which makes working with hand-tracking easy, it has methods - findHands to track hands, findPosition to get coordinates i.e. hand landmarks for all 21 points that mediapipe offers for a hand, and a fingersUp method that returns how many fingers are currently open. 

The fingersUp method is used to know whether the player has played rock, paper or scissor - rock for 0 fingers open, scissor for 2 fingers open and paper for all five fingers open.

https://user-images.githubusercontent.com/85190369/166179806-76b8cf07-1dcf-4515-a1fc-24aec34b4147.mov



There is a red area on the player side and only when the player shows his move inside the area, it is considered a move. There is a timer which tells when the computer will play its move, it resets after every 4 seconds and after the player has played his move, if the timer hits 0 before the player's move, it will wait for the player to play. The computer will play when the timer hits 0 and the player move is detected.

Scores for both player and computer are shown below their sides.


https://user-images.githubusercontent.com/85190369/166187639-29a0289c-ec05-4840-819f-beef6bdbec24.mp4


For accurately showcasing your move, don't wait for the timer to hit 0 to play your move, be ready with your move in the red area before the timer hits 0.

There is no end condition for the game, you can play it for as long as you want.


https://user-images.githubusercontent.com/85190369/166200684-2fadb07c-d409-4885-a150-6b7abb430d3a.mp4

