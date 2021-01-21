# stackdeploy-generator

This python utility helps bring up multiple stacks based on docker compose templates.
  
You can output to standard I/O and pipe the output to a script file (default), specify a script file to write to, or specify a docker compose output
The script files, when run, will export the correct envars for that stack. You can then use the docker compose template directly.
You can either make them executable with a `chmod +x` or run them through your shell
The latter will hard code your variable values into a docker compose file.

To add envars to the applicable command line arguments you can use an args file. This is a simple CSV with the following

```short,long,help,default,action,type,choices```, Short and long are mandatory

If you fill in `type` or `choices`, they will be `eval()`d.

You should also add some sane defaults so that you don't have to type in every parameter every time.  
This is a csv file with the format: ```PARAMETER, value```

port parameters are automagically searched for if your use a `port-range` cli argument.
path base in combination with the deployment identifier are needed for multiple stacks, to separate your docker volumes.

**NB**: there are several ports that are blocked by major browsers - and port 6000 is one of them so you may want to 
avoid that port range. for complete list:

[Blocked Port List](https://chromium.googlesource.com/chromium/src.git/+/refs/heads/master/net/base/port_util.cc)


## Built in arguments
| short | long              | description                                                           | default             | Required          |
|-------|-------------------|-----------------------------------------------------------------------|---------------------|-------------------|
| -F    | --folder          | A folder with args.csv, defaults.csv, and a docker-compose.yml        | None                | Yes or -af -df -t |
| -af   | --argfile         | CSV File with command line arguments to collect envars for a template | ./args.csv          | Yes or -F         |
| -df   | --defaults-file   | CSV File with sane default values for a template                      | ./defaults.csv      | Yes or -F         |
| -t    | --template        | A template for docker compose                                         | ./docker-compose.yml| Yes or -F         |
| -s    | --script          | Specifies an output script filename                                   | None                | No, can use STDIO |
| -c    | --docker-compose  | Specifies an output docker compose filename                           | None                | No, can use STDIO |
| -D    | --defaults        | Use sane defaults everywhere from defaults CSV File                   | True                | No                |

## Special arguments
| short | long                    | description                                                           | default                                                              |
|-------|-------------------------|-----------------------------------------------------------------------|----------------------------------------------------------------------|
| -i    | --deployment-identifier | Add a modifier to run multiple stacks                                 | None                                                                 |
| -P    | --path-base             | Path for your docker volumes                                          | $HOME/sartography/docker-volumes/cr-connect/<deployment_identifier>/ |

## Demo run:
### STDIO
```
./stackdeploy-generator.py -af ./cr_connect/args.csv -df ./cr_connect/defaults.csv --port-range 3000 -i a_stack
OR
./stackdeploy-generator.py -F ./cr_connect/ --port-range 3000 -i a_stack
```
### Script:
```
./stackdeploy-generator.py -af ./cr_connect/args.csv -df ./cr_connect/defaults.csv -t ./cr_connect/docker-compose.yml -s ./runme.sh --port-range 4000 -i b_stack
OR
./stackdeploy-generator.py -F ./cr_connect/ -s ./runme.sh --port-range 4000 -i b_stack
```
### Docker Compose File:
```
./stackdeploy-generator.py -af ./cr_connect/args.csv -df ./cr_connect/defaults.csv -t ./cr_connect/docker-compose.yml -c ./docker-compose-c.yml --port-range 7000 -i c_stack
or
./stackdeploy-generator.py -F ./cr_connect/ -c ./docker-compose-c_stack.yml --port-range 7000 -i c_stack
```
