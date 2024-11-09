# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Njet(AutotoolsPackage):
    """NJet is a library for multi-parton one-loop matrix elements
    in massless QCD."""

    homepage = "https://bitbucket.org/njet/njet/wiki/Home"
    url = "https://bitbucket.org/njet/njet/downloads/njet-2.1.1.tar.gz"

    tags = ["hep"]

    license("GPL-3.0-or-later")

    version("2.1.1", sha256="3858ad37e84f3652711aa033819a6566352ecff04a1cb0189d6590af75b7bb56")
    version("2.0.0", sha256="a1f5c171b8aff3553d9dde24d3ced5479bdaeec67f4c90c70a846ee3449b40ea")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("qd")

    patch("njet-2.0.0.patch", when="@2.0.0", level=0)

    def configure_args(self):
        args = [
            "--with-qd=" + self.spec["qd"].prefix,
            "FFLAGS=-ffixed-line-length-none -std=legacy",
        ]
        return args
