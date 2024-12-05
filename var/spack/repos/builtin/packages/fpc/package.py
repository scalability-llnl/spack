# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Fpc(Package):
    """Free Pascal is a 32, 64 and 16 bit professional Pascal compiler."""

    homepage = "https://www.freepascal.org/"
    url = "https://downloads.sourceforge.net/project/freepascal/Linux/3.0.2/fpc-3.0.2.x86_64-linux.tar"

    license("GPL-2.0-or-later AND LGPL-2.1-or-later")

    version("3.0.2", sha256="b5b27fdbc31b1d05b6a898f3c192d8a5083050562b29c19eb9eb018ba4482bd8")

    def install(self, spec, prefix):
        install = Executable("./install.sh")

        # Questions:
        #
        # Install prefix:
        # Install Textmode IDE (Y/n) ?
        # Install documentation (Y/n) ?
        # Install demos (Y/n) ?

        install_answers = ["%s\n" % prefix, "Y\n", "Y\n", "n\n"]

        install_answers_filename = "spack-install.in"

        with open(install_answers_filename, "w") as f:
            f.writelines(install_answers)

        with open(install_answers_filename, "r") as f:
            install(input=f)
