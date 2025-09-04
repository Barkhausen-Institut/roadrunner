import rrenv

with open(rrenv.template, "r") as fh:
    tpl = fh.read()

with open("message", "w") as fh:
    fh.write(tpl.format(animal=rrenv.animal))
