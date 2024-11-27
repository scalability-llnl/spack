# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Xmlf90(AutotoolsPackage):
    """xmlf90 is a suite of libraries to handle XML in Fortran."""

    homepage = "https://xmlf90.readthedocs.io/en/latest/"
    git = "https://gitlab.com/siesta-project/libraries/xmlf90"

    license("BSD-2-Clause")

    version("1.6.3", tag="1.6.3", commit="963fe5d11487233d43ac59dd0c1340a7b2cc3dc5")
    version("1.6.2", tag="1.6.2", commit="2be1d8d2253233093857e8555e50e74857d0bb51")
    version("1.6.1", tag="1.6.1", commit="773726675fc4290334444adcc76d9af96871f25f")
    version("1.6.0", tag="1.6.0", commit="36c64350138af1edfbbd8e0ce23b36a0ac8db617")
    version("1.5.6", tag="1.5.6", commit="c51a18e86b0d9e7d624509e799ee823c95f69fd1")
    version("1.5.5", tag="1.5.5", commit="166c0458750f973e2d6f86dd59738f3e3088295e")
    version("1.5.4", tag="xmlf90-1.5.4", commit="5b21b2c63c834adaa2327e22daa0c856644b2c75")
    version("1.5.3", tag="xmlf90-1.5.3", commit="d55a5bcf8a0d4e592a03585209435d342d8e6d0f")
    version("1.5.2", tag="xmlf90-1.5.2", commit="b238aec8719b7c40c7b7252c5f200818a0d5004a")

    depends_on("fortran", type="build")  # generated

    depends_on("autoconf@2.69:", type="build")
    depends_on("automake@1.14:", type="build")
    depends_on("libtool@2.4.2:", type="build")
    depends_on("m4", type="build")

    # Additional include directory specification required for Fujitsu compiler
    patch("fj_modmakefile.patch", when="%fj")

    @when("@1.5.2")
    def autoreconf(self, spec, prefix):
        sh = which("sh")
        sh("autogen.sh")

    def configure_args(self):
        if self.spec.satisfies("%gcc"):
            return ["FCFLAGS=-ffree-line-length-none"]
        return []

    @run_after("install")
    def fix_mk(self):
        install(join_path(self.prefix, "share", "org.siesta-project", "xmlf90.mk"), prefix)
