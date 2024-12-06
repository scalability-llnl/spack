# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Ctpl(AutotoolsPackage):
    """CTPL is a template engine library written in C and distributed
    under the terms of the GNU GPL."""

    homepage = "https://github.com/b4n/ctpl"
    url = "https://github.com/b4n/ctpl/archive/0.3.tar.gz"

    license("GPL-3.0-only")

    version("0.3", sha256="034875ba8e1ce87b7ee85bc7146a6a2b2a6ac0518482b36d65eb67dd09c03d0a")

    depends_on("c", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("gettext", type="build")
    depends_on("gtk-doc")
    depends_on("glib@2.10:")

    def autoreconf(self, spec, prefix):
        bash = which("bash")
        bash("./autogen.sh")
