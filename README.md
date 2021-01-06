# ups_python
Python source for host based GUI

## HOW TO INSTALL

### PRE REQS
* Have Python installed
* Have git installed

### INSTALL
1. Pull down the code from Github
    * git clone https://github.com/lab-instruments/ups_python.git
2. Navigate to the Python directory
    * cd ups_python
3. Setup the Python virtual environment using the provided script
    * Linux/Mac
      * source ./setup_venv.sh
    * Windows
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
