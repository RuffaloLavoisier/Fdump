import frida
import sys

focus_path = [
    "/data/user/0/",
    "/data/app/"
]

color_focus = '\033[93m'
color_normal = '\033[36m'

color_init = '\033[0m'
color_bold = '\033[1m'

def is_target_path(path):
    return any(path.startswith(prefix) for prefix in focus_path)

def on_message(message, data):
    if message["type"] == "send":
        path = str(message["payload"])
        print('[*] Attempt to open a file ({0}open={1}{2}{3})'.format(
            color_bold, color_focus if is_target_path(path) else color_normal, path, color_init))
    else:
        print(message)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: python {sys.argv[0]} \"package_name\"")
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
