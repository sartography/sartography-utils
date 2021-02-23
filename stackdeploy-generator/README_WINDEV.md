
The following has been tested in Windows 10 Pro, Version 10.0.18363 Build 18363. All CLI commands were run in a regular user powershell.


1. You will need to set up python 3, git for windows and/or GitHub desktop, and docker desktop, which needs WSLv2. You will also need the sartography-utils repository which contains the stack deploy generator.
2. After you set up git for windows, make sure to set the following command: `git config --global core.autocrlf false`
3. Clone the repository you want to work on (for example, cr-connect-workflow). 
4. Build the docker image for that repository. For example, with cr-connect, we could do:
	1. cd to the repository
	2. build the image locally with a custom tag i.e. `cr-connect-workflow-windev`
	   The command to do this is: `docker build -t cr-connect-workflow-windev .`
   	   The first time you do this, it may take some time. Subsequent builds for cr-connect-workflow should happen almost instantly, unless you purge your docker image cache.
5. Generate an appropriate docker compose file from the stackdeploy generator. For example you can run `.\stackdeploy-generator.py -F .\cr_connect_windev\ -c windev.yml`
   * You can customize your template or your parameters as you wish, please see the README.MD file for the stackdeploy generator.
6. Run your docker compose with `docker-compose.exe -f windev.yml up`
7. You should see the results of your code changes in a fully functional development environment. Additionally, in your powershell, you can see the various log outputs as requests come in.

