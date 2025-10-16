# The Config Space

RoadRunner configures the description of the project in a data structure called the *config space*.
At its core this is a hierarchical structure of attribute sets, lists and leaf nodes holding values with standard basic types as bools, strings, integers, etc...
On top of that the config space defines some additional custom nodes to cross-link, dynamically generate values or load precalculated values into the data structure.

The config space of a project is rooted in a YAMl formated file in the root source directory.
The easiest way of visulizing it is therefore YAML.
A simple config space example could then be:

```yaml
module:
  sv:
    - mod1.sv
    - mod2.sv
simulation:
  tool: Icarus
  toplevel: Bench
  sv: Bench.sv
  inc: =;module
```

There is already a lot going on in this example, the meaning will be exmpained step by step.

## File Hierarchy

The root of the config space is loaded from a file called `RR` in the root direcrory of a project.
All file relative file specifications, for example source files, are considered relative to the RR file.
This becomes important when other RR files are included into the main, or any other RR file.
To include a file into the config space it is sufficent to start a value with `+#` followed by the file nane.
Because often RR files are included from a projects subdirectroy and carry the standard name i.e. `RR` a shortcut can be used to include those. The line  `subdir: +subdir` is equivalent to `subdir: +#subdir/RR`.
And because it is often a good idea to include a subdirectory to a config space node with the same name a even short version exists; `subdir: ++` is also equivalent to `subdir: +subdir` because with  `++` the directory name is derived directlyfrom the ky name.

```yaml
libs:
  ip: ++
  ip2: +weirdname
  ip3: +#dir/source.RR
```

## Config Space Paths

RoadRunner uses a pathing syntax, to describe positions in the config space, either as an absolute position, or relative to another location.
Paths are encoded as list of keys separated by modifiers.
A simple intuitive exmaple is the absoulte path `:simulation.toplevel` which points to the leaf node holdin the value `Bench` in the exmaple.
The two modifiers used here are `:` and `.`, that anchor the path at the root node and select a node's child, respecitvely.
Apart from these two there are a couple other modifiers:

 * `:` - go to root node
 * `.` - selelct child node
 * `;` - go to the root node of the current file (file includes are explained later)
 * `$` - invoke a special function or insert a context dependent variable (explainted later)

 The meaning of the *key* following the modifer depends on the modifier.
 In case of an anchor `:`, `.`, `;`, the key has to be an string matching a attribute of an attribute set, or a number matching an item in a list.
 An empty key is allowed and will *go one level up*.
 Consider for exmaple the line saying `inc: =;module`.
 Ignoring the `=` for a moment the path goes to the file root and then selects the attribute `module`.
 Being in the location `:simulation.inc` it would also  be possible to use a relative path: `...module`, going up twice and the selecting `module`. 
 In case of a function call `$` the key must be a defined special function or defined variable.

## Cross Links

The config space allows defining links across  config space nodes.
In the example the line `inc: =;module` creates such a link.
It is defined by starting a value with `=` followed by a path specifying the destianation of the link.
The link behaves similar to a symlink in Linux, meaning that in the exmple, getting the value of `:simulation.inc` is equivalent to to `:module`.
As a forward reference cross-links can also apply modifications to the context when used.
For example when changing the example line to `inc: ;module+opt~13` getting  `:simulation.inc` will still point to `:module` but the context will carry the variable `opt=13`.

## Variables

There are three ways how config space variables can be defined.
First RoadRunner will define several variables when accessing the config space.
These variables include amoung others information about the target (`SIMULATION`, `SYNTHESIS`), the tools being used (`XILINX`,`SYNOPSYS`,`VIVADO`,`ICARUS`,etc...).

Secondly, following cross-links may add variables to the current context by adding a list of variables separated by `+` to the end of the destination path.
Avariable can either be just defined, and will then be set to `True`, or can receive a boolean or numerical value by appanding the value separated with `~`.
Both integer and floating point values are allowed.
Exampled to variable appendixes are

* `+opt~13`
* `+flag+num~2`
* `+rat~0.12`

