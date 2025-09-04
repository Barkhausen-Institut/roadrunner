{ python310, lua, pkg-config, mkShell }:
let
  pypkg = python-packages: with python-packages; [
    pyyaml
    lupa
    psutil
    typing-extensions
    pytest
  ]; 
  py = python310.withPackages pypkg;
in mkShell {
  packages = [
    py
    lua
  ];
  nativeBuildInputs = [
      pkg-config
  ];
  shellHook = ''
    export PATH=$PATH:$PWD/bin
    export PYTHONPATH=$PWD
    #create a link to the python3 that can be selected as interpreter in vscode
    if [ -d .vscode ]; then
      ln -fs ${py}/bin/python3 .vscode/py3
    fi
  '';
}
