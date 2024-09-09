import streamlit as st
import cv2
import pyautogui
from functions import *
import numpy as np

# Set up camera and session state
if 'camera' not in st.session_state:
    st.session_state.camera = cv2.VideoCapture(0)
    st.session_state.count = 0
    st.session_state.last_warning = True
    st.session_state.frame = None

# Streamlit app title
st.title("AI Proctored Exam System")

# Function to capture and save frames and screenshots
def capture_images(count):
    ret, frame = st.session_state.camera.read()
    if ret:
        cv2.imwrite(f"image{count}.jpg", frame)
        screenshot = pyautogui.screenshot()
        screenshot.save(f"ss{count}.jpg")
        return frame, screenshot
    return None, None

# Displaying captured images
if st.session_state.frame is not None:
    st.image(st.session_state.frame, channels="BGR", caption="Current Frame")

# Button to start the exam system
if st.button("Start Exam Monitoring"):
    while True:
        result = run(st.session_state.camera)  # Call the AI model for result
        st.write(f"Monitoring result: {result}")

        if not result:
            st.session_state.count += 1
            frame, screenshot = capture_images(st.session_state.count)

            # Display captured images
            if frame is not None:
                st.image(frame, channels="BGR", caption=f"Captured Image {st.session_state.count}")
                st.image(np.array(screenshot), caption=f"Screenshot {st.session_state.count}")

            # Handle warnings and actions
            if st.session_state.count == 3 and st.session_state.last_warning:
                speak("This is the last warning, After this, your exam will be terminated")
                st.warning("Last Warning: Your exam will be terminated after the next violation.")
                st.session_state.last_warning = False

            if st.session_state.count == 4:
                st.error("Exam Terminated!")
                speak("Exam Terminated.")
                st.session_state.camera.release()
                break

# Clean up when the app is stopped
if st.button("Stop Monitoring"):
    st.session_state.camera.release()
    st.write("Camera stopped.")
