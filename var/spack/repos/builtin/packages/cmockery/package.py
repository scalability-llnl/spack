# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Cmockery(AutotoolsPackage):
    """A lightweight library to simplify and generalize the process of
    writing unit tests for C applications."""

    homepage = "https://github.com/google/cmockery"
    url = "https://github.com/google/cmockery/archive/v0.1.2.tar.gz"

    license("BSD-3-Clause")

    version("0.1.2", sha256="d40135ae9179201c01bde725fa64fc32d86b5899972e0ce4ad51668d261edbae")
    version("0.1.1", sha256="a801d17976f781fff6dc49042ff109e55ca4ebe8efb13757fa1a511ca52316be")
    version("0.1.0", sha256="9e017d48e56ab9d2ebcf5286fa54e37d42fe308d3c01fbc367793da2b9ad95e7")

    depends_on("c", type="build")  # generated

    depends_on("m4", type="build")
    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")

    def autoreconf(self, spec, prefix):
        bash = which("bash")
        bash("./autogen.sh")
