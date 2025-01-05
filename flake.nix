{
  description = "Nix devshells";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-24.11";
  };

  outputs =
    { nixpkgs, ... }@inputs:
    let
      arch = "x86_64-linux";
      pkgs = nixpkgs.legacyPackages."${arch}";
    in
    {
      devShells."${arch}" = {
        default = pkgs.mkShell {
          # Python dev env
          packages = with pkgs; [ python312 python312Packages.tkinter ];
        };
        tex = pkgs.mkShell {
          # LaTeX dev env
          packages = with pkgs; [ texliveFull pandoc ];
        };
      };
    };
}