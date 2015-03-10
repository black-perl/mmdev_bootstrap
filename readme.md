Description
-----------
Need to work on a new feature or bug-fix and want a seperate development environment. Sick of cloning again and again. Sick of making `virtual envs` and running `setup.py develop`. With **mmdev_boostrap**  just clone once and by making using use of `bzr` branches make the most of it. Keep updated for the changes and create seperate environments instantly without any chaos.

<img src="mmdev-bootstrap.png" alt="mmdev_boostrap" width="200" height="200" />

**mmdev_bootsrap** automates settting up of `mailman-core`, `mailman-client`, `postorius` and `postorius-standalone` for both `usage` and `development` purposes.

- Highly interactive, customise your paths of installation at each step.
- Checks for updates while creating a new branch for development.
- Creates and manages virtual envs automatically for `python2` and `python3`.
- Automatically tells you about any unavailable prerequisites.
- Automatically checks for internet connection.

Setting Up
-----
        $ git clone https://github.com/black-perl/mmdev_bootstrap.git
        $ cd mmdev_bootstrap/

Usage
-----
Supply the virtual env folder path as command-line argument. If not supply will create the virtual environments in the current directory. Use` python 2.7`.

       $ python2 mmdev_boostrap.py <path-for-virtual-envs-installation>

Modes of Usage
--------------
- **Scratch** : Download everthing from scratch and setup dev environments for the first time.
- **Fast** : Just `pull the changes` and create dev environments at blazing speed. Need to specify the `same directories` used earlier while using the script in `scratch` mode.


Sample-Usage
------------
- Create a directory which will contain the virtual environments for both the `mailman-core` and `postorius and rest`. 

        ank@bash-box ~
        >> cd Desktop/
        
        ank@bash-box ~/Desktop
        >> mkdir envs
- Now if you want to set up a dev environment for fixing a bug in mailman or want to work on a new feature ; create a directory for it too.

        ank@bash-box ~/Desktop
        >> mkdir mailman-fix
- Now create a directory where **mmdev_boostrap** will keep the one time cloned code. This will updated again and again for changes and will be used for create dev environments

        ank@bash-box ~/Desktop
        >> mkdir mailman-all

- 
**Note**: You can always ask **mmdev_bootstrap** to put things in the `current directory`.

- It is supposed you have cloned the **mmdev_bootstrap**.
- `cd` into `mmdev_boostrap` and you are ready to go.

        ank@bash-box ~/Desktop
        >> cd mmdev_bootstrap/
        
        ank@bash-box ~/Desktop/mmdev_bootstrap
        >> python mmdev_boostrap.py ../envs
- Just wait for **mmdev_boostrap** to interact with you and have a cup of tea. :coffee:
- It would look like this:


<img src='data/mmdev_bootstrap.gif' alt="mmdev_bootstrap-usage" height="240" width="320" />

- It will automatically start `mailman` and `postorius-standalone` for you.
- Head over to http://127.0.0.1:9090 and enjoy. :smiley:
- Next time when run with same `configuration` will let you create new dev environments at blazing speed because it will only pull the changes.

Make a push
------------
Now `cd` to `mailman-fix`, work and finally `push` your changes. The workflow is as simple as that.

Contribute
----------
Contributions are always welcomed. :smiley:

