{ python311, mkShell }:
let
  pypkg = python-packages: with python-packages; [
    build
    twine
  ]; 
  py = python311.withPackages pypkg;
in mkShell {
  packages = [
    py
  ];
  shellHook = ''
    alias pybuild="python -m build"
    alias pyupload="python -m twine upload dist/*"
    printf "This shell can be used to publish the package to pypi\n"
    printf "  python -m build - aliased to pybuild\n"
    printf "  python -m twine upload dist/* - aliased to pyupload\n"
    printf "to use test.pypi add --repository testpypi to the upload command\n"
  '';
}
