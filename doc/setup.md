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

### VEnv

### Environment Modules / lmod

### Container