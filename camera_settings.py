import subprocess

# set download location to be memory card
def set_target_card():
    # do not use sudo
    subprocess.call("gphoto2 --set-config-value /main/settings/capturetarget=1", shell=True)
    subprocess.call("gphoto2 --set-config capturetarget=\"Memory card\"", shell=True)

# get the current config for the specified setting
def get_config(config):
    child = subprocess.Popen(["gphoto2", "--get-config="+config], stdout=subprocess.PIPE)
    results = child.communicate()[0].split("\n")
    return results[2].split(" ")[-1]

# set the current config for the specified setting
def set_config(config, setting):
    to_call = 'gphoto2 --set-config {}={}'.format(config, setting)
    subprocess.call(to_call, shell=True)

# get a list of possible options for the specified setting
def get_options(config):
    child = subprocess.Popen(["gphoto2", "--get-config="+config], stdout=subprocess.PIPE)
    trunc_results = child.communicate()[0].split("\n")[3:]
    results = [ opt.split(" ")[-1] for opt in trunc_results if opt != '' ]
    return results
