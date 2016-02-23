Vagrant.configure(2) do |config|

  config.vm.box = "centos66-java8-dev"
  config.vm.box_check_update = false

  config.rdp.port = 5000

  config.vm.network "private_network", ip: "192.168.33.40"

  # take care of /etc/hosts in both host and guest
  config.hostmanager.enabled = true
  config.hostmanager.manage_host = true
  config.hostmanager.manage_guest = true

  config.vm.define "rpmbuild" do |toolvm|
    toolvm.vm.network "private_network", ip: "192.168.11.10"
    toolvm.vm.hostname = "rpmbuild"
    toolvm.vm.provision :hostmanager
    toolvm.hostmanager.aliases = %w(rpmbuild.homenet.vn)

  end
  config.vm.synced_folder ".", "/work"

  config.vm.provider "virtualbox" do |vb|
    vb.name   = "rpmbuild"
    vb.gui    = false
    vb.memory = 2024
    vb.cpus   = 2
  end

  config.vm.provision "file", source: ".provision/macros.rpmbuild", destination: "/tmp/macros.rpmbuild"
  config.vm.provision "shell", path: ".provision/do_provision.sh"
end

# vim: set ai nu nobk expandtab sw=2 tw=72 ts=4 syntax=ruby :
