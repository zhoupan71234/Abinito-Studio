# Install

Firstly, you need a python compiler. Here we recommend the Anaconda Individual Edition(https://www.anaconda.com/).

Our software package use the PyQt5 to create graphical user interface(GUI). However, other python-related softwares, such as spyder, also strongly depend on PyQT5 and its version. Therefore, we strongly suggest the user build a new virtual environment to install Abinito Studio because we only test the special version of PyQT5. You can build a new environment by

	conda create -n abinito python=3.7

Then you can activate the environment with 

	conda activate abinito

In order to decide the environment is created or not, you can use 

	conda info -e

to watch all environments created in your Anaconda.


Our software packages depend on PyQT5, Pymatgen, Mayavi and so on. To be able to easily install other dependencies of python packages, the user can use the install.py to automatic install all need packages.

After installing all these dependencies, we can start the GUI from Anaconda Powershell Prompt with 

	cd /destination_directory/AbinitoStudio-x.x( x.x is the number of version)
	python ./appMain.py

