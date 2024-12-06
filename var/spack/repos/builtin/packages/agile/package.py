# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Agile(AutotoolsPackage):
    """AGILe is A Generator Interface Library (& executable), i.e. a uniform
    object oriented C++ interface for a variety of Fortran-based Monte Carlo
    event generators.."""

    homepage = "https://agile.hepforge.org/"
    url = "http://www.hepforge.org/archive/agile/AGILe-1.4.1.tar.gz"

    tags = ["hep"]

    maintainers("vvolkl")

    license("GPL-2.0-only")

    version("1.5.1", sha256="e38536300060e4b845ccaaed824c7495944f9117a0d7e4ee74a18bf278e2012f")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("hepmc")
    depends_on("boost")

    def configure_args(self):
        options = [
            "--prefix=%s" % self.spec.prefix,
            "--with-hepmc=%s" % self.spec["hepmc"].prefix,
            "--with-boost=%s" % self.spec["boost"].prefix,
            "--disable-pyext",  # probably only works with python2
            "CFLAGS=-g0 -O2",
            "CXXFLAGS=-g0 -O2",
            "FFLAGS=-g0 -O2",
        ]
        return options
