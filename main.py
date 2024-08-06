import streamlit as st
from cv2.typing import MatLike
from cv2 import VideoCapture, CAP_PROP_FRAME_WIDTH, CAP_PROP_FRAME_HEIGHT, waitKey, destroyAllWindows


@st.fragment
def updateFrame(frame: MatLike):
    with st.session_state.main_pane[1]:
        # print(st.session_state.main_pane_cols)
        # st.session_state.frame_bucket.image(frame, channels="BGR")
        st.write("Frame updated")

def count(capture: VideoCapture = VideoCapture(0), resolution: tuple = (1280, 720)) -> None:
            frame_width, frame_height = resolution
            # source = source if source != "0" else 0
            # capture = VideoCapture(source)
            capture.set(CAP_PROP_FRAME_WIDTH, frame_width)
            capture.set(CAP_PROP_FRAME_HEIGHT, frame_height)

            while capture.isOpened():
                success, im0 = capture.read()
                if not success:
                    break

                # update the frame in session state
                updateFrame(im0)

                if waitKey(1) == ord('q'):
                    break

            capture.release()
            destroyAllWindows()