# Setup

In RoadRunner the information how to call a certain tool is decoupled from the project itself.
Instead loading the used tools in machine (or user) based configuration.
RoadRunner will load this information from a user specific and a global config location being:

```bash
~/.config/roadrunner
/etc/roadrunner
```

The main config file in both locations is the config.ini and is formated in the ini format as understood Python's stdlib ConfigParser.
It contains a section for every tool named after the tool which have to feature either the `exec` or the `execFile`.
Where the first specifies an inline tool loading script, the second points to a file containing the script.

## Tool Loading Script

The goal of a tool loading script is to create an environment in which the needed tool is available.
Technically the script has to act as an interpreter for a bash script and source the very script again.
Consider as an example a command script that calls the Icarus verilog compiler.

```bash
#! env/Icarus.sh

iverilog module.v
```

And then the tool loader script in env/Icarus.sh:

```bash
#!/usr/bin/env -S nix shell nixpkgs#verilog nixpkgs#gcc --command bash
source $@
```

Notice that the command script has a shebang and specifies the file `env/Icarus.sh` as its interpreter.
The tool loader script uses its own shebang to spawn a nix shell that has Icarus on board. It then calls the command script.

The tool loader script is specified in the `config.ini` and is copied over to `env` in the preparation phase.
It can be defined in an extra file with the content shown above:

```ini
[Icarus]
execFile = /home/user/.config/roadrunner/IcEnv.sh
```

> **NOTE**<br>
> Because the `ConfigParser` does not hint from which file an option was loaded relative paths do not work for `execFile` options. You must use absolute references.

or as inline script

```ini
[Icarus]
exec = #!/usr/bin/env -S nix shell nixpkgs#verilog nixpkgs#gcc --command bash\nsource $@
```

In ini files values have to be single lined but thanks to modification that RoadRunner applies `\n` are allowed to implement multiline scripts.

> **NOTE**<br>
> Notice that **only** the content of **only** the tool loader script is copied to a working directory. If you need to reference other files do so with absolut paths.

## Tool Variants

Sometimes it is necessary to specify multiple different versions of one tool.
RoadRunner allows to specify different versions by appending a version key after the tool name using a colon to load a specific version of a tool:

```ini
[Python3:crc]
exec = #!/usr/bin/env bash\nPATH=/opt/VEnv/crc/bin:$PATH\nsource $@
```

## Tool Loading Technics

Writing tool loader scripts is highly dependent on the local setup, preferred environment mangagement tool and potentially other things.
There are no recipies that will always work.
Nevertheless we will share some setups that have work for us in the past and maybe of value for other users as well.

### Nix

Nix can be used to prepare an environment to contain certain software.
in this example the created environment is assured to have git available

```ini
[Shell:git]
exec = #!/usr/bin/env -S nix shell nixpkgs#git --command bash\nsource $@
```

Unrolled to a file, the environment script look like this

```bash
#!/usr/bin/env -S nix shell nixpkgs#git --command bash
source $@
```

### VEnv

For Python programs it is often usefull to have dedicated VEnvs that contain all the libraries needed. This example created an environment that will use the python executable from a VEnv located at `/opt/VEnv/floogen`:

```ini
[Python3:floogen]
script = #!/usr/bin/env bash\nPATH=/opt/VEnv/floogen/bin:$PATH\nsource $@
```

### Environment Modules / lmod

Many setups using comercial software are using Environment or Lmod as environment manager.
The trouble with these both is that they are designed to work on interactive shells.
To make then work in scripts can differ a bit depending on the setup, however here is one example that worked somewhere:

```ini
[Vivado]
exec = #!/bin/bash\neval `$LMOD_CMD sh load Vivado`\nsource $@
```

The gist is that the `module` command that a user normaly runs ist actually a shell function that may not be available in script environments.

### Container

Roadrunners tool loading allows for mor sophisticated setups.
In this example we assume a machine that cannot run Synopsys VCS, beacause it runs Ubuntu which is not supported.
qFurther the tool is available from a NFS share mounted to the machine.
There is a contrainer image based on RockyLinux that is capable of running the tool.
The the configuration could be something like this

```ini
[VCS]
execFile = /home/mattis/.config/roadrunner/VCSEnv.sh
```
In `config.ini` we just link the file containing the script.
Global paths are necessary here because Pythons `ConfigParser` is unable to tell from which file an option comes.

```bash
#!/usr/bin/env bash
cat <<EOT > container.run
#!/usr/bin/bash
module add Synopsys/VCS
module add Synopsys/Verdi
cd /WD
source $1
EOT
chmod a+x container.run
docker run --rm -it -e DISPLAY \
-v /tmp/.X11-unix:/tmp/.X11-unix \
-v /opt/bi/hpc:/opt/bi/hpc:ro \
-v ./:/WD \
--user `id -u`:`id -g` \
meeseeks \
/WD/container.run $1
```

At runtime the script is copied into a working directory, so you cannot reference anything with relative paths.
This script first writes a file `container.run` which will be given to the container to execute.
In this script `module` is used to load `VCS` and `Verdi`.
It then switches to the working directory at `/WD` and executes the script given as param `$1`.

Then a docker container is started using the images `meeseeks`.
The NFS mounted software directory is mounted `-v /opt/bi/hpc:/opt/bi/hpc:ro`.
To support X11 windows, `-e DISPLY` is set and `-v /tmp/.X11-unix:/tmp/.X11-unix` is mounted.
Finally, the current directory, which is the working directory is mounted `-v ./:/WD` and the uid and gid are set to the current user ``--user `id -u`:`id -g` ``.
Beacause of the way Roadrunner prepares working directories for tools, the docker container now has everything to run VCS.


