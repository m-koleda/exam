from time import sleep


print("CHECK REQUIRED FIELDS IN CONFIG.YAML... \n ")

f = open('config.yaml', mode='r')
file = f.read()
if "use: 'centos'" in file:
    sleep(1)
    print("check 'use' - type of OS...")
#    sleep(1)
    print("...ok. use: CentOS")
elif "use: 'ubuntu'" in file:
    print("check 'use' - type of OS...")
#    sleep(1)
    print("...ok. use: Ubuntu")
else:
    print("ERROR IN CONFIG.YAML FILE: incorrect OS")
    raise ValueError()
if "playbook:" in file:
    print("check playbook...")
#    sleep(1)
    print("...ok")
else:
    raise ValueError()
if "public_ip:" in file:
    print("check public_ip...")
#    sleep(1)
    print("...ok")
else:
    raise ValueError() 

print("CHECK REQUIRED FIELDS IN JENKINSFILE... \n ")

f = open('Jenkinsfile', mode='r')
file = f.read()
if "sh 'python3 test.py'" in file:
    print("check for presence of test.py")
#    sleep(1)
    print("...ok")
else:
    raise ValueError()
if "sh 'vagrant up --provision'" in file:
    print("check right Vagrant command...")
#    sleep(1)
    print("...ok")
else:
    raise ValueError()

print("CHECK REQUIRED FIELDS IN VAGRANTFILE... \n ")

f = open('Vagrantfile', mode='r')
file = f.read()
if 'configs        = YAML.load_file("#{current_dir}/config.yaml")' in file:
    print("check link for config.yaml")
#    sleep(1)
    print("...ok")
else:
    raise ValueError()
if "vagrant_config['box']" in file:
    print("check for presence of boxes name ...")
#    sleep(1)
    print("...ok")
else:
    raise ValueError()
if 'machine.vm.network "public_network", bridge: "enp1s0"' in file:
    print("check for public network and bridge ...")
#    sleep(1)
    print("...ok")
else:
    raise ValueError()

print("TEST STAGE OK") 
