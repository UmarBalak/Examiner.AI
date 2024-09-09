import streamlit as st
import pyautogui
import cv2
from functions import *  # Ensure these functions are available

# Streamlit App Title
st.title("Exam Monitoring System")

# Initialize Camera
camera = cv2.VideoCapture(0)
if not camera.isOpened():
    st.error("Error: Could not open camera.")
    st.stop()  # Stop execution if the camera is not available

# A flag to control when the monitoring should stop
stop_monitoring_flag = st.button("Stop Monitoring")


def save_image_and_screenshot(count):
    """Helper function to save images and screenshots."""
    ret, frame = camera.read()
    if ret:
        img_filename = f"image{count}.jpg"
        ss_filename = f"ss{count}.jpg"
        
        # Save the camera frame and a screenshot of the desktop
        cv2.imwrite(img_filename, frame)
        pyautogui.screenshot().save(ss_filename)

        return img_filename, ss_filename
    else:
        st.error("Error: Unable to capture image from camera")
        return None, None


# Main monitoring function
def monitor():
    count = 0
    last_warning = True
    captured_images = []
    captured_screenshots = []
    
    result_placeholder = st.empty()

    while True:
        # Check if the user clicked the "Stop Monitoring" button
        if stop_monitoring_flag:
            st.write("Monitoring manually stopped by user.")
            break

        result, to_speak = run(camera)  # Assume run returns True/False based on monitoring logic
        result_placeholder.write(f"Run result: {result}")  # Updates in the same spot
        
        if not result:
            count += 1
            img, ss = save_image_and_screenshot(count)
            speak(to_speak)
            if img and ss:
                captured_images.append(img)
                captured_screenshots.append(ss)
            
            # Issue the warning at count 3 and terminate at count 4
            if count == 3 and last_warning:
                speak("This is the last warning. After this, your exam will be terminated.")
                st.warning("This is the last warning. After this, your exam will be terminated.")
                last_warning = False
            elif count == 4:
                st.write("Monitoring stopped after 4 warnings.")
                break

    # Release the camera after monitoring
    camera.release()
    cv2.destroyAllWindows()

    # Display captured images and screenshots after monitoring
    if captured_images and captured_screenshots:
        st.subheader("Captured Images and Screenshots:")
        for i in range(len(captured_images)):
            st.image(captured_images[i], caption=f"Captured Image {i + 1}")
            st.image(captured_screenshots[i], caption=f"Screenshot {i + 1}")


# Button to start the monitoring process
if st.button("Start Monitoring"):
    monitor()

# Display closing message
st.write("Ready to monitor.")
