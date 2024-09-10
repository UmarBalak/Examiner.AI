import cv2
import streamlit as st
import time
from functions2 import *

st.set_page_config(
    page_title="Examiner.AI",
    page_icon=":camera:",
    initial_sidebar_state="expanded",
)

# Custom CSS to style buttons, text, layout, and metric cards
st.markdown("""
    <style>
        .main-title {
            font-size: 36px;
            font-weight: bold;
            color: #FFFFFF;
            text-align: center;
            margin-bottom: 30px;
        }
        .subheader {
            font-size: 24px;
            font-weight: bold;
            color: #2E8B57;
        }
        .camera-status {
            font-size: 18px;
            font-weight: bold;
            color: #32CD32;
        }
        .stButton>button {
            background-color: #007acc;
            color: white;
            font-size: 16px;
            border-radius: 8px;
            margin-top: 20px;
        }
        .stButton>button:hover {
            background-color: #005f99;
            color: white;
        }
        .streamlit-container {
            padding: 20px;
        }
        .metric-card {
            background-color: #007acc;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
            color: white;
            text-align: center;
            font-family: Arial, sans-serif;
        }
        .metric-card h2 {
            font-size: 18px;
            margin-bottom: 10px;
            font-weight: bold;
        }
        .metric-card p {
            font-size: 26px;
            margin: 0;
            font-weight: bold;
        }
        .metric-card span {
            font-size: 14px;
            margin-top: 5px;
            display: block;
            color: #f0f0f0;
        }
        .fps-card {
            background-color: #28a745;  /* Green for FPS */
        }
        .eye-card {
            background-color: #17a2b8;  /* Light blue for Eye Direction */
        }
        .head-card {
            background-color: #ffc107;  /* Yellow for Head Direction */
        }
        .obj-card {
            background-color: #dc3545;  /* Red for Background Status */
        }
    </style>
""", unsafe_allow_html=True)

# Initialize the camera
camera = cv2.VideoCapture(0)

def process_frame(camera):
    # Call the function that processes the video feed and returns metrics
    result, eye_d, head_d, fps, obj_d = run(camera)
    return result, eye_d, head_d, fps, obj_d

def main():
    st.markdown("<h1 class='main-title'>Real-Time Proctoring System</h1>", unsafe_allow_html=True)

    # Sidebar for camera control buttons
    with st.sidebar:
        st.header("Controls")
        start_button = st.button("Start Camera")
        stop_button = st.button("Stop Camera")

    st.markdown("<h3 class='subheader'>Live Video Feed</h3>", unsafe_allow_html=True)
    
    # Placeholder for video feed with reduced height
    FRAME_WINDOW = st.image([])  # Placeholder for the video feed

    st.markdown("<h3 class='subheader'>Real-Time Metrics</h3>", unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns([1, 1, 1, 1])
    # Create placeholders for real-time metrics using the card-based UI
    with c1:
        fps_placeholder = st.empty()
    with c2:
        eye_placeholder = st.empty()
    with c3:
        head_placeholder = st.empty()
    with c4:
        obj_placeholder = st.empty()

    # If the start button is pressed
    if start_button:
        st.markdown("<p class='camera-status'>Camera is active. Press 'Stop Camera' to stop.</p>", unsafe_allow_html=True)
        prev_time = time.time()

        while camera.isOpened():
            ret, frame = camera.read()

            if not ret:
                st.error("Failed to capture video. Check your camera connection.")
                break

            # Check if the frame is valid before processing
            if frame is not None:
                # Calculate frame rate
                current_time = time.time()
                elapsed_time = current_time - prev_time
                fps = 1 / elapsed_time if elapsed_time > 0 else 0
                prev_time = current_time

                # Convert the frame to RGB for displaying
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame_rgb = cv2.flip(frame_rgb, 1)

                # Resize the frame to reduce height (adjust width to maintain aspect ratio)
                frame_rgb = cv2.resize(frame_rgb, (int(frame_rgb.shape[1] * 1.0), int(frame_rgb.shape[0] * 0.75)))

                # Only display the frame if it's valid
                if frame_rgb is not None:
                    FRAME_WINDOW.image(frame_rgb, caption="Live Feed", use_column_width=False)

                    # Process frame metrics
                    result, eye_d, head_d, fps, obj_d = process_frame(camera)

                    if eye_d is not None:
                        # Update real-time metrics with card-based UI
                        fps_placeholder.markdown(f"""
                            <div class="metric-card fps-card">
                                <h2>FPS</h2>
                                <p>{fps:.2f}</p>
                            </div>
                        """, unsafe_allow_html=True)

                        eye_placeholder.markdown(f"""
                            <div class="metric-card eye-card">
                                <h2>Eye Direction</h2>
                                <p>{eye_d}</p>
                            </div>
                        """, unsafe_allow_html=True)

                        head_placeholder.markdown(f"""
                            <div class="metric-card head-card">
                                <h2>Head Direction</h2>
                                <p>{head_d}</p>
                            </div>
                        """, unsafe_allow_html=True)

                        obj_placeholder.markdown(f"""
                            <div class="metric-card obj-card">
                                <h2>Background</h2>
                                <p>{"Ok" if obj_d else "Object detected"}</p>
                            </div>
                        """, unsafe_allow_html=True)
                else:
                    st.error("Invalid frame detected, skipping frame display.")
            else:
                st.error("No frame captured from the camera.")

            # Stop if the stop button is pressed
            if stop_button:
                st.warning("Camera stopped.")
                break

            # Add a short delay to reduce CPU usage
            time.sleep(0.01)

    # Cleanup resources
    camera.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
