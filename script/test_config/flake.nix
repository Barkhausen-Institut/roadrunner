{
  description = "RoadRunner Shells";

  inputs = {
    nixpkgs.url = github:NixOS/nixpkgs;
    bender.url = "github:pulp-platform/bender";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils, bender }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        benderPkgs = bender.packages.${system};
      in
      {
        packages = {
          pyRRToolTest = pkgs.python3.withPackages (pp: with pp; [
            art
          ]);
          RRToolTest = pkgs.cowsay;
          git = pkgs.git;
          icarus = pkgs.symlinkJoin {
            name = "icarus";
            paths = [
              pkgs.iverilog
              pkgs.gcc
            ];
          };
          bender = benderPkgs.bender;
          python3 = pkgs.python3;
          sv-lang = pkgs.sv-lang;
          verilator = pkgs.symlinkJoin {
            name = "veril";
            paths = [
              pkgs.verilator
              pkgs.gcc
              pkgs.gnumake
              pkgs.findutils
            ];
          };
        };
      });
}