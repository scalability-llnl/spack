# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Ace(MakefilePackage):
    """ACE is an open-source framework that provides many components and
    patterns for developing high-performance, distributed real-time and
    embedded systems. ACE provides powerful, yet efficient abstractions
    for sockets, demultiplexing loops, threads, synchronization
    primitives."""

    homepage = "https://www.dre.vanderbilt.edu/~schmidt/ACE.html"
    url = "https://download.dre.vanderbilt.edu/previous_versions/ACE-6.5.1.tar.gz"

    license("DOC")

    version("7.1.4", sha256="a2bc358401178dd8175f4d826e60d23d901bfe38bc2fa0ac9275d01d7fda34bc")
    version("7.1.3", sha256="4cb82d8daf83f3abe50ac460b4fac9a8da2512f08d8efb4d327dcacd0b3929b3")
    version("7.1.0", sha256="d78d9f3f2dee6ccb46a8c296367369349054fd475dff3c5b36e2dff3dee0bf8f")
    version("6.5.12", sha256="de96c68a6262d6b9ba76b5057c02c7e6964c070b1328a63bf70259e9530a7996")
    version("6.5.6", sha256="7717cad84d4a9c3d6b2c47963eb555d96de0be657870bcab6fcef4c0423af0de")
    version("6.5.1", sha256="1f318adadb19da23c9be570a9c600a330056b18950fe0bf0eb1cf5cac8b72a32")
    version("6.5.0", sha256="b6f9ec922fbdcecb4348e16d851d0d1f135df1836dfe77d2e0b64295ddb83066")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    def edit(self, spec, prefix):
        # Dictionary mapping: compiler-name : ACE config-label
        supported = {"intel": "_icc", "gcc": ""}

        if not (self.compiler.name in supported):
            raise Exception(
                "compiler " + self.compiler.name + " not supported in ace spack-package"
            )

        env["ACE_ROOT"] = self.stage.source_path

        with working_dir("./ace"):
            with open("config.h", "w") as f:
                f.write('#include "ace/config-linux.h"\n')

        with working_dir(join_path(self.stage.source_path, "include/makeinclude")):
            with open("platform_macros.GNU", "w") as f:
                f.write(
                    "include $(ACE_ROOT)/include/makeinclude/"
                    "platform_linux" + supported[self.compiler.name] + ".GNU\n"
                )
                f.write(f"INSTALL_PREFIX={prefix}")
