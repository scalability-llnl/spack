# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Cunit(AutotoolsPackage):
    """Automated testing framework for 'C'."""

    homepage = "https://sourceforge.net/projects/cunit/"
    url = "https://sourceforge.net/projects/cunit/files/CUnit/2.1-3/CUnit-2.1-3.tar.bz2"

    license("GPL-2.0-or-later")

    version("2.1-3", sha256="f5b29137f845bb08b77ec60584fdb728b4e58f1023e6f249a464efa49a40f214")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
