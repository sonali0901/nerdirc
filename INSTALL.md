#Installation Guide

This guide will help you in setting up nerdirc through console.

##Clone the project
Clone the project from GitHub by running the following command:

    git clone project_url_here

For nerdirc, this would correspond to:

    git clone https://github.com/iogf/nerdirc.git

##Install virtualenv
	pip install virtualenv

Create a virtual environment for your project as shown below. venv here is name of the folder that will be created.
	It can be changed as per choice.

	virtualenv -p /usr/lib/python3 venv

##Activating the virtualenv
Get into the virtualenv where the bin file is present and activate it as follows-

	cd venv
	source bin/activate

##Installing python3

After activating the virtualenv we will start installing the necessities for the project.

	 sudo apt-get install python3

##Installing texlive

	sudo apt-get install textlive

**Note: If you aren't going to use the latex plugin then you don't need to install texlive at all.**

##Installing Tkinter

	sudo apt-get install python3-tk

Tkinter provides a robust and platform independent windowing toolkit, that is available to Python programmers.

##Installing setup file

Come out the virtual environment folder and get into the folder that was cloned.

	cd ..
	cd nerdirc

Install the setup file by running the following command

	python setup.py install

##Run the application by the following command in the terminal
	./nerdirc

##Deactivating virtualenv

When done working with the virtual environment, deactivate it by running following command.

	deactivate
