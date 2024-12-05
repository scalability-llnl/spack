# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Beakerlib(MakefilePackage):
    """BeakerLib is a shell-level integration testing library, providing
    convenience functions which simplify writing, running and analysis
    of integration and blackbox tests."""

    homepage = "https://github.com/beakerlib/beakerlib"
    url = "https://github.com/beakerlib/beakerlib/archive/1.20.tar.gz"

    license("GPL-2.0-only")

    version("1.29.3", sha256="f792b86bac8be1a4593dd096c32c1a061102c802c6f5760259a5753b13f6caa1")
    version("1.20", sha256="81f39a0b67adff4c3f4c051ffd26bcf45e19068dee7e81e3b00ee4698587f4e9")
    version("1.19", sha256="4dcaddf70a057ea5810c967cf5194d11850c8b5263ca25533e9e381067288460")
    version("1.18.1", sha256="65e6f81f17fd87f9db783d0b7a7216387a337f4692d3d9e1c40ef427d977c3d5")

    def install(self, spec, prefix):
        make("DESTDIR={0}".format(prefix), "PKGDOCDIR=", "install")
