# Final project at itstep.by

# Jenkins + Vagrant + Ansible for Wordpress LAMP on Ubuntu 18.04 LTS or CentOS 7

There are too many Jenkins+Ansible+Terraform for any cloud tutorials and not many for Jenkins+Vagrant+Ansible with create VM on local machine, so I wanted to understand how to do it.  
By this tutorial you can up an Ubuntu 18.04 or CentOS 7 virtual machine and install a LAMP environment (**L**inux, **A**pache, **M**ySQL and **P**HP), Wordpress and copy site from dir site to VMs. Machines will auto-create by Vagrant and will configuare by Ansible. 
You must choose an OS and playbook for run VM and delivery code or just delivery code in the `config.yaml` file.  
A virtualhost will be created with the options specified in the `vars/default.yml` variable file.  

## Settings  

- `mysql_root_password`: the password for the MySQL root account.
- `app_user`: a remote non-root user on the Ansible host that will own the application files.
- `http_host`: your domain name.
- `http_conf`: the name of the configuration file that will be created within Apache.
- `http_port`: HTTP port, default is 80.
- `disable_default`: whether or not to disable the default Apache website. When set to true, your new virtualhost should be used as default website. Default is true.

## Prerequisites  

To follow this tutorial, you will need:  

One Ubuntu 22.04 server with installed:
- Virtualbox 6.1.32  
- Vagrant 2.3.4 with vbguest plugin
- Jenkins 2.375.2 (running as standart user, not jenkins - it's need)

### 1. Customize Options in vars/default.yml

```shell
nano vars/default.yml
```

```yml
---
mysql_root_password: "mysql_root_password"
app_user: "sam"
http_host: "your_domain"
http_conf: "your_domain.conf"
http_port: "80"
disable_default: true
```

### 2. Customize Options in config.yaml

```shell
nano config.yaml
```
For first build with creating VM in Jenkins use playbook--startvm.yml
For another build use playbook--cd.yml

### 3. Create Pipelines in Jenkins 

Create Pipelines for every branch you have in git-repository:
- Build Triggers: Poll SCM Schedule: H/2 * * * * - for schedule every 2 minutes
- Pipeline script from SCM: Git 
- Script Path: Jenkinsfile


Jenkins master first build output:  

    Started by an SCM change
    Obtained Jenkinsfile from git https://github.com/m-koleda/exam.git
    [Pipeline] Start of Pipeline
    [Pipeline] node
    Running on Jenkins in /var/lib/jenkins/workspace/exam-master-branch
    [Pipeline] {
    [Pipeline] stage
    [Pipeline] { (Declarative: Checkout SCM)
    [Pipeline] checkout
    Selected Git installation does not exist. Using Default
    The recommended git tool is: NONE
    No credentials specified
     > git rev-parse --resolve-git-dir /var/lib/jenkins/workspace/exam-master-branch/.git # timeout=10
    Fetching changes from the remote Git repository
     > git config remote.origin.url https://github.com/m-koleda/exam.git # timeout=10
    Fetching upstream changes from https://github.com/m-koleda/exam.git
     > git --version # timeout=10
     > git --version # 'git version 2.34.1'
     > git fetch --tags --force --progress -- https://github.com/m-koleda/exam.git +refs/heads/*:refs/remotes/origin/* # timeout=10
     > git rev-parse refs/remotes/origin/master^{commit} # timeout=10
    Checking out Revision 0d522999ce365e16395e94c859d0ab4de50600e1 (refs/remotes/origin/master)
     > git config core.sparsecheckout # timeout=10
     > git checkout -f 0d522999ce365e16395e94c859d0ab4de50600e1 # timeout=10
    Commit message: "update config.yaml"
     > git rev-list --no-walk 730b7e722bd378b79539f4a1aec5811ea76bd5bf # timeout=10
    [Pipeline] }
    [Pipeline] // stage
    [Pipeline] withEnv
    [Pipeline] {
    [Pipeline] stage
    [Pipeline] { (Build)
    [Pipeline] sh
    + echo BUILDING...
    BUILDING...
    [Pipeline] sh
    + echo BUILD ID - 8
    BUILD ID - 8
    [Pipeline] sh
    + echo BUILD STAGE OK
    BUILD STAGE OK
    [Pipeline] }
    [Pipeline] // stage
    [Pipeline] stage
    [Pipeline] { (Test)
    [Pipeline] sh
    + echo TESTING...
    TESTING...
    [Pipeline] sh
    + python3 test.py
    CHECK REQUIRED FIELDS IN CONFIG.YAML... 

    check 'use' - type of OS...
    ...ok. use: CentOS
    check playbook...
    ...ok
    check public_ip...
    ...ok
    CHECK REQUIRED FIELDS IN JENKINSFILE... 

    check for presence of test.py
    ...ok
    check right Vagrant command...
    ...ok
    CHECK REQUIRED FIELDS IN VAGRANTFILE... 

    check link for config.yaml
    ...ok
    check for presence of boxes name ...
    ...ok
    check for public network and bridge ...
    ...ok
    TEST STAGE OK
    [Pipeline] }
    [Pipeline] // stage
    [Pipeline] stage
    [Pipeline] { (Deploy)
    [Pipeline] sh
    + echo DEPLOYING...
    DEPLOYING...
    [Pipeline] sh
    + vagrant up --provision
    Bringing machine 'consul-server' up with 'virtualbox' provider...
    ==> consul-server: Importing base box 'centos/7'...

    [KProgress: 20%
    [KProgress: 40%
    [KProgress: 70%
    [KProgress: 90%
    [K==> consul-server: Matching MAC address for NAT networking...
    ==> consul-server: Checking if box 'centos/7' version '2004.01' is up to date...
    ==> consul-server: Setting the name of the VM: exam-master-branch_consul-server_1674994591202_1837
    ==> consul-server: Clearing any previously set network interfaces...
    ==> consul-server: Preparing network interfaces based on configuration...
        consul-server: Adapter 1: nat
        consul-server: Adapter 2: bridged
    ==> consul-server: Forwarding ports...
        consul-server: 22 (guest) => 2222 (host) (adapter 1)
    ==> consul-server: Booting VM...
    ==> consul-server: Waiting for machine to boot. This may take a few minutes...
        consul-server: SSH address: 127.0.0.1:2222
        consul-server: SSH username: vagrant
        consul-server: SSH auth method: private key
        consul-server: 
        consul-server: Vagrant insecure key detected. Vagrant will automatically replace
        consul-server: this with a newly generated keypair for better security.
        consul-server: 
        consul-server: Inserting generated public key within guest...
        consul-server: Removing insecure key from the guest if it's present...
        consul-server: Key inserted! Disconnecting and reconnecting using new SSH key...
    ==> consul-server: Machine booted and ready!
    ==> consul-server: Checking for guest additions in VM...
        consul-server: No guest additions were detected on the base box for this VM! Guest
        consul-server: additions are required for forwarded ports, shared folders, host only
        consul-server: networking, and more. If SSH fails on this machine, please install
        consul-server: the guest additions and repackage the box to continue.
        consul-server: 
        consul-server: This is not an error message; everything may continue to work properly,
        consul-server: in which case you may ignore this message.
    ==> consul-server: Configuring and enabling network interfaces...
    ==> consul-server: Rsyncing folder: /var/lib/jenkins/workspace/exam-master-branch/ => /vagrant
    ==> consul-server: Running provisioner: ansible...
        consul-server: Running ansible-playbook...
    PYTHONUNBUFFERED=1 ANSIBLE_NOCOLOR=true ANSIBLE_HOST_KEY_CHECKING=false ANSIBLE_SSH_ARGS='-o UserKnownHostsFile=/dev/null -o IdentitiesOnly=yes -o ControlMaster=auto -o ControlPersist=60s' ansible-playbook --connection=ssh --timeout=30 --limit="consul-server" --inventory-file=/var/lib/jenkins/workspace/exam-master-branch/.vagrant/provisioners/ansible/inventory -v playbook-centos-startvm.yml
    No config file found; using defaults

    PLAY [all] *********************************************************************

    TASK [Gathering Facts] *********************************************************
    ok: [consul-server]

    TASK [Update ca-certificates before importing the GPG Key] *********************
    changed: [consul-server] => {"changed": true, "changes": {"installed": [], "updated": [["ca-certificates", "2022.2.54-74.el7_9.noarch from updates"]]}, "msg": "warning: /var/cache/yum/x86_64/7/updates/packages/ca-certificates-2022.2.54-74.el7_9.noarch.rpm: ................

    TASK [Import Remi2018 and Webtatic GPG key] ************************************
    changed: [consul-server] => (item=https://mirror.webtatic.com/yum/RPM-GPG-KEY-webtatic-el7) => {"ansible_loop_var": "item", "changed": true, "item": "https://mirror.webtatic.com/yum/RPM-GPG-KEY-webtatic-el7"}
    changed: [consul-server] => (item=https://rpms.remirepo.net/RPM-GPG-KEY-remi2017) => {"ansible_loop_var": "item", "changed": true, "item": "https://rpms.remirepo.net/RPM-GPG-KEY-remi2017"}

    TASK [Install Remi and Webtatic repos] *****************************************
    changed: [consul-server] => (item=https://mirror.webtatic.com/yum/el7/webtatic-release.rpm) => {"ansible_loop_var": "item", "changed": true, "changes": {"installed": ["/home/vagrant/.ansible/tmp/ansible-tmp-1674994647.8148553-11568-254282429824743/webtatic-releasefKZ2Y7.rpm"]}, "item": "https://mirror.webtatic.com/yum/el7/webtatic-release.rpm", ................

    TASK [Install LAMP Packages] ***************************************************
    changed: [consul-server] => (item=httpd) => {"ansible_loop_var": "item", "changed": true, "changes": {"installed": ["httpd"], "updated": []}, "item": "httpd", "msg": "", "rc": 0, "results": ["Loaded plugins: fastestmirror\nLoading mirror speeds from cached ................       \n\nComplete!\n"]}

    TASK [Install the mariadb] *****************************************************
    changed: [consul-server] => {"changed": true, "changes": {"installed": ["mariadb-server", "MySQL-python"]}, "msg": "", ................  \n\nComplete!\n"]}

    TASK [Restarting mariadb pacakage] *********************************************
    changed: [consul-server] => {"changed": true, "enabled": true, "name": "mariadb", "state": "started", "status": {"ActiveEnterTimestampMonotonic": "0", "ActiveExitTimestampMonotonic": "0", "ActiveState": "inactive", "After": "syslog.target system.slice network.target ................

    TASK [Create document root] ****************************************************
    changed: [consul-server] => {"changed": true, "gid": 48, "group": "apache", "mode": "0755", "owner": "apache", "path": "/var/www/test.local", "secontext": "unconfined_u:object_r:httpd_sys_content_t:s0", "size": 6, "state": "directory", "uid": 48}

    TASK [Set up Apache VirtualHost] ***********************************************
    changed: [consul-server] => {"changed": true, "checksum": "c98b3bd1174f774b43fef3ef137fea6bccfd0d6c", "dest": "/etc/httpd/conf.d/test.local.conf", "gid": 0, "group": "root", "md5sum": "a30b622ae27adbbc51eb474832b7f542", "mode": "0644", "owner": "root", "secontext": "system_u:object_r:httpd_config_t:s0", "size": 498, "src": "/home/vagrant/.ansible/tmp/ansible-tmp-1674994823.5333807-11877-152370369136318/source", "state": "file", "uid": 0}

    TASK [mariadb - Setting RootPassword] ******************************************
    changed: [consul-server] => {"changed": true, "msg": "Password updated (old style)", "user": "root"}

    TASK [Remove all anonymous user accounts] **************************************
    changed: [consul-server] => {"changed": true, "msg": "User deleted", "user": ""}

    TASK [Remove the MySQL test database] ******************************************
    changed: [consul-server] => {"changed": true, "db": "test", "db_list": ["test"], "executed_commands": ["DROP DATABASE `test`"]}

    TASK [Creates database for WordPress] ******************************************
    changed: [consul-server] => {"changed": true, "db": "wordpress", "db_list": ["wordpress"], "executed_commands": ["CREATE DATABASE `wordpress`"]}

    TASK [Create MySQL user for WordPress] *****************************************
    changed: [consul-server] => {"changed": true, "msg": "User added", "user": "sammy"}

    TASK [Download and unpack latest WordPress] ************************************
    changed: [consul-server] => {"changed": true, "dest": "/var/www/test.local", "extract_results": {"cmd": ["/bin/gtar", "--extract", "-C", "/var/www/test.local", "-z", "-f", "/home/vagrant/.ansible/tmp/ansible-tmp-1674994827.6611865-11942-88572250041665/latest.tarOapWuQ.gz"], "err": "", "out": "", "rc": 0}, "gid": 48, "group": "apache", "handler": "TgzArchive", "mode": "0755", "owner": "apache", "secontext": "unconfined_u:object_r:httpd_sys_content_t:s0", "size": 23, "src": "/home/vagrant/.ansible/tmp/ansible-tmp-1674994827.6611865-11942-88572250041665/latest.tarOapWuQ.gz", "state": "directory", "uid": 48}

    TASK [Set ownership] ***********************************************************
    changed: [consul-server] => {"changed": true, "gid": 48, "group": "apache", "mode": "0755", "owner": "apache", "path": "/var/www/test.local", "secontext": "unconfined_u:object_r:httpd_sys_content_t:s0", "size": 23, "state": "directory", "uid": 48}

    TASK [Set permissions for directories] *****************************************
    changed: [consul-server] => {"changed": true, "cmd": "/usr/bin/find /var/www/test.local/wordpress/ -type d -exec chmod 750 {} \\;", "delta": "0:00:00.332592", "end": "2023-01-29 12:20:42.261347", "rc": 0, "start": "2023-01-29 12:20:41.928755", "stderr": "", "stderr_lines": [], "stdout": "", "stdout_lines": []}

    TASK [Set permissions for files] ***********************************************
    changed: [consul-server] => {"changed": true, "cmd": "/usr/bin/find /var/www/test.local/wordpress/ -type f -exec chmod 640 {} \\;", "delta": "0:00:02.751812", "end": "2023-01-29 12:20:45.475095", "rc": 0, "start": "2023-01-29 12:20:42.723283", "stderr": "", "stderr_lines": [], "stdout": "", "stdout_lines": []}

    TASK [Set up wp-config] ********************************************************
    changed: [consul-server] => {"changed": true, "checksum": "6b82a9beab5ea9fb8299bcd88b9c25746975942f", "dest": "/var/www/test.local/wordpress/wp-config.php", "gid": 0, "group": "root", "md5sum": "4c8b3642f310996459e36f71e21670c1", "mode": "0644", "owner": "root", "secontext": "system_u:object_r:httpd_sys_content_t:s0", "size": 3140, "src": "/home/vagrant/.ansible/tmp/ansible-tmp-1674994845.5925927-12003-96712130710303/source", "state": "file", "uid": 0}

    TASK [copy files from local host to remote host] *******************************
    changed: [consul-server] => {"changed": true, "dest": "/var/www/test.local/wordpress/", "src": "/var/lib/jenkins/workspace/exam-master-branch/./webapp/"}

    RUNNING HANDLER [Restart httpd] ************************************************
    changed: [consul-server] => {"changed": true, "enabled": true, "name": "httpd", "state": "started", "status": {"ActiveEnterTimestampMonotonic": "0", "ActiveExitTimestampMonotonic": "0", "ActiveState": "inactive", "After": "-.mount systemd-journald.socket system.slice ................

    PLAY RECAP *********************************************************************
    consul-server              : ok=21   changed=20   unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   

    [Pipeline] sh
    + echo DEPLOY STAGE OK
    DEPLOY STAGE OK
    [Pipeline] }
    [Pipeline] // stage
    [Pipeline] }
    [Pipeline] // withEnv
    [Pipeline] }
    [Pipeline] // node
    [Pipeline] End of Pipeline
    Finished: SUCCESS

Jenkins master another build output:  

    Started by an SCM change
    Obtained Jenkinsfile from git https://github.com/m-koleda/exam.git
    [Pipeline] Start of Pipeline
    [Pipeline] node
    Running on Jenkins in /var/lib/jenkins/workspace/exam-master-branch
    [Pipeline] {
    [Pipeline] stage
    [Pipeline] { (Declarative: Checkout SCM)
    [Pipeline] checkout
    Selected Git installation does not exist. Using Default
    The recommended git tool is: NONE
    No credentials specified
     > git rev-parse --resolve-git-dir /var/lib/jenkins/workspace/exam-master-branch/.git # timeout=10
    Fetching changes from the remote Git repository
     > git config remote.origin.url https://github.com/m-koleda/exam.git # timeout=10
    Fetching upstream changes from https://github.com/m-koleda/exam.git
     > git --version # timeout=10
     > git --version # 'git version 2.34.1'
     > git fetch --tags --force --progress -- https://github.com/m-koleda/exam.git +refs/heads/*:refs/remotes/origin/* # timeout=10
     > git rev-parse refs/remotes/origin/master^{commit} # timeout=10
    Checking out Revision eb6d46214abeb97b32f21f8ef65e504bad8e0a57 (refs/remotes/origin/master)
     > git config core.sparsecheckout # timeout=10
     > git checkout -f eb6d46214abeb97b32f21f8ef65e504bad8e0a57 # timeout=10
    Commit message: "update config.yaml"
     > git rev-list --no-walk 0d522999ce365e16395e94c859d0ab4de50600e1 # timeout=10
    [Pipeline] }
    [Pipeline] // stage
    [Pipeline] withEnv
    [Pipeline] {
    [Pipeline] stage
    [Pipeline] { (Build)
    [Pipeline] sh
    + echo BUILDING...
    BUILDING...
    [Pipeline] sh
    + echo BUILD ID - 9
    BUILD ID - 9
    [Pipeline] sh
    + echo BUILD STAGE OK
    BUILD STAGE OK
    [Pipeline] }
    [Pipeline] // stage
    [Pipeline] stage
    [Pipeline] { (Test)
    [Pipeline] sh
    + echo TESTING...
    TESTING...
    [Pipeline] sh
    + python3 test.py
    CHECK REQUIRED FIELDS IN CONFIG.YAML... 

    check 'use' - type of OS...
    ...ok. use: CentOS
    check playbook...
    ...ok
    check public_ip...
    ...ok
    CHECK REQUIRED FIELDS IN JENKINSFILE... 

    check for presence of test.py
    ...ok
    check right Vagrant command...
    ...ok
    CHECK REQUIRED FIELDS IN VAGRANTFILE... 

    check link for config.yaml
    ...ok
    check for presence of boxes name ...
    ...ok
    check for public network and bridge ...
    ...ok
    TEST STAGE OK
    [Pipeline] }
    [Pipeline] // stage
    [Pipeline] stage
    [Pipeline] { (Deploy)
    [Pipeline] sh
    + echo DEPLOYING...
    DEPLOYING...
    [Pipeline] sh
    + vagrant up --provision
    Bringing machine 'consul-server' up with 'virtualbox' provider...
    ==> consul-server: Checking if box 'centos/7' version '2004.01' is up to date...
    ==> consul-server: Running provisioner: ansible...
        consul-server: Running ansible-playbook...
    PYTHONUNBUFFERED=1 ANSIBLE_NOCOLOR=true ANSIBLE_HOST_KEY_CHECKING=false ANSIBLE_SSH_ARGS='-o UserKnownHostsFile=/dev/null -o IdentitiesOnly=yes -o ControlMaster=auto -o ControlPersist=60s' ansible-playbook --connection=ssh --timeout=30 --limit="consul-server" --inventory-file=/var/lib/jenkins/workspace/exam-master-branch/.vagrant/provisioners/ansible/inventory -v playbook-centos-cd.yml
    No config file found; using defaults

    PLAY [all] *********************************************************************

    TASK [Gathering Facts] *********************************************************
    ok: [consul-server]

    TASK [Copy files from local host to remote host] *******************************
    changed: [consul-server] => {"changed": true, "dest": "/var/www/test.local/wordpress/", "src": "/var/lib/jenkins/workspace/exam-master-branch/./webapp/"}

    TASK [Restart Apache] **********************************************************
    changed: [consul-server] => {"changed": true, "name": "httpd", "state": "started", "status": {"ActiveEnterTimestamp": "Sun 2023-01-29 12:21:44 UTC", "ActiveEnterTimestampMonotonic": "307390713", "ActiveExitTimestampMonotonic": "0", "ActiveState": "active", "After": ................

    PLAY RECAP *********************************************************************
    consul-server              : ok=3    changed=2    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   

    [Pipeline] sh
    + echo DEPLOY STAGE OK
    DEPLOY STAGE OK
    [Pipeline] }
    [Pipeline] // stage
    [Pipeline] }
    [Pipeline] // withEnv
    [Pipeline] }
    [Pipeline] // node
    [Pipeline] End of Pipeline
    Finished: SUCCESS

Jenkins dev first build output:  

    Started by an SCM change
    Obtained Jenkinsfile from git https://github.com/m-koleda/exam.git
    [Pipeline] Start of Pipeline
    [Pipeline] node
    Running on Jenkins in /var/lib/jenkins/workspace/exam-dev-branch
    [Pipeline] {
    [Pipeline] stage
    [Pipeline] { (Declarative: Checkout SCM)
    [Pipeline] checkout
    Selected Git installation does not exist. Using Default
    The recommended git tool is: NONE
    No credentials specified
     > git rev-parse --resolve-git-dir /var/lib/jenkins/workspace/exam-dev-branch/.git # timeout=10
    Fetching changes from the remote Git repository
     > git config remote.origin.url https://github.com/m-koleda/exam.git # timeout=10
    Fetching upstream changes from https://github.com/m-koleda/exam.git
     > git --version # timeout=10
     > git --version # 'git version 2.34.1'
     > git fetch --tags --force --progress -- https://github.com/m-koleda/exam.git +refs/heads/*:refs/remotes/origin/* # timeout=10
     > git rev-parse refs/remotes/origin/dev^{commit} # timeout=10
    Checking out Revision 6632527dcb7940ae55c3c852b6c7b8b1353e5088 (refs/remotes/origin/dev)
     > git config core.sparsecheckout # timeout=10
     > git checkout -f 6632527dcb7940ae55c3c852b6c7b8b1353e5088 # timeout=10
    Commit message: "update config.yaml"
     > git rev-list --no-walk 0520d637b50d5ff0b0e5b3d850adebce9cd73a73 # timeout=10
    [Pipeline] }
    [Pipeline] // stage
    [Pipeline] withEnv
    [Pipeline] {
    [Pipeline] stage
    [Pipeline] { (Build)
    [Pipeline] sh
    + echo BUILDING...
    BUILDING...
    [Pipeline] sh
    + echo BUILD ID - 3
    BUILD ID - 3
    [Pipeline] sh
    + echo BUILD STAGE OK
    BUILD STAGE OK
    [Pipeline] }
    [Pipeline] // stage
    [Pipeline] stage
    [Pipeline] { (Test)
    [Pipeline] sh
    + echo TESTING...
    TESTING...
    [Pipeline] sh
    + python3 test.py
    CHECK REQUIRED FIELDS IN CONFIG.YAML... 

    check 'use' - type of OS...
    ...ok. use: Ubuntu
    check playbook...
    ...ok
    check public_ip...
    ...ok
    CHECK REQUIRED FIELDS IN JENKINSFILE... 

    check for presence of test.py
    ...ok
    check right Vagrant command...
    ...ok
    CHECK REQUIRED FIELDS IN VAGRANTFILE... 

    check link for config.yaml
    ...ok
    check for presence of boxes name ...
    ...ok
    check for public network and bridge ...
    ...ok
    TEST STAGE OK
    [Pipeline] }
    [Pipeline] // stage
    [Pipeline] stage
    [Pipeline] { (Deploy)
    [Pipeline] sh
    + echo DEPLOYING...
    DEPLOYING...
    [Pipeline] sh
    + vagrant up --provision
    Bringing machine 'consul-server' up with 'virtualbox' provider...
    ==> consul-server: Importing base box 'ubuntu/bionic64'...

    [KProgress: 10%
    [KProgress: 90%
    [K==> consul-server: Matching MAC address for NAT networking...
    ==> consul-server: Checking if box 'ubuntu/bionic64' version '20230124.0.0' is up to date...
    ==> consul-server: There was a problem while downloading the metadata for your box
    ==> consul-server: to check for updates. This is not an error, since it is usually due
    ==> consul-server: to temporary network problems. This is just a warning. The problem
    ==> consul-server: encountered was:
    ==> consul-server: 
    ==> consul-server: The requested URL returned error: 404
    ==> consul-server: 
    ==> consul-server: If you want to check for box updates, verify your network connection
    ==> consul-server: is valid and try again.
    ==> consul-server: Setting the name of the VM: exam-dev-branch_consul-server_1674995977414_40212
    ==> consul-server: Fixed port collision for 22 => 2222. Now on port 2201.
    ==> consul-server: Clearing any previously set network interfaces...
    ==> consul-server: Preparing network interfaces based on configuration...
        consul-server: Adapter 1: nat
        consul-server: Adapter 2: bridged
    ==> consul-server: Forwarding ports...
        consul-server: 22 (guest) => 2201 (host) (adapter 1)
    ==> consul-server: Running 'pre-boot' VM customizations...
    ==> consul-server: Booting VM...
    ==> consul-server: Waiting for machine to boot. This may take a few minutes...
        consul-server: SSH address: 127.0.0.1:2201
        consul-server: SSH username: vagrant
        consul-server: SSH auth method: private key
        consul-server: Warning: Connection reset. Retrying...
        consul-server: Warning: Remote connection disconnect. Retrying...
        consul-server: 
        consul-server: Vagrant insecure key detected. Vagrant will automatically replace
        consul-server: this with a newly generated keypair for better security.
        consul-server: 
        consul-server: Inserting generated public key within guest...
        consul-server: Removing insecure key from the guest if it's present...
        consul-server: Key inserted! Disconnecting and reconnecting using new SSH key...
    ==> consul-server: Machine booted and ready!
    ==> consul-server: Checking for guest additions in VM...
        consul-server: The guest additions on this VM do not match the installed version of
        consul-server: VirtualBox! In most cases this is fine, but in rare cases it can
        consul-server: prevent things such as shared folders from working properly. If you see
        consul-server: shared folder errors, please make sure the guest additions within the
        consul-server: virtual machine match the version of VirtualBox you have installed on
        consul-server: your host and reload your VM.
        consul-server: 
        consul-server: Guest Additions Version: 5.2.42
        consul-server: VirtualBox Version: 6.1
    ==> consul-server: Configuring and enabling network interfaces...
    ==> consul-server: Mounting shared folders...
        consul-server: /vagrant => /var/lib/jenkins/workspace/exam-dev-branch
    ==> consul-server: Running provisioner: ansible...
        consul-server: Running ansible-playbook...
    PYTHONUNBUFFERED=1 ANSIBLE_NOCOLOR=true ANSIBLE_HOST_KEY_CHECKING=false ANSIBLE_SSH_ARGS='-o UserKnownHostsFile=/dev/null -o IdentitiesOnly=yes -o ControlMaster=auto -o ControlPersist=60s' ansible-playbook --connection=ssh --timeout=30 --limit="consul-server" --inventory-file=/var/lib/jenkins/workspace/exam-dev-branch/.vagrant/provisioners/ansible/inventory -v playbook-ubuntu-startvm.yml
    No config file found; using defaults

    PLAY [all] *********************************************************************

    TASK [Gathering Facts] *********************************************************
    ok: [consul-server]

    TASK [Install prerequisites] ***************************************************
    changed: [consul-server] => {"cache_update_time": 1674996033, "cache_updated": true, "changed": true, "stderr": "", "stderr_lines": [], "stdout": ...............

    TASK [Install LAMP Packages] ***************************************************
    changed: [consul-server] => (item=apache2) => {"ansible_loop_var": "item", "cache_update_time": 1674996061, "cache_updated": true, "changed": true, "item": "apache2", "stderr": "", "stderr_lines": [], "stdout": ............... 

    TASK [Create document root] ****************************************************
    changed: [consul-server] => {"changed": true, "gid": 33, "group": "www-data", "mode": "0755", "owner": "www-data", "path": "/var/www/test.local", "size": 4096, "state": "directory", "uid": 33}

    TASK [Set up Apache VirtualHost] ***********************************************
    changed: [consul-server] => {"changed": true, "checksum": "f15959302a6db742269504ff037bec59b75ed1ea", "dest": "/etc/apache2/sites-available/test.local.conf", "gid": 0, "group": "root", "md5sum": "e7fc43b4c4b4cafc34d1a155c1ab2be8", "mode": "0644", "owner": "root", "size": 504, "src": "/home/vagrant/.ansible/tmp/ansible-tmp-1674996239.015966-18278-223022341217185/source", "state": "file", "uid": 0}

    TASK [Enable rewrite module] ***************************************************
    changed: [consul-server] => {"changed": true, "cmd": "/usr/sbin/a2enmod rewrite", "delta": "0:00:00.063919", "end": "2023-01-29 12:43:58.923969", "rc": 0, "start": "2023-01-29 12:43:58.860050", "stderr": "", "stderr_lines": [], "stdout": "Enabling module rewrite.\nTo activate the new configuration, you need to run:\n  systemctl restart apache2", "stdout_lines": ["Enabling module rewrite.", "To activate the new configuration, you need to run:", "  systemctl restart apache2"]}

    TASK [Enable new site] *********************************************************
    changed: [consul-server] => {"changed": true, "cmd": "/usr/sbin/a2ensite test.local.conf", "delta": "0:00:00.064334", "end": "2023-01-29 12:43:59.387114", "rc": 0, "start": "2023-01-29 12:43:59.322780", "stderr": "", "stderr_lines": [], "stdout": "Enabling site test.local.\nTo activate the new configuration, you need to run:\n  systemctl reload apache2", "stdout_lines": ["Enabling site test.local.", "To activate the new configuration, you need to run:", "  systemctl reload apache2"]}

    TASK [Disable default Apache site] *********************************************
    changed: [consul-server] => {"changed": true, "cmd": "/usr/sbin/a2dissite 000-default.conf", "delta": "0:00:00.050143", "end": "2023-01-29 12:43:59.809781", "rc": 0, "start": "2023-01-29 12:43:59.759638", "stderr": "", "stderr_lines": [], "stdout": "Site 000-default disabled.\nTo activate the new configuration, you need to run:\n  systemctl reload apache2", "stdout_lines": ["Site 000-default disabled.", "To activate the new configuration, you need to run:", "  systemctl reload apache2"]}

    TASK [Set the root password] ***************************************************
    changed: [consul-server] => {"changed": true, "msg": "Password updated (new style)", "user": "root"}

    TASK [Remove all anonymous user accounts] **************************************
    ok: [consul-server] => {"changed": false, "msg": "User doesn't exist", "user": ""}

    TASK [Remove the MySQL test database] ******************************************
    ok: [consul-server] => {"changed": false, "db": "test", "db_list": ["test"], "executed_commands": []}

    TASK [Creates database for WordPress] ******************************************
    changed: [consul-server] => {"changed": true, "db": "wordpress", "db_list": ["wordpress"], "executed_commands": ["CREATE DATABASE `wordpress`"]}

    TASK [Create MySQL user for WordPress] *****************************************
    changed: [consul-server] => {"changed": true, "msg": "User added", "user": "sammy"}

    TASK [UFW - Allow HTTP on port 80] *********************************************
    changed: [consul-server] => {"changed": true, "commands": ["/usr/sbin/ufw status verbose", "/bin/grep -h '^### tuple' /lib/ufw/user.rules /lib/ufw/user6.rules /etc/ufw/user.rules /etc/ufw/user6.rules /var/lib/ufw/user.rules /var/lib/ufw/user6.rules", "/usr/sbin/ufw --version", "/usr/sbin/ufw allow from any to any port 80 proto tcp", "/usr/sbin/ufw status verbose", "/bin/grep -h '^### tuple' /lib/ufw/user.rules /lib/ufw/user6.rules /etc/ufw/user.rules /etc/ufw/user6.rules /var/lib/ufw/user.rules /var/lib/ufw/user6.rules"], "msg": "Status: inactive"}

    TASK [Download and unpack latest WordPress] ************************************
    changed: [consul-server] => {"changed": true, "dest": "/var/www/test.local", "extract_results": {"cmd": ["/bin/tar", "--extract", "-C", "/var/www/test.local", "-z", "-f", "/home/vagrant/.ansible/tmp/ansible-tmp-1674996245.7964458-18393-20853256904077/latest.tarddasevta.gz"], "err": "", "out": "", "rc": 0}, "gid": 33, "group": "www-data", "handler": "TgzArchive", "mode": "0755", "owner": "www-data", "size": 4096, "src": "/home/vagrant/.ansible/tmp/ansible-tmp-1674996245.7964458-18393-20853256904077/latest.tarddasevta.gz", "state": "directory", "uid": 33}

    TASK [copy files from local host to remote host] *******************************
    changed: [consul-server] => {"changed": true, "dest": "/var/www/test.local/wordpress/", "src": "/var/lib/jenkins/workspace/exam-dev-branch/./webapp/"}

    TASK [Set ownership] ***********************************************************
    changed: [consul-server] => {"changed": true, "gid": 33, "group": "www-data", "mode": "0755", "owner": "www-data", "path": "/var/www/test.local", "size": 4096, "state": "directory", "uid": 33}

    TASK [Set permissions for directories] *****************************************
    changed: [consul-server] => {"changed": true, "cmd": "/usr/bin/find /var/www/test.local/wordpress/ -type d -exec chmod 750 {} \\;", "delta": "0:00:00.330637", "end": "2023-01-29 12:45:03.969703", "rc": 0, "start": "2023-01-29 12:45:03.639066", "stderr": "", "stderr_lines": [], "stdout": "", "stdout_lines": []}

    TASK [Set permissions for files] ***********************************************
    changed: [consul-server] => {"changed": true, "cmd": "/usr/bin/find /var/www/test.local/wordpress/ -type f -exec chmod 640 {} \\;", "delta": "0:00:02.567132", "end": "2023-01-29 12:45:06.919024", "rc": 0, "start": "2023-01-29 12:45:04.351892", "stderr": "", "stderr_lines": [], "stdout": "", "stdout_lines": []}

    TASK [Set up wp-config] ********************************************************
    changed: [consul-server] => {"changed": true, "checksum": "03b5c9d9562b3a7745820c9044823bc346c3dbae", "dest": "/var/www/test.local/wordpress/wp-config.php", "gid": 0, "group": "root", "md5sum": "0670c18feedf089dfca5f9b6e77cd275", "mode": "0644", "owner": "root", "size": 3140, "src": "/home/vagrant/.ansible/tmp/ansible-tmp-1674996308.5624974-19321-124848926968781/source", "state": "file", "uid": 0}

    RUNNING HANDLER [Reload Apache] ************************************************
    changed: [consul-server] => {"changed": true, "name": "apache2", "state": "started", "status": {"ActiveEnterTimestamp": "Sun 2023-01-29 12:42:23 UTC", "ActiveEnterTimestampMonotonic": "160672537", "ActiveExitTimestamp": ...............

    RUNNING HANDLER [Restart Apache] ***********************************************
    changed: [consul-server] => {"changed": true, "name": "apache2", "state": "started", "status": {"ActiveEnterTimestamp": "Sun 2023-01-29 12:42:23 UTC", "ActiveEnterTimestampMonotonic": "160672537", "ActiveExitTimestamp": "Sun 2023-01-29 12:42:23 UTC" ...............

    PLAY RECAP *********************************************************************
    consul-server              : ok=23   changed=20   unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   

    [Pipeline] sh
    + echo DEPLOY STAGE OK
    DEPLOY STAGE OK
    [Pipeline] }
    [Pipeline] // stage
    [Pipeline] }
    [Pipeline] // withEnv
    [Pipeline] }
    [Pipeline] // node
    [Pipeline] End of Pipeline
    Finished: SUCCESS


Jenkins dev another build output:  

    Started by an SCM change
    Obtained Jenkinsfile from git https://github.com/m-koleda/exam.git
    [Pipeline] Start of Pipeline
    [Pipeline] node
    Running on Jenkins in /var/lib/jenkins/workspace/exam-dev-branch
    [Pipeline] {
    [Pipeline] stage
    [Pipeline] { (Declarative: Checkout SCM)
    [Pipeline] checkout
    Selected Git installation does not exist. Using Default
    The recommended git tool is: NONE
    No credentials specified
     > git rev-parse --resolve-git-dir /var/lib/jenkins/workspace/exam-dev-branch/.git # timeout=10
    Fetching changes from the remote Git repository
     > git config remote.origin.url https://github.com/m-koleda/exam.git # timeout=10
    Fetching upstream changes from https://github.com/m-koleda/exam.git
     > git --version # timeout=10
     > git --version # 'git version 2.34.1'
     > git fetch --tags --force --progress -- https://github.com/m-koleda/exam.git +refs/heads/*:refs/remotes/origin/* # timeout=10
     > git rev-parse refs/remotes/origin/dev^{commit} # timeout=10
    Checking out Revision 4ee002ca18ea40960c94c3582c472e307b6b1b05 (refs/remotes/origin/dev)
     > git config core.sparsecheckout # timeout=10
     > git checkout -f 4ee002ca18ea40960c94c3582c472e307b6b1b05 # timeout=10
    Commit message: "update config.yaml"
     > git rev-list --no-walk 6632527dcb7940ae55c3c852b6c7b8b1353e5088 # timeout=10
    [Pipeline] }
    [Pipeline] // stage
    [Pipeline] withEnv
    [Pipeline] {
    [Pipeline] stage
    [Pipeline] { (Build)
    [Pipeline] sh
    + echo BUILDING...
    BUILDING...
    [Pipeline] sh
    + echo BUILD ID - 4
    BUILD ID - 4
    [Pipeline] sh
    + echo BUILD STAGE OK
    BUILD STAGE OK
    [Pipeline] }
    [Pipeline] // stage
    [Pipeline] stage
    [Pipeline] { (Test)
    [Pipeline] sh
    + echo TESTING...
    TESTING...
    [Pipeline] sh
    + python3 test.py
    CHECK REQUIRED FIELDS IN CONFIG.YAML... 

    check 'use' - type of OS...
    ...ok. use: Ubuntu
    check playbook...
    ...ok
    check public_ip...
    ...ok
    CHECK REQUIRED FIELDS IN JENKINSFILE... 

    check for presence of test.py
    ...ok
    check right Vagrant command...
    ...ok
    CHECK REQUIRED FIELDS IN VAGRANTFILE... 

    check link for config.yaml
    ...ok
    check for presence of boxes name ...
    ...ok
    check for public network and bridge ...
    ...ok
    TEST STAGE OK
    [Pipeline] }
    [Pipeline] // stage
    [Pipeline] stage
    [Pipeline] { (Deploy)
    [Pipeline] sh
    + echo DEPLOYING...
    DEPLOYING...
    [Pipeline] sh
    + vagrant up --provision
    Bringing machine 'consul-server' up with 'virtualbox' provider...
    ==> consul-server: Checking if box 'ubuntu/bionic64' version '20230124.0.0' is up to date...
    ==> consul-server: Running provisioner: ansible...
        consul-server: Running ansible-playbook...
    PYTHONUNBUFFERED=1 ANSIBLE_NOCOLOR=true ANSIBLE_HOST_KEY_CHECKING=false ANSIBLE_SSH_ARGS='-o UserKnownHostsFile=/dev/null -o IdentitiesOnly=yes -o ControlMaster=auto -o ControlPersist=60s' ansible-playbook --connection=ssh --timeout=30 --limit="consul-server" --inventory-file=/var/lib/jenkins/workspace/exam-dev-branch/.vagrant/provisioners/ansible/inventory -v playbook-ubuntu-cd.yml
    No config file found; using defaults

    PLAY [all] *********************************************************************

    TASK [Gathering Facts] *********************************************************
    ok: [consul-server]

    TASK [Copy files from local host to remote host] *******************************
    ok: [consul-server] => {"changed": false, "dest": "/var/www/test.local/wordpress/", "src": "/var/lib/jenkins/workspace/exam-dev-branch/webapp/"}

    TASK [Restart Apache] **********************************************************
    changed: [consul-server] => {"changed": true, "name": "apache2", "state": "started", "status": {"ActiveEnterTimestamp": "Sun 2023-01-29 12:45:09 UTC", "ActiveEnterTimestampMonotonic": "327346609", "ActiveExitTimestamp": "Sun 2023-01-29 12:45:09 UTC", ...............

    PLAY RECAP *********************************************************************
    consul-server              : ok=3    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   

    [Pipeline] sh
    + echo DEPLOY STAGE OK
    DEPLOY STAGE OK
    [Pipeline] }
    [Pipeline] // stage
    [Pipeline] }
    [Pipeline] // withEnv
    [Pipeline] }
    [Pipeline] // node
    [Pipeline] End of Pipeline
    Finished: SUCCESS




For more information on how to run Ansible setup check this guide: [How to Use Ansible to Install and Set Up WordPress with LAMP on Ubuntu 18.04](https://www.digitalocean.com/community/tutorials/how-to-use-ansible-to-install-and-set-up-wordpress-with-lamp-on-ubuntu-18-04).
Used materials:  
https://www.digitalocean.com/community/tutorials/how-to-install-jenkins-on-ubuntu-22-04  
+change jenkins as user $USER  
https://medium.com/fusionqa/how-to-run-jenkins-using-the-root-user-in-linux-centos-79d96749ca5a  
https://www.digitalocean.com/community/tutorials/how-to-install-the-apache-web-server-on-centos-7  
https://www.digitalocean.com/community/tutorials/how-to-install-linux-apache-mysql-php-lamp-stack-on-centos-7  
https://github.com/arocki7/ansible-centos7-lamp  
https://github.com/sruthymanohar/Ansible-role-lamp-wordpress  
https://www.digitalocean.com/community/tutorials/how-to-use-ansible-to-install-and-set-up-wordpress-with-lamp-on-ubuntu-18-04-ru  
https://docs.ansible.com/ansible/latest/collections/ansible/builtin/yum_module.html  
https://developer.hashicorp.com/vagrant/docs/vagrantfile/machine_settings  
https://developer.hashicorp.com/vagrant/docs/provisioning/ansible  
https://docs.ansible.com/ansible/latest/scenario_guides/guide_vagrant.html#  
https://help.ubuntu.ru/wiki/vagrant  
https://pocoz.gitbooks.io/ansible_for_dev_ops_russian/content/chapter1/ispolzovanie-ansible-s-vagrant.html  
https://github.com/hashicorp/vagrant/issues/9666#issuecomment-401931144  
