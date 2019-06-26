
# Sports Catalog Project
This is a web server for allowing access to a catalog of sports equipment 
It features:
* A catalog of sporting equipment.
* Oauth2 authentication.
* Ability for the user to add and edit entries they have created after authenticated.

------------------------------
## Prerequisites
* [VirtualBox](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1)
	* Install the version for your operating system. You do not need to launch VirtualBox after running it
* [Vagrant](https://www.vagrantup.com/downloads.html)
	* Install the version for your operating system.
	* If the installer asks you to grant network permissions or make a firewall exeption, be sure to allow this.
* Install the VM configuration.
	* Download [FSND-Virtual-Machine.zip](https://s3.amazonaws.com/video.udacity-data.com/topher/2018/April/5acfbfa3_fsnd-virtual-machine/fsnd-virtual-machine.zip)
	* Unzip the file and `cd` into its directory and `cd` into the vagrant directory.
	* run the command `vagrant up` to install the Linux virtual machine.
------------------------------
## Installation
The `catalog` folder should be placed in the `vagrant` directory, which is shared with your virtual machine.

-----------------------------------
## Usage
* `cd` to the location of your Vagrant VM.
* log into vagrant with `vagrant ssh`.
* `cd` to the location of your `vagrant/catalog` directory.
* run `python catalog_database.py` to create the database.
* run `python catalog.py` to start the server.
* visit the server in a browser at https://localhost:8000.
* perform a `GET` at https://localhost:8000/api/v1 to recieve a json of all items in catalog.
* perform a `GET` at https://localhost:8000/api/v1/<category>/<item> to recieve a json of a single item.

------------------------------------
## Authors
Zachary Dumas - https://github.com/zacharydumas

----------------------------------
## Acknowledgements
Installation instructions for prerequisites comes from [Udacity](https://www.udacity.com/)