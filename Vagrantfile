Vagrant.configure("2") do |config|
  config.vm.box = "bento/ubuntu-20.10"
  config.vm.box_check_update = true

  # on the host
  #  localhost:60610 is the queueserver console
  #  localhost:60610/docs is the fastapi documentation
  config.vm.network "forwarded_port", guest: 60610, host: 60610

  config.vm.provider "virtualbox" do |vb|
    vb.gui = false
  end

  config.vm.provision "shell", inline: <<-SHELL
    # https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-20-04
    apt update
    apt full-upgrade
    apt install -y python3-pip

    # install miniconda3
    wget -P /tmp https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
    bash /tmp/Miniconda3-latest-Linux-x86_64.sh -b -p /home/vagrant/miniconda3
    rm /tmp/Miniconda3-latest-Linux-x86_64.sh
    /home/vagrant/miniconda3/bin/conda init --system
    /home/vagrant/miniconda3/bin/conda update conda -y

    # create a conda environment for bluesky-queueserver and bluesky-httpserver
    /home/vagrant/miniconda3/bin/conda create -y -n qserver python=3.8
    /home/vagrant/miniconda3/envs/qserver/bin/pip install bluesky-httpserver
    /home/vagrant/miniconda3/envs/qserver/bin/pip install -e /vagrant
    /home/vagrant/miniconda3/envs/qserver/bin/pip install -r /vagrant/requirements-dev.txt
    # change ownership for /home/vagrant/miniconda3 after creating virtual environments and installing packages
    chown -R vagrant:vagrant /home/vagrant/miniconda3

    # install bluesky-queueserver source to get the simulated ipython profile
    git clone https://github.com/bluesky/bluesky-queueserver.git /home/vagrant/bluesky-queueserver
    chown -R vagrant:vagrant /home/vagrant/bluesky-queueserver

    # install redis on default port for bluesky-queueserver
    apt install redis -y
    systemctl stop redis
    # losing the fight for a regular expression [0-9]\+ is close
    sed "s;^port 6379;port 60590;" -i /etc/redis/redis.conf
    systemctl start redis
    systemctl enable redis

    # install mongodb
    wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | sudo apt-key add -
    echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/4.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.4.list
    apt update
    apt install -y mongodb-org

    # note: change the mongodb bindIP in /etc/mongod.conf to 0.0.0.0 to allow connections from the host
    sed "s;bindIP;bindIP 0.0.0.0;" -i /etc/mongod.conf

    systemctl start mongod
    systemctl enable mongod

#     # databroker will look for this directory
#     cd /home/vagrant
#     mkdir -p .local/share/intake
#     chown -Rv vagrant:vagrant .local
  SHELL
end