Thirdly, variables can be defined directly in the config space using the magic attribute `vars:`.
All attributes defined directly below a `vars:` node are inserted to each context that resides in a sibling or a decendent of such of the `vars:` node.
In general, multiple of those nodes can apply.
In the case of a variable collision, the one closer to the context's location shadows the others.
However, a variable can be defined *weak* by prepending a `?` to its definition to prevent it from shadowing higher variants.
Variables can be cross-links that can be used in paths with the `$` modifier.
The cross link will be evaluated from the position of its position.
Here is a example that showcases in config space defined variables.

```yaml
node1:
  vars:
    animal: kea
    tool: hammer
    link: =;value0
  value1: foo #here animal is defined as kea
  node2:
    vars:
      animal: raven #shadows kea
      ?tool: axe #weak, does not shadow
    value2: foo2 #animal=raven, tool=hammer 
    value3: =$link #links to :value0 because of the link variable
value0: bar # here animal is not defined
```

## Lua Integration

The config space includes a Lua engine to dynamically render content.
There are several placed that can make use of the integrated Lua interpreter.
All context variables are available to the Lua interpreter.

### Templates

All string values are considered Lua templates, thus can dynamically include values from variables or even more comple expressions.
RoadRunner uses the [etlua](https://github.com/leafo/etlua) templates.
A simple variable insertion looks like this: `This is a: <%- animal %>`.

### Expressions & Program

A config space leaf can be considered a Lua expression and evaluated as such by starting it with a single `$`.
When the value of the node is queried the expression is evaluated under the current context and the value returned.
It is possible to create dynamic values other than string, like the number of fingers: `$alien and 6 or 5`
that distinghuishes between an alien and not alien (human) hand.

Starting a leaf node with a double `$$` will consider the node to be a subprogram.
It is evaluated like a function and has to return the final value using the `return` statement.

The returned values can be Lua (nested) Tables that will be converted to a config space node hierarchy.
This way, whole subspaces of the config space can be generated.
However, this method is considered to reduce readability and conditional attributes sets should be preferred.

### Conditional Attribute Sets

Conditional attribute sets can be used to define the value of a node depending on the current context, which basically is the set of currently defined variables.
In a conditional attribute set the keys start with a `/` followed by a Lua expression.
When the value of the set is queried, all keys are evaluated.
For all key that evaluate to something other den `False` the assigned values are merged to form the dynamic value of the attribute set.
When mergin values the following rules apply:

* To merge two values they have to be of the same type (leaf, list, attr set).
* Merging leaf values, the first one is picked.
* Lists are appended
* attribute sets are merged deeply, meaning that all keys of both sets are in the result set; in case of a collision the values of the two sources are merged.

When evaluating conditional attribute set keys, the variable `default` is defined to be `true` to allow easy definition of a always included branch

```yaml
cond:
  /num == 5: # include foo:bar if num is 5
    foo: bar
  /default: # always include animal:monkey 
    animal: monkey
cond2:
  /blue: # 2 and 3 in list
    - 2
    - 3
  /red: # append 7 and 9
    - 7
    - 9
  # if neither red and blue are defined the value is None and throws an error
  # for lists use conditional list set 
```

### conditional list sets

Conditional list sets are very similar to normal conditional sets, but increase he convinience when dealing with lists.
In contrast, the keys must start with `/#`.
The computed value of a conditional list set is always a list.
Even if all keys evaluate to `False` the computed value will be a list, namely the empty list.
The values of all keys must be either list, but also can be leaf values.
Where lists will be concatted with the current list, leaf values will be appended.

```yaml
alist:
  /#blue: # two and three in list
    - 2
    - 3
  /#red: 7 # add 7 to the list
  #even is neither red and blue are defined this results in a valid (empty) list
```

### exclusive conditional sets

The exclusive variant of the conditional set will never merge values, but instead just takes the value of the first key that evaluates to a non-`False` value.
To desribe an exclusive conditional set, begin keys with `/?`.

```yaml
set:
  /?red:
    animal: monkey
  /?blue:
    tool: hammer
  # the result never contains keys animal and tool
  # when red is defined rendering stops after the first key and result only contains "animal: monkey"
```

