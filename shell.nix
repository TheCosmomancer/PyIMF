{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = with pkgs; [
    python312Packages.peewee
    python312Packages.xattr
    python312Packages.cryptography
    python312Packages.tkinter
    figlet
  ];
}
