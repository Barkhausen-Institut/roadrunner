####    ############
####    ############
####
####
############    ####
############    ####
####    ####    ####
####    ####    ####
############
############

from pathlib import Path
from roadrunner.config import ConfigContext, PathNotExist
from roadrunner.fn import etype, relpath
from roadrunner.help import HelpItem, HelpOption, HelpProxy, HelpArg
from roadrunner.rr import Call, Pipeline, asset
import roadrunner.modules.verilog
import roadrunner.modules.cpp
import roadrunner.modules.files


NAME = "Verilator"
HelpItem("tool", NAME, "Verilator Simulator")

DEFAULT_FLAGS = ['VERILATOR', 'DPI']

HelpItem("command", (NAME, "run"), "run Verilator lint check", [
    HelpProxy("function", (NAME, "do_compile")),
    HelpProxy("module", ("files", "share")),
    HelpProxy("module", ("files", "handleFiles")),
    HelpOption("attribute", "check", "bool", "true", "run the logchecker"),
    HelpProxy("function", (NAME, "do_check"))
])
def cmd_run(cfg:ConfigContext, pipe:Pipeline, vrsn:str) -> int:
    etype((cfg,ConfigContext), (pipe,Pipeline), (vrsn,(str,None)))
    wd = pipe.initWorkDir()

    flags = cfg.get('.flags', mkList=True, default=[]) + DEFAULT_FLAGS
    fcfg = cfg.move(addFlags=set(flags))

    check = fcfg.get('.check', default=True, isType=bool)

    with pipe.inSequence("verilator"):

        roadrunner.modules.files.share(fcfg, pipe)
        roadrunner.modules.files.handleFiles(fcfg, wd, pipe)

        do_compile(fcfg, wd, vrsn, pipe)

        call = Call(wd, 'simulation', NAME, vrsn)
        call.addArgs(['obj_dir/VSim'])
        pipe.addCall(call)

        if check:
            do_check(wd, pipe)

    return 0
HelpItem("command", (NAME, "lint"), "run Verilator lint check", [
    HelpProxy("function", (NAME, "do_compile")),
    HelpProxy("module", ("files", "share")),
    HelpProxy("module", ("files", "handleFiles"))
])
def cmd_lint(cfg:ConfigContext, pipe:Pipeline, vrsn:str) -> int:
    etype((cfg,ConfigContext), (pipe,Pipeline), (vrsn,(str,None)))
    wd = pipe.initWorkDir()

    with pipe.inSequence("lint"):

        roadrunner.modules.files.share(cfg, pipe)
        roadrunner.modules.files.handleFiles(cfg, wd, pipe)

        do_compile(cfg, wd, vrsn, pipe, lint=True)

    return 0

HelpItem("function", (NAME, "do_check"), "run logcheck", [])
def do_check(wd:Path, pipe:Pipeline):
    with open(wd / "logcheck.py", "w") as fh:
        print(asset(Path('rr/logcheck.py')).source, file=fh)
    call = Call(wd, 'logcheck', "Python3")
    call.addArgs(['python3', 'logcheck.py', 'simulation.stdout'])
    pipe.addCall(call)

def do_compile(cfg:ConfigContext, wd:Path, vrsn:str, pipe:Pipeline, lint:bool=False) -> int:
    etype((cfg,ConfigContext), (wd,Path), (vrsn,(str,None)), (pipe,Pipeline), (lint,bool))

    toplevel = cfg.get('.toplevel', isType=str)

    envfile = roadrunner.modules.verilog.writeEnvFile(wd, {})

    do_VerilogFiles(cfg, wd, pipe, [relpath(envfile, wd)])
    do_DpiModules(cfg, wd, pipe)


    call = Call(wd, 'verilator', NAME, vrsn)
    call.addArgs(['verilator', '--cc'])
    if lint:
        call.addArgs(['--lint-only'])
    else:
        call.addArgs(['--binary'])
    # TODO this should be loaded from attributes
    call.addArgs(['--trace'])
    call.addArgs(['--timing'])
    call.addArgs(['-Wno-TIMESCALEMOD'])
    call.addArgs(['--top-module', toplevel])
    call.addArgs(['-o', 'VSim'])
    call.addArgs(['-f', 'sources.cmd'])
    call.addArgs(['-f', 'dpiModules.cmd'])

    pipe.addCall(call)

    return 0

def do_VerilogFiles(cfg:ConfigContext, wd:Path, pipe:Pipeline, addFiles:list=[]):
    etype((cfg,ConfigContext), (wd,Path), (pipe,Pipeline), (addFiles, list, Path))
    lst = roadrunner.modules.verilog.includeFiles(cfg.move(), wd)

    files = addFiles[:]
    defs = set()
    incs = set()
    for itm in lst:
        for fname in itm.sv + itm.v:
            if fname not in files:
                files.append(fname)
        for d in itm.defines:
            defs.add(d)
        for inc in itm.path:
            incs.add(inc)

    with open(wd / 'sources.cmd', 'w') as fh:
        for d in defs:
            print(f"-D{d}", file=fh)
        for fname in files:
            print(f"{fname}", file=fh)
        for inc in incs:
            print(f"-I{inc}", file=fh)

def do_DpiModules(cfg:ConfigContext, wd:Path, pipe:Pipeline):
    etype((cfg,ConfigContext), (wd,Path), (pipe,Pipeline))

    used = []

    with open(wd / 'dpiModules.cmd', 'w') as fh:
        for vnode in cfg.travers():
            node = vnode.real()
            try:
                dpiMod = node.move(".dpiModule")
            except PathNotExist:
                continue
            if node.pos() in used:
                continue
            used.append(node.pos())
            for itm in roadrunner.modules.cpp.includeFiles(dpiMod, wd):
                for path in itm.path:
                    print(f'-CFLAGS -I../{path}', file=fh)
                for lib in itm.libpath:
                    print(f'-CFLAGS -L../{lib}', file=fh)
                for lib in itm.lib:
                    print(f'-CFLAGS -l{lib}', file=fh)
                if itm.std is not None:
                    print(f'-CFLAGS -std={itm.std}', file=fh)
                print(*map(str, itm.c), sep='\n', file=fh)
                print(*map(str, itm.cpp), sep='\n', file=fh)
