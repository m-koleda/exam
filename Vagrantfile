# -*- mode: ruby -*-
# vi: set ft=ruby :

require 'yaml'

current_dir    = File.dirname(File.expand_path(__FILE__))
configs        = YAML.load_file("#{current_dir}/config.yaml")
vagrant_config = configs['configs'][configs['configs']['use']]

Vagrant.configure("2") do |config|
  config.vm.box = vagrant_config['os']
  #config.ssh.username = 'vagrant'
  #config.ssh.password = 'vagrant'
  #config.ssh.keys_only = false
  config.vm.define "consul-server" do |machine|
	machine.vm.network "public_network", bridge: "wlp2s0", ip: vagrant_config['public_ip']
#	machine.vm.provision "shell", inline: "echo ubuntu:ubuntu | chpasswd"
#	machine.vm.synced_folder "html/", "/var/www/html"
#	machine.vm.provision "shell", inline: "apt-get update && apt-get install -y python-minimal"
#	machine.vm.provision "shell", inline: "sed -i 's/PasswordAuthentication no/PasswordAuthentication yes/g' /etc/ssh/sshd_config"
#	machine.vm.provision "shell", inline: "systemctl restart sshd.service"
  end
  config.vm.provision "ansible" do |ansible|
    ansible.verbose = "v"
    ansible.playbook = vagrant_config['playbook']  

  end
end
