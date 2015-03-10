Description
-----------
Need to work on a new feature or bug-fix and want a seperate development environment. Sick of cloning again and again. Sick of making `virtual envs` and running `setup.py develop`. With **mmdev_boostrap**  just clone once and by making using use of `bzr` branches make the most of it. Keep updated for the changes and create seperate environments instantly without any chaos.

**mmdev_bootsrap** automates settting up of `mailman-core`, `mailman-client`,`postorius` and `postorius-standalone` for both usage and development purposes.

- Highly interactive, customise your paths of installation at each step.
- Checks for updates while creating a new branch for development.
- Creates and manages virtual envs automatically for `python2` and `python3`.

Setting Up
-----

	`git clone https://github.com/black-perl/mmdev_bootstrap.git
	cd mmdev_bootstrap/`

Usage
-----
Supply the virtual env folder path as command-line argument. If not supply will create the virtual environments in the current directory.


	`
	python mmdev_boostrap.py <path-for-virtual-envs-installation>
	`



