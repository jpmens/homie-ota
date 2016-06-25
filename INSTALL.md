## Install python, pip, virtualenv and virtualenvwrapper
Become *root* or run commands using `sudo`:

    # be sure you're up-to-date
    apt-get update
    apt-get upgrade

    # install python and pip
    apt-get install python-dev python-pip

    # install virtualenv and virtualenvwrapper
    pip install --upgrade virtualenv virtualenvwrapper

Create a `~/.bashrc` (if not exists) and copy into:

    # for global pip-usage type gpip install...
    gpip(){
       PIP_REQUIRE_VIRTUALENV="" pip "$@"
    }
 
    # pip should only run if there is a virtualenv currently activated
    export PIP_REQUIRE_VIRTUALENV=true
    export WORKON_HOME=$HOME/.venvs
    export PROJECT_HOME=$HOME
    source /usr/local/bin/virtualenvwrapper.sh

*Note: depending on your system the path to the virtualenvwrapper script might be slightly different*

Create a `~/.bash_profile` (if not exists) and copy into:

    # Load .bashrc if it exists
    test -f ~/.bashrc && source ~/.bashrc

## Create a dedicated homie-ota (hota) user

    adduser --system hota

## Login & Install

    su -s /bin/bash -l hota

Create a *~/.bashrc* and *~/.bash_profile* as above.

    # create a new virtualenv for homie-ota
    mkproject homie-ota

    # clone project from git
    git clone https://github.com/jpmens/homie-ota.git .

    # install required components into virtualenv
    pip install -r requirements.txt

    # copy & adjust preferences
    cp homie-ota.ini.example homie-ota.ini

    # try to start homie-ota manually
    ./homie-ota.py

## Autostart

    # create systemd unit file
    touch /lib/systemd/system/homie-ota@hota.service
    # open unit file in nano
    nano /lib/systemd/system/homie-ota@hota.service

Copy into `homie-ota@hota.service`:

    [Unit]
    Description=Homie OTA
    After=network.target
 
    [Service]
    Type=simple
    User=%i
    ExecStart=/home/hota/.venvs/homie-ota/bin/python /home/hota/homie-ota/homie-ota.py
    WorkingDirectory=/home/hota/homie-ota
 
    [Install]
    WantedBy=multi-user.target

Now make systemd aware of your unit:

    systemctl --system daemon-reload
    systemctl enable homie-ota@hota
    systemctl start homie-ota@hota
    systemctl status homie-ota@hota

Check the logs using `journalctl`:

    journalctl -f -u homie-ota@hota
