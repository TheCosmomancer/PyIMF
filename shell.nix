{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = with pkgs; [
    python313Packages.peewee
    python313Packages.cryptography
    python313Packages.tkinter
    python313Packages.levenshtein
    python313Packages.nltk
  ];
}
