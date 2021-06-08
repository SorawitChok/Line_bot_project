import cv2 
import numpy as np

screen = cv2.imread('/home/sorawitchok/Line_bot_project/static/screen_state/screen.png')
login_check = cv2.imread('/home/sorawitchok/Line_bot_project/static/resource/login.png')
chat_check = cv2.imread('/home/sorawitchok/Line_bot_project/static/resource/chat.png')
friend_check = cv2.imread('/home/sorawitchok/Line_bot_project/static/resource/friend.png')
add_friend_check = cv2.imread('/home/sorawitchok/Line_bot_project/static/resource/add_friend.png')

state = 'None'

result = cv2.matchTemplate(login_check,screen,cv2.TM_SQDIFF)

H,W = np.unravel_index(result.argmax(),result.shape)
h,w,c = login_check.shape
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
h1 , w1 = min_loc

if min_val < 0.000000000000001:
    state = 'login'
else:
    pass

result = cv2.matchTemplate(chat_check,screen,cv2.TM_SQDIFF)

H,W = np.unravel_index(result.argmax(),result.shape)
h,w,c = login_check.shape
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
h1 , w1 = min_loc

if min_val < 0.000000000000001:
    state = 'chat'
else:
    pass

result = cv2.matchTemplate(friend_check,screen,cv2.TM_SQDIFF)

H,W = np.unravel_index(result.argmax(),result.shape)
h,w,c = login_check.shape
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
h1 , w1 = min_loc

if min_val < 0.000000000000001:
    state = 'friend'
else:
    pass

result = cv2.matchTemplate(add_friend_check,screen,cv2.TM_SQDIFF)

H,W = np.unravel_index(result.argmax(),result.shape)
h,w,c = login_check.shape
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
h1 , w1 = min_loc

if min_val < 0.000000000000001:
    state = 'add friend'
else:
    pass

print(state)
