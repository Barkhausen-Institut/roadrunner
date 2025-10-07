# Usage

RoadRunner is a commandline tool that can be calld by `roadrunner` or `rr` for a short version.

Technically `rr` takes a single argument which specifies the *query*.
You could also call it subcommand, but the term command is already taken in RoadRunner.

All following arguments are passed to the query handler.

There are some global options, however.

## Global Options

Global options should be passed before the query identifier or they might end up being misinterpreted in the query handler.

* `--dir` Change to this directory before doing anything
* `--setup` Overwrite values in the `:_setup` subtree of the config space
* `--loglevel` set scope specific loglevels - this is actually a convienience function that could also be achieved with `--setup`

## Queries

### version

`rr version` prints the version of RoadRunner to stdout. It uses git to determine if the internally set version number matches a git label and might append a `-dev` if not.

### help

Prints information about tools, commands and queries.

When called without additional parameters, `rr help` prints a list of all tools that are registered in RoadRunner.
Each tool is presented by name, short description, a list of all commands and all queries it defines.

```shell
> rr help
--==---------------------------Tools----------------------------==--
Bender - Bender dependency manager
  commands: run
BuiltIn - builtin functions
  queries: jabberwocky, help, getval, get, invoke, version
  commands: jabberwocky
Icarus - Icarus Verilog
  commands: compile, sim, run
...
```

Giving the tool name as parameter will give more details about the specified tool.

```shell
> rr help BuiltIn
--==--------------------------ToolInfo--------------------------==--
BuiltIn - builtin functions
  queries:
    jabberwocky - prints the jabberocky poem
    help - prints info about the available tools
    getval - retrieves a value from the config space and prints it as python value
    get - get part of the config space and dumps it
    invoke - execute a command node. This is the main funtionallity of RoadRunner.
    version - put roadrunners version
  commands:
    jabberwocky - writes the jabberwocky poem into a file
--==                         (ToolInfo)                         ==--
```

Similar, giving the name of a query or command as second parameter, prints information about the selected topic.

```shell
> rr help BuiltIn jabberwocky
--==-------------------------Query Info-------------------------==--
BuiltIn.jabberwocky - prints the jabberocky poem
  --long -l - print the long version of the poem
  --fail -f - return a failing exit code from the query
  --noret -n - return None from the query
--==                        (Query Info)                        ==--
```

RoadRunner will prioritize the query if there is also a command with the same name.
Use `--cmd` to force help to show the command

```shell
> rr help BulitIn jabberwocky --cmd
--==------------------------Command Info------------------------==--
BuiltIn.jabberwocky - writes the jabberwocky poem into a file
  long (bool) default:False - writes to long version
  fail (bool) default:False - return a failing exitcode (-1)
  noret (bool) default:False - return nothing (None)
--==                       (Command Info)                       ==--
```

### invoke

The invoke query is the main query of RoadRunner as it calls a command definition from the confif space.
Invoke takes a single parameter which is a config path to the command definition to be executed.

Considering the standard exmaple: 

```yaml
modules:
mod1:
    sv: mod.sv
mod2:
    sv: mod2.sv
    inc: =...modules.mod1
mod3: +lib/mod3
simulation:
tool: Icarus #try "Vivado.sim"
top: Bench
sv: bench.sv
inc: =;modules.mod2
```

The command run the simulation would be: `rr invoke :simulation`.
Because invoke is used so often two simplifications can be applied.
For the path the leading global anchor `:` can be omitted.
The call `rr invoke simulation` is therefore equivalent.
Second, the query identifier `invoke` can be omitted as well, so that `rr simulation` is equivalent as well.
It has to be noticed, however, that RoadRunner first tries to find a query matching the first parameter.
Only if not query is found, it will assume `invoke` and use the parameter as path.

### get & getval

The `get` and `getval` queries can be used to read values from the config space, for exmaple to debug the configuration itself.
Both queries take a path to a node in the config space.
They will both retrieve the node and print it.
The difference is that, `get` will output the node raw, without applying dynamic content rendering and will format the value in a yaml similar style.

```shell
> rr get :modules.mod2
--==-----------------------Config Getter------------------------==--
.modules.mod2 #
sv: mod2.sv
inc: =....modules.mod1
--==                      (Config Getter)                       ==--
```

The query `getval` on the contrary will resolve all dynamic functions until it ends up with a pure Python data structure consisting of nested dicts, lists and simple leaf values like strings or ints.
It will output the final value as Python expression

```shell
> rr getval :modules.mod2
--==-----------------------Config Getter------------------------==--
(:modules.mod2):{'sv': 'mod2.sv', 'inc': {'sv': 'mod.sv'}}
--==                      (Config Getter)                       ==--
```

