{
  description = "Roadrunner EDA tooling";

  inputs = {
    nixpkgs.url = github:NixOS/nixpkgs;
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        roadrunner = pkgs.callPackage ./roadrunner.nix {};
      in
      {
        devShells = {
          default = pkgs.callPackage ./shell.nix { };
          pypi = pkgs.callPackage ./pypi.nix { };
        };
        packages = {
          roadrunner = roadrunner;
          default = roadrunner;
        };
        apps = {
          unittest = pkgs.callPackage ./test.nix { inherit self; };
          single = pkgs.callPackage ./test.nix { inherit self; unittestArgs = "tests.test_tool_icarus.TestSim.test_vpi";};
        };
      }
    );
}
