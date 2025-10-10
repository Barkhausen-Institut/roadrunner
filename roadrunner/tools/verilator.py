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
from roadrunner.config import ConfigContext
from roadrunner.fn import etype, relpath
from roadrunner.help import HelpItem
from roadrunner.rr import Call, Pipeline, asset
import roadrunner.modules.verilog


NAME = "Verilator"
HelpItem("tool", NAME, "Verilator Simulator")

DEFAULT_FLAGS = ['VERILATOR']

def cmd_run(cfg:ConfigContext, pipe:Pipeline, vrsn:str) -> int:
    etype((cfg,ConfigContext), (pipe,Pipeline), (vrsn,(str,None)))
    wd = pipe.initWorkDir()

    flags = cfg.get('.flags', mkList=True, default=[]) + DEFAULT_FLAGS
    fcfg = cfg.move(addFlags=set(flags))

    with pipe.inSequence("verilator"):
        do_compile(fcfg, wd, vrsn, pipe)

        call = Call(wd, 'simulation', NAME, vrsn)
        call.addArgs(['obj_dir/VSim'])
        pipe.addCall(call)

        do_check(wd, pipe)

    return 0

HelpItem("function", (NAME, "do_check"), "run logcheck", [])
def do_check(wd:Path, pipe:Pipeline):
    with open(wd / "logcheck.py", "w") as fh:
        print(asset(Path('rr/logcheck.py')).source, file=fh)
    call = Call(wd, 'logcheck', "Python3")
    call.addArgs(['python3', 'logcheck.py', 'simulation.stdout'])
    pipe.addCall(call)

def do_compile(cfg:ConfigContext, wd:Path, vrsn:str, pipe:Pipeline) -> int:
    etype((cfg,ConfigContext), (wd,Path), (vrsn,(str,None)), (pipe,Pipeline))

    envfile = roadrunner.modules.verilog.writeEnvFile(wd, {})
    lst = roadrunner.modules.verilog.includeFiles(cfg.move(), wd)

    toplevel = cfg.get('.toplevel', isType=str)

    hist = set()
    defs = set()
    with open(wd / 'sources.cmd', 'w') as fh:
        print(f"{relpath(envfile, wd)}", file=fh)
        for itm in lst:
            for fname in itm.sv + itm.v:
                if fname in hist:
                    continue
                hist.add(fname)
                #TODO add and remove defines and includes
                #write file
                print(f"{fname}", file=fh)

    call = Call(wd, 'verilator', NAME, vrsn)
    call.addArgs(['verilator', '--cc', '--binary'])
    # TODO this should be loaded from attributes
    call.addArgs(['--trace'])
    call.addArgs(['-Wno-TIMESCALEMOD'])
    call.addArgs(['--top-module', toplevel])
    call.addArgs(['-o', 'VSim'])
    call.addArgs(['-f', 'sources.cmd'])

    pipe.addCall(call)


    return 0

