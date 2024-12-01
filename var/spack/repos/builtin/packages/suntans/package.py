# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Suntans(MakefilePackage):
    """The Stanford unstructured-grid,
    nonhydrostatic, parallel coastal
    ocean model."""

    homepage = "https://github.com/ofringer/suntans"
    url = "https://github.com/ofringer/suntans/archive/master.zip"

    maintainers("ofringer", "zyaj", "mrayson", "jadelson", "lhxone")

    license("LGPL-2.1-or-later")

    version("3.1", sha256="9b5d0dee5502a5650e37bf72f64b1124be86c084e7408aa517c214ddb25e36de")

    depends_on("libx11@1.6.3")
    depends_on("mpi")

    def edit(self, spec, prefix):
        env["MPIHOME"] = spec["openmpi"].prefix
        with working_dir("main"):
            makefile = FileFilter("Makefile")
            makefile.filter("XINC=.*", "XINC= -I{0}".format(spec["libx11"].prefix.include))
            makefile.filter("XLIBDIR = .*", "XLIBDIR = {0}".format(spec["libx11"].prefix.lib))
            makefile.filter(
                "INCLUDES = .*",
                "INCLUDES=$(PARMETISINCLUDE)$(TRIANGLEINCLUDE)$(NETCDFINCLUDE)$(XINC)",
            )

    def build(self, spec, prefix):
        with working_dir("main"):
            make("sunplot")

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        mkdir(prefix.include)
        with working_dir("main"):
            install("sunplot", prefix.bin)
            install("*.h", prefix.include)
