{ python3, writeShellApplication, self, unittestArgs ? "discover -s tests" }:
let
    pypkg = python-packages: with python-packages; [
        pyyaml
        lupa
        psutil
        typing-extensions
        coverage
    ]; 
    python = python3.withPackages pypkg;
    prog = writeShellApplication {
        name = "rrTest";
        text = ''
            cd ${self}
            ${python}/bin/python3 -m unittest ${unittestArgs}
        '';
    };
   
in {
    type = "app";
    program = "${prog}/bin/rrTest";
}


#            ${python}/bin/python3 -m roadrunner
