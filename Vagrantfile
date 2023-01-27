# -*- mode: ruby -*-
# vi: set ft=ruby :

require 'yaml'

current_dir    = File.dirname(File.expand_path(__FILE__))
configs        = YAML.load_file("#{current_dir}/config.yaml")
vagrant_config = configs['configs'][configs['configs']['use']]

Vagrant.configure("2") do |config|
  config.vm.box = vagrant_config['box']
  config.vm.box_version = vagrant_config['box_version']
  config.vbguest.auto_update = false
  config.vm.define "consul-server" do |machine|
	machine.vm.network "public_network", bridge: "enp1s0", ip: vagrant_config['public_ip'] 
#wlp2s0 
        #machine.vm.provision "shell", inline: "echo ubuntu:ubuntu | chpasswd" 
        #machine.vm.synced_folder "./webapp/", vagrant_config['path'], type: "rsync"
          
  end
  config.vm.provision "ansible" do |ansible|
    ansible.verbose = "v"
    ansible.playbook = vagrant_config['playbook']  

  end
end
