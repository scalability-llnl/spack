# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Gengeo(AutotoolsPackage):
    """GenGeo is a library of tools for creating complex particle
    geometries for use in ESyS-Particle simulations. GenGeo is a standalone
    application with a Python API that creates geometry files suitable for
    importing into ESyS-Particle simulations. The functionality of GenGeo far
    exceeds the in-simulation geometry creation utilities
    provided by ESyS-Particle itself."""

    homepage = "https://launchpad.net/esys-particle/gengeo"
    url = "https://launchpad.net/esys-particle/trunk/3.0-alpha/+download/gengeo-163.tar.gz"

    maintainers("dorton21")

    license("Apache-2.0")

    version("163", sha256="9c896d430d8f315a45379d2b82e7d374f36259af66a745bfdee4c022a080d34d")

    depends_on("cxx", type="build")  # generated

    extends("python")

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")

    depends_on("boost+python")
    depends_on("openmpi")

    def autoreconf(self, spec, prefix):
        autogen = Executable("./autogen.sh")
        autogen()

    def configure_args(self):
        args = [
            "--verbose",
            "--with-boost=" + self.spec["boost"].prefix,
            "CCFLAGS=-fpermissive",
            "CXXFLAGS=-fpermissive",
        ]
        return args
