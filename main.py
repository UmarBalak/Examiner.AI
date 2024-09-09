import pyautogui
from functions import *

camera = cv2.VideoCapture(0)
count = 0
last_warning = True

def save_image_and_screenshot(image_name, screenshot_name):
    ret, frame = camera.read()
    if ret:
        cv2.imwrite(image_name, frame)
        pyautogui.screenshot().save(screenshot_name)
    else:
        print("Error: Unable to capture image from camera")

while True:
    result, to_speak = run(camera)
    print(result)
    
    if not result:
        count += 1
        save_image_and_screenshot(f"image{count}.jpg", f"ss{count}.jpg")
        speak(to_speak)

    if count == 3:
        if last_warning:
            speak("This is the last warning. After this, your exam will be terminated")
            last_warning = False
    elif count == 4:
        break

# Cleanup camera resources
camera.release()
cv2.destroyAllWindows()
