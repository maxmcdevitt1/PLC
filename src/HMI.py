from time import sleep
from threading import Thread, Lock
from flask import Flask, jsonify

from plc_client import Plc


app = Flask(__name__)

latest_status = {
    "connected": False,
    "machine_state": "STARTING",
    "error": None,
}

status_lock = Lock()


def update_status(new_status):
    global latest_status

    with status_lock:
        latest_status = new_status


def get_latest_status():
    with status_lock:
        return latest_status.copy()


def plc_poll_loop():
    plc = Plc()

    while True:
        try:
            if not plc.connect():
                update_status({
                    "connected": False,
                    "machine_state": "PLC CONNECTION FAILED",
                    "error": "Could not connect to PLC",
                })

                sleep(1)
                continue

            while True:
                status = plc.read_status()
                status["connected"] = True
                status["error"] = None

                update_status(status)

                sleep(1)

        except Exception as error:
            update_status({
                "connected": False,
                "machine_state": "PLC COMMUNICATION ERROR",
                "error": str(error),
            })

            plc.close()
            sleep(1)


@app.route("/")
def index():
    return "PLC HMI backend is running."


@app.route("/api/status")
def api_status():
    return jsonify(get_latest_status())


if __name__ == "__main__":
    poll_thread = Thread(target=plc_poll_loop, daemon=True)
    poll_thread.start()

    app.run(host="0.0.0.0", port=5000)