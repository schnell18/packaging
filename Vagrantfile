Vagrant.configure(2) do |config|

  config.vm.box = "centos70-min"
  config.vm.box_check_update = false

  config.rdp.port = 5000

  config.vm.network "private_network", ip: "192.168.33.40"

  config.vm.synced_folder ".", "/work"

  config.vm.provider "virtualbox" do |vb|
    vb.name   = "rpm-build"
    vb.gui    = false
    vb.memory = 2024
    vb.cpus   = 2
  end

  config.vm.provision "shell", path: ".provision/do_provision.sh"
end

# vim: set ai nu nobk expandtab sw=2 tw=72 ts=4 syntax=ruby :
