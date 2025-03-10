import frida
import sys

pathToBeCloselyExamined = [
    "/data/user/0/",
    "/data/app/"
]

focus_color = '\033[93m'
normal_color = '\033[36m'

init_color = '\033[0m'
bold_color = '\033[1m'

def is_target_path(path):
    return any(path.startswith(prefix) for prefix in pathToBeCloselyExamined)

def on_message(message, data):
    if message["type"] == "send":
        path = str(message["payload"])
        print('[*] Attempt to open a file ({0}open={1}{2}{3})'.format(bold_color, focus_color if is_target_path(path) else normal_color, path, init_color))
    else:
        print(message)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python sample.py \"package_name\"")
        sys.exit(1)
    package_name = sys.argv[1]
    device = frida.get_usb_device()
    pid = device.spawn([package_name])
    session = device.attach(pid)

    with open("hook.js", "r") as f:
        script = session.create_script(f.read())

    script.on("message", on_message)
    script.load()
    device.resume(pid)
    sys.stdin.read()
