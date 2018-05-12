#!/bin/bash

MIN_PYTHON_VERSION=2.7

#Let's make sure the user's system is ready to roll
command_exists () {
    type "$1" &> /dev/null ;
}

# make sure Python installed
python_check (){
    echo "checking for Python"
    ver = python -c 'import platform; print(platform.python_version())'

}

# make sure pip installed
pip_check (){
    echo "checking for PIP"
}

# make sure git is installed
git_check (){
    if command_exists git
        then
            HAVEGIT=1
    fi
}

# do you want to set up Raspberry Pi auto-login? recommended
auto_login (){
    echo "do you want to setup auto-login?"
}

# install python requirements
python_requirements (){
    echo "installing Python requirements"
}

# Copy Start/Stop scripts to home
copy_scripts (){
    echo "installing ibuki scripts"
}
# Copy Lib to ...
copy_lib(){
    echo "installing ibuki libraries"
}

# Copy Run to Home/ibuki
copy_ibuki (){
    echo "installing ibuki software"
}

# add ibuki.sh to profile.d
add_to_path (){
    echo "adding all path parameters"
    mv ibuki.sh /etc/profile.d/
}

# add ibuki screen to .screenrc
setup_screen(){
    echo "screen -t ibuki 0 bash" > .screenrc

}

install (){
    echo "installing"
    python_check
    pip_check
    python_requirements
    auto_login

    copy_scripts
    copy_lib
    copy_ibuki
    setup_screen
}

# ready to install ibuki?
read -p "Are you ready to install ibuki and its dependencies? (y/n)" answer
case ${answer:0:1} in
    y|Y )
        install
    ;;
    * )
        echo No
    ;;
esac
