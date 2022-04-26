# alda
A French programming language created with the SLY library. :croissant: 

## Requirements
 :warning: alda requires the SLY library (sly~=0.4) and therefore the use of Python 3.6 or greater :

    pip3 install -r requirements.txt

## Installation

If you want to generate your own source and binary packages, make sure you have the following packages installed:

    sudo apt-get install python3-stdeb python-all dh-python fakeroot 

You can then run the following commands to generate the source and binary packages:

    python3 setup.py --command-packages=stdeb.command bdist_deb

Or if you want to generate the source package only:

    python3 setup.py --command-packages=stdeb.command sdist_dsc

If you used the `bdist_deb` command, you will find the source and binary packages in the `deb_dist` directory:

    cd deb_dist

You can now install the deb package with the following command:

    sudo dpkg -i python3-alda_1.0.0-1_all.deb

 :warning: If you use Python 3.9 and you encounter any error during the installation, I suggest trying to install it with an older version of Python such as Python 3.7.

## Usage

    alda [-h] [-f FILE] [-s]

    optional arguments:
    -h, --help            show this help message and exit
    -f FILE, --file FILE  Execute program from .alda file
    -s, --shell           Start ALDA shell
