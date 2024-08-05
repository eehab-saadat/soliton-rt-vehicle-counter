from streamlit import dialog, header, write, rerun, fragment
from time import sleep

@fragment
@dialog(title="System Message")
def showDialogBox(icon: any = "⚠️", heading: str = "Warning", message: str = "some error occurred. Please try again."):
    header(icon + " " + heading)
    write(message)