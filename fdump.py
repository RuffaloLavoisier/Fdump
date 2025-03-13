import frida
import sys

focus_path = [
    "/data/user/0/",
    "/data/app/"
]

target_path = [
    "/data/user/0/",
    "/data/app/",
    "/system/"
]

color_focus = '\033[93m'
color_normal = '\033[36m'

color_init = '\033[0m'
color_bold = '\033[1m'

# Check if the path is in the focus_path
def is_focus_path(path):
    return any(path.startswith(prefix) for prefix in focus_path)

# Check if the path is in the target_path
def is_target_path(path):
    return any(path.startswith(prefix) for prefix in target_path)

def on_message(message, data):
    if message["type"] == "send":
        path = str(message["payload"])
        # Check if the path is in the target_path (E.g., /data/user/0/ or /data/app/ it will print it, if the target_path is empty, it will print all the paths)
        if is_target_path(path) or len(target_path) == 0:
            print('[*] Attempt to open a file ({0}open={1}{2}{3})'.format(
                color_bold, color_focus if is_focus_path(path) else color_normal, path, color_init))
    else:
        print(message)

def printLogo():
    print(r'''
 ________              ________  ___  ___  _____ ______   ________   
|\  _____\            |\   ___ \|\  \|\  \|\   _ \  _   \|\   __  \  
\ \  \__/ ____________\ \  \_|\ \ \  \\\  \ \  \\\__\ \  \ \  \|\  \ 
 \ \   __\\____________\ \  \ \\ \ \  \\\  \ \  \\|__| \  \ \   ____\
  \ \  \_\|____________|\ \  \_\\ \ \  \\\  \ \  \    \ \  \ \  \___|
   \ \__\                \ \_______\ \_______\ \__\    \ \__\ \__\   
    \|__|                 \|_______|\|_______|\|__|     \|__|\|__|   
          

    * Author: Ruffalo Lavoisier (https://github.com/RuffaloLavoisier)
    * Version: 1.0.0''')
    print();
if __name__ == "__main__":
    printLogo()
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
