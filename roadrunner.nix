{ python3Packages, lib }:

python3Packages.buildPythonApplication {
    pname = "roadrunner";
    version = lib.removeSuffix "\n" (builtins.readFile ./roadrunner/version);
    pyproject = true;

    src = ./.;

    buildInputs = [
        python3Packages.setuptools
    ];

    dependencies = with python3Packages; [
        lupa
        psutil
        pyyaml
    ];
    #typing-extensions
    #pytest
    
}