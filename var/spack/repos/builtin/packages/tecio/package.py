# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Tecio(CMakePackage):
    """The TecIO library allows third-party applications to read and write
    Tecplot file format."""

    homepage = "https://www.tecplot.com/products/tecio-library/"
    #url = "file://{}/tecio.tgz".format(os.getcwd())
    url = "file:///aerolab/admin/software/dist/tecplot/tecio.2023.1.1.tgz"

    manual_download = True

    maintainers("snehring")

    version("2023.1.1", sha256="1468430e3cf6f019175da2559e63c5d6cf61c8569a3e994890448d1c6f7aa1f3")


    #depends_on("cmake@3.0.2:", type="build")

    #depends_on("boost@1.69.0:+system", type="build")
    depends_on("boost", type="build")
    depends_on("mpi", when="+mpi")

    variant("mpi", default=False, description="Build tecio with mpi support.")

    @property
    def root_cmakelists_dir(self):
        if self.spec.satisfies("+mpi"):
            return "teciompisrc"
        else:
            return "teciosrc"

    def install(self, spec, prefix):
        includes = [
            "StandardIntegralTypes.h",
            "TECIO.h",
            "tecio_Exports.h",
            "tecio.inc",
            "tecio.for",
            "tecio.f90",
        ]
        mkdirp(join_path(prefix, "include"))
        mkdirp(join_path(prefix, "lib"))
        mkdirp(join_path(prefix, "bin"))
        with working_dir(self.root_cmakelists_dir):
            for f in includes:
                install(f, prefix.include)
            install("tecio_license_agreement.txt", prefix)
        with working_dir(self.build_directory):
            install("szcombine", prefix.bin)
            if spec.satisfies("+mpi"):
                install("libteciompi.a", prefix.lib)
            else:
                install("libtecio.a", prefix.lib)
