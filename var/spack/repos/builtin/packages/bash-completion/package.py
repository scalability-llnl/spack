# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class BashCompletion(AutotoolsPackage):
    """Programmable completion functions for bash."""

    homepage = "https://github.com/scop/bash-completion"
    url = "https://github.com/scop/bash-completion/archive/2.3.tar.gz"
    git = "https://github.com/scop/bash-completion.git"

    license("GPL-2.0-or-later")

    version("develop", branch="master")
    version("2.12.0", sha256="5277d347481cb5a05399629f00b7deb4475fe71b8b4f8a219c360213e2113752")
    version("2.7", sha256="dba2b88c363178622b61258f35d82df64dc8d279359f599e3b93eac0375a416c")
    version("2.3", sha256="d92fcef5f6e3bbc68a84f0a7b063a1cd07b4000cc6e275cd1ff83863ab3b322a")

    depends_on("c", type="build")  # generated

    # Build dependencies
    depends_on("automake", type="build")
    depends_on("autoconf", type="build")
    depends_on("libtool", type="build")

    # Other dependencies
    depends_on("bash@4.1:", type="run")

    @run_before("install")
    def create_install_directory(self):
        mkdirp(join_path(self.prefix.share, "bash-completion", "completions"))

    @run_after("install")
    def show_message_to_user(self):
        prefix = self.prefix
        # Guidelines for individual user as provided by the author at
        # https://github.com/scop/bash-completion
        print("=====================================================")
        print("Bash completion has been installed. To use it, please")
        print("include the following lines in your ~/.bash_profile :")
        print("")
        print("# Use bash-completion, if available")
        print(f"[[ $PS1 && -f {prefix}/share/bash-completion/bash_completion ]] && \\")
        print(f"    . {prefix}/share/bash-completion/bash_completion")
        print("")
        print("=====================================================")
