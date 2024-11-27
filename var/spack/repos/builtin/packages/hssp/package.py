# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.pkg.builtin.boost import Boost


class Hssp(AutotoolsPackage):
    """The source code for building the mkhssp and hsspconv programs is bundled
    in the hssp project.

    The mkhssp executable creates stockholm files with hssp annotations in
    them. The hsspconv executable converts stockholm to the original hssp
    format.
    """

    homepage = "https://github.com/cmbi/hssp"
    url = "https://github.com/cmbi/hssp/archive/3.0.10.tar.gz"

    license("GPL-3.0-or-later")

    version("3.1.5", sha256="9462608ce6b5b92f13a3a8d94b780d85a3cac68ab38449116193754cc22dc5d0")
    version("3.0.10", sha256="9b2cba9c498e65fd48730f0fc86ca2b480bf12903a2c131521023f3a161fe870")
    version("3.0.9", sha256="2f67743ffd233ed9c4cd298e8fc65a332b863052945fb62bd61d7f1776274da9")
    version("3.0.8", sha256="56c926d2e43a3dd6324de558dde868751355f385d1b60fd85586a0a2c2bc82e0")
    version("3.0.7", sha256="3f1c09eb2cdc679119375a9ee552f853bcd1e959f030cb67ca6bd33809e6cdf2")
    version("3.0.6", sha256="8d3bc75bd9513dd0800a630049969639758692e42a28028651543320cce70d5f")
    version("3.0.5", sha256="8ca1de53e8add9e7af18a9f565bbcfa388f4d6ddcd2b7a1eae668c836ec0d09c")
    version("3.0.4", sha256="67a39d325ce9c17a416a26172fd5ae28878be3557cd611d7cbb9bcaf09507e76")
    version("3.0.3", sha256="42fc2b293fc60407ae097cc8021fd7cf0044092aa366c11ee99015beec83beea")
    version("3.0.2", sha256="76b4275c8cde120509d7920609fca983f2b04249a649d0aa802c69fd09e5f8cf")
    version("3.0.1", sha256="62a703d15bdfec82fdbd2a4275e1973b6a1ac6ccd4dbec75036f16faacaa9dce")

    depends_on("cxx", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("boost@1.48:")
    depends_on(Boost.with_default_variants)

    def configure_args(self):
        args = ["--with-boost=%s" % self.spec["boost"].prefix]
        return args

    @run_after("configure")
    def edit(self):
        makefile = FileFilter(join_path(self.stage.source_path, "Makefile"))
        makefile.filter(".*-Werror .*", "                    -Wno-error \\")
