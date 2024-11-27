# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from glob import glob

from spack.package import *


class Cask(Package):
    """Cask is a project management tool for Emacs Lisp to automate the package
    development cycle; development, dependencies, testing, building,
    packaging and more."""

    homepage = "https://cask.readthedocs.io/en/latest/"
    url = "https://github.com/cask/cask/archive/v0.7.4.tar.gz"

    license("GPL-3.0-only")

    version("0.8.1", sha256="8739ba608f23c79b3426faa8b068d5d1bc096c7305ce30b1163babd354be821c")
    # version 0.8.0 is broken
    version("0.7.4", sha256="b183ea1c50fc215c9040f402b758ecc335901fbc2c3afd4a7302386c888d437d")

    depends_on("emacs", type=("build", "run"))

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("bin/cask", prefix.bin)
        install_tree("templates", join_path(prefix, "templates"))
        for el_file in glob("*.el"):
            install(el_file, prefix)
        for misc_file in ["COPYING", "cask.png", "README.md"]:
            install(misc_file, prefix)
        # disable cask's automatic upgrading feature
        touch(join_path(prefix, ".no-upgrade"))
