from utils.onlycams import list_hot_cameras_on_my_device

def handle_camera_stream() -> None:
    all_cams = list_hot_cameras_on_my_device()
    # model.count(source=all_cams[st.session_state.selected_cam], skip=2, region_points=linear_points)
    print(all_cams)