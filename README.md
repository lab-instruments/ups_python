# ups_python
Python source for host based GUI

## HOW TO INSTALL

### PRE REQS
* Have Python installed (google "Python" and download/install for your operating system)
* Have git installed (google "Git" and download/install for your operating system)
* Create an account on Github.com

### INSTALL
1. Open Git. Pull down the code from Github by typing the following
    * git clone https://github.com/lab-instruments/ups_python.git
    you may be asked to signin to GitHub.com at this point. 
2. Navigate to the Python directory (search for "ups_python" in search bar or finder for folder)
    * cd ups_python
3. Open the "Python" folder. Setup the Python virtual environment using the provided script
    * Linux/Mac
      * source ./setup_venv.sh
    * Windows (double click on file in Python folder; command window will run; it takes a minute so be patient)p
      * setup_venv.cmd

   If netifaces fails to build during install, the Visual Studio build tools might need to be installed.
    * Download and run -- https://visualstudio.microsoft.com/thank-you-downloading-visual-studio/?sku=BuildTools&rel=16
    * Click the box that says Visual Studio build tools and install 
3. To launch the GUI
    * Windows (pick one)
      * From the command prompt (cmd.exe), activate the virtual environment and run 'python gui.py'
      * Run gui.cmd from the command prompt (cmd.exe)
      * Setup a shortcut to gui.cmd and put on desktop
    * Linux/Mac (pick one)
      * From the command prompt (bash), activate the virtual environment and run 'python gui.py'
      * Run gui.sh from the command prompt (bash)
