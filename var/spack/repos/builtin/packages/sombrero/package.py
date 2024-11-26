# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from os import symlink

from spack.package import *


class Sombrero(MakefilePackage):
    "A next-generation conjugate gradient benchmark from computational particle physics"

    homepage = "https://github.com/sa2c/sombrero"
    url = "https://github.com/sa2c/sombrero/archive/refs/tags/1.0.tar.gz"

    license("GPL-2.0-only")

    version(
        "2021-08-16", sha256="f62aa1934fef6a025449a9e037345043072be6198f92087853c58c67f1342f73"
    )
    version(
        "2021-07-31", sha256="9c59693f330904b1f444187d1974a179c61d801f063581acb94a7a77955151e0"
    )
    version(
        "2021-07-14", sha256="d2801a4efea312a14fc34775b0dea862e958ccb9b7721a63b6c29e1224e12257"
    )
    version(
        "2021-07-08", sha256="816b0f0a684a421fa620f11c21649ac162e85d1febd6a7e10cfd07604760c0d6"
    )
    # Version 1 is incompatible with spack
    # as CFLAGS and the like are hardcoded in the makefile.
    version(
        "1.0",
        sha256="423a631c86f0e5f14dea186228871099ca0374dc07bf1bb24b6be17f79784682",
        deprecated=True,
    )

    depends_on("c", type="build")  # generated

    depends_on("mpi")

    maintainers("mmesiti", "edbennett")

    def edit(self, spec, prefix):
        # Make the `sombrero.sh` driver relocatable
        sombrero_sh = FileFilter(join_path(self.stage.source_path, "sombrero.sh"))
        sombrero_dir = join_path(prefix.bin, "sombrero")
        sombrero_sh.filter("sombrero/", "{0}/".format(sombrero_dir))

    def install(self, spec, prefix):
        sombrero_dir = join_path(prefix.bin, "sombrero")
        mkdirp(sombrero_dir)
        # Install the shell driver
        install("sombrero.sh", prefix.bin)
        # Install all executables
        for i in range(1, 7):
            src = join_path("sombrero", "sombrero{0}".format(i))
            install(src, sombrero_dir)
            symlink(
                join_path(sombrero_dir, "sombrero{0}".format(i)),
                join_path(prefix.bin, "sombrero{0}".format(i)),
            )
