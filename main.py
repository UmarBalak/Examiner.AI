from functions import *
import pyautogui

camera = cv2.VideoCapture(0)
ret, frame = camera.read()
count = 0
last_warning = True
while True:
    result = run(camera)
    print(result)
    if not result:
        count += 1
    if count == 1:
        ret, frame = camera.read()
        cv2.imwrite("image1.jpg", frame)
        pyautogui.screenshot().save("ss1.jpg")
    elif count == 2:
        ret, frame = camera.read()
        cv2.imwrite("image2.jpg", frame)
        pyautogui.screenshot().save("ss.jpg")
    elif  count == 4:
        ret, frame = camera.read()
        cv2.imwrite("image4.jpg", frame)
        pyautogui.screenshot().save("ss4.jpg")
        break
    elif count == 3:
        ret, frame = camera.read()
        cv2.imwrite("image3.jpg", frame)
        pyautogui.screenshot().save("ss3.jpg")
        if last_warning:
            speak("This is the last warning, After this, your exam will be terminated")
            last_warning = False


# camera.release()
# cv2.destroyAllWindows()