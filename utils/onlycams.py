from cv2_enumerate_cameras import enumerate_cameras

def list_hot_cameras_on_my_device():
    devices = {}
    index = 0
    for camera in enumerate_cameras():
        if camera.name not in list(devices.keys()):
            devices[camera.name] = index
            index += 1
        else:
            continue
    return devices

if __name__ == "__main__":
    print(list_hot_cameras_on_my_device())