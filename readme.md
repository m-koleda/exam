# exam
An exam in itstep.by

# Wordpress LAMP on Ubuntu 16.04 LTS or CentOS 7 or Docker-image

This playbook will install a LAMP environment (**L**inux, **A**pache, **M**ySQL and **P**HP), Wordpress and copy site from dir site on 
an Ubuntu 16.04 or CentOS machine or like Docker-image. Machines and image will auto-create by Vagrant and will configuare by Ansible. 
You can choose an OS in the `config.yaml` file.
A virtualhost will be created with the options specified in the `vars/default.yml` variable file.

## Settings

- `mysql_root_password`: the password for the MySQL root account.
- `app_user`: a remote non-root user on the Ansible host that will own the application files.
- `http_host`: your domain name.
- `http_conf`: the name of the configuration file that will be created within Apache.
- `http_port`: HTTP port, default is 80.
- `disable_default`: whether or not to disable the default Apache website. When set to true, your new virtualhost should be used as default website. Default is true.


## Running this Playbook

Quickstart guide for those already familiar with Ansible:

### 1. Obtain the playbook
```shell
git clone https://github.com/m-koleda/exam.git
cd ....
```

### 2. Customize Options

```shell
nano vars/default.yml
nano config.yaml
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

### 3. Run the Vagrant VM + Playbook

```command
vagrant up
```

For more information on how to run this Ansible setup, please check this guide:.
