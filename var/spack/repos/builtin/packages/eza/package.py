# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Eza(CargoPackage):
    """A modern, maintained replacement for ls."""

    homepage = "https://github.com/eza-community/eza"
    url = "https://github.com/eza-community/eza/archive/refs/tags/v0.15.3.tar.gz"

    maintainers("trws")

    license("EUPL-1.2", when="@0.20:", checked_by="pranav-sivaraman")
    license("MIT", when="@:0.19", checked_by="pranav-sivaraman")

    version("0.20.4", sha256="5f25e866521c310d9530b9bbabeb288ad8d9cd208adee79582dde79bdd51c470")
    version("0.15.3", sha256="09093e565913104acb7a8eba974f8067c95566b6fbedf31138c9923a8cfde42f")

    depends_on("rust@1.70:", when="@0.15.3:")
    depends_on("c", type="build")

    @run_after("install")
    def install_completions(self):
        package_completions_path = f"{self.stage.source_path}/completions"

        mkdirp(bash_completion_path(self.prefix))
        copy(f"{package_completions_path}/bash/eza", bash_completion_path(self.prefix))

        mkdirp(zsh_completion_path(self.prefix))
        copy(f"{package_completions_path}/zsh/_eza", zsh_completion_path(self.prefix))

        mkdirp(fish_completion_path(self.prefix))
        copy(f"{package_completions_path}/fish/eza.fish", fish_completion_path(self.prefix))
