# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class VtableDumper(MakefilePackage):
    """A tool to list content of virtual tables in a shared library."""

    homepage = "https://github.com/lvc/vtable-dumper"
    url = "https://github.com/lvc/vtable-dumper/archive/1.2.tar.gz"

    license("GPL-2.0-only")

    version("1.2", sha256="6993781b6a00936fc5f76dc0db4c410acb46b6d6e9836ddbe2e3c525c6dd1fd2")
    version("1.1", sha256="f0a57a7b82a0a56845cea9ab56ad449e63f5f01c6a0c9f1467efa4ef60dd4a93")
    version("1.0", sha256="a222de5a19bf716ab2f35148f43bbf8a052772b54ff622c6387a4ba2440fb9a0")

    depends_on("c", type="build")  # generated

    depends_on("libelf")

    def install(self, spec, prefix):
        make("prefix={0}".format(prefix), "install")
