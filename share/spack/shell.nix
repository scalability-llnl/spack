{ pkgs ? (import <nixpkgs> {}) }:

with pkgs; stdenv.mkDerivation {

  buildInputs = [
    python3
    gnupg

    # fortran compiler not exposed by standard environment
    gfortran
    gfortran.cc.lib

    # external packages to pass to spack
    openjdk11_headless
    bazel_4
  ];

  name = "spack-shell";
  shellHook = ''
    source ${toString ./.}/setup-env.sh
    spack external find openjdk
    spack external find bazel
  '';
}
