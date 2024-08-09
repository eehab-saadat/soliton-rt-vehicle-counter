import threading 
from streamlit.runtime.scriptrunner import add_script_run_ctx
from streamlit.runtime.scriptrunner.script_run_context import get_script_run_ctx
from streamlit.runtime import get_instance
import datetime
from utils.input import load_instance
from new_app import main
def start_beating(status: bool):
    thread = threading.Thread(target=start_beating, args=(False,))

    add_script_run_ctx(thread) 
    ctx = get_script_run_ctx()     
    runtime = get_instance()     # this is the main runtime, contains all the sessions

    if runtime.is_active_session(session_id=ctx.session_id):
        # Session is running
        thread.start()
        if status:
            main(None)
    else:
        load_instance().stop_all()
        print("Session stopped")
        # Session is not running, Do what you want to do on user exit here
        return
    
if __name__ == "__main__":
    start_beating(True)