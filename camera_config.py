import subprocess, sys

def usbKill():
    ## kill hold on camera storage. Camera must not be plugged in yet
    ## Investigate further
    #http://www.awesomeprojects.xyz/2015/08/how-to-use-old-usb-digital-camera-as.html
    subprocess.call("sudo killall gvfs-gphoto2-volume-monitor", shell=True)

def targetCard():
    # set download location to be memory card
    # do not use sudo
    subprocess.call("gphoto2 --set-config-value /main/settings/capturetarget=1", shell=True)
    subprocess.call("gphoto2 --set-config capturetarget=\"Memory card\"", shell=True)
    # http://gphoto-software.10949.n7.nabble.com/Setting-capturetarget-to-card-not-working-td13613.html

def main():
    while True:
        print "\n-- OPTIONS\n1. Clear USB Permissions\n2. Set capture target to memory card\n0. Exit\n"
        menu_select = raw_input(" >> ")
        if menu_select == '1':
            usbKill()
        if menu_select == '2':
            targetCard()
        if menu_select == '0':
            sys.exit()
        else:
            continue

if __name__ == "__main__":
    main()
