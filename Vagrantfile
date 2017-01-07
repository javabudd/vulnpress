Vagrant.configure(2) do |config|
  config.vm.box = "javabudd/centos72-samba"
  config.ssh.pty = true

  config.vm.provider "virtualbox" do |v|
    v.memory = ENV.fetch('VAGRANT_MEMORY', 2048)
    v.cpus = ENV.fetch('VAGRANT_CPUS', 1)
    v.check_guest_additions = false
  end

  config.vm.network "private_network", ip: ENV.fetch('VAGRANT_PRIVATE_IP', "192.168.69.69")

  if Vagrant::Util::Platform.windows?
    config.vm.synced_folder ".", "/vagrant", type: "smb", mount_options: ["dir_mode=0777,file_mode=0777"]
  else
    config.vm.synced_folder ".", "/vagrant", type: "nfs"
  end

  config.vm.provision "shell", run: "always", inline: "sysctl -w net.ipv4.ip_forward=1"

  config.vm.provision "shell", run: "always", inline: "docker rm -f $(docker ps -a -q) || true"

  config.vm.provision "docker", run: "always" do |d|
    d.build_image "/vagrant/docker", args: "-t 'vulnpress/webserver'"
    d.run "vulnpress/webserver",
      args: "--restart no -e 'TERM=vt100' \
        -v '/var/lib/mysql:/var/lib/mysql' \
        -v '/vagrant/docker/wordpress:/var/www/wordpress' \
        -h 'vulnpress.dev' -p 80:80 -p 3306:3306"
  end
end
