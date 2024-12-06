# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Heputils(MakefilePackage):
    """Generic tools for high energy physics, e.g. vectors, event records,
    math and other util functions."""

    homepage = "https://bitbucket.org/andybuckley/heputils/src/default/"
    url = "https://bitbucket.org/andybuckley/heputils/get/heputils-1.3.2.tar.gz"

    tags = ["hep"]

    license("GPL-3.0-only")

    version("1.3.2", sha256="be43586979ab1a81a55348d795c2f63a5da19fc6367d5f66f354217c76c809c0")
    version("1.3.1", sha256="7f33ef44364a3d3a39cc65005fb6aa9dfd06bd1b18b41151c0e5e3d28d6ba15b")
    version("1.3.0", sha256="1ec9d9d71d409ce6b2e668e4927b1090ddf2ee9acf25457f767925cf89b24852")
    version("1.2.1", sha256="99f0b27cddffb98977d37418d53f3386e5defda547aeb4c4fda00ab6fcf2cc31")
    version("1.2.0", sha256="0f9f96bd7589f9aec8f1271524b8622291216fe2294ffed772b84d010759eaef")
    version("1.1.0", sha256="671374641cdb6dc093327b69da2d2854df805b6eb8e90f0efefb0788ee4a2edd")
    version("1.0.8", sha256="9b9a45ebff1367cd2ab1ec4ee8c0e124a9b7ed66c75d8961412163ade1962d91")
    version("1.0.7", sha256="481a26755d4e2836563d1f8fcdad663bfa7e21b9878c01bd8a73a67876726b81")
    version("1.0.6", sha256="1ecd8597ef7921a63606b21136900a05a818c9342da7994a42aae768ecca507f")
    version("1.0.5", sha256="efff3d7d6973822f1dced903017f86661e2d054ff3f0d4fe926de2347160e329")
    version("1.0.4", sha256="aeca00c1012bce469c6fe6393edbf4f33043ab671c97a8283a21861caee8b1b4")
    version("1.0.3", sha256="8e7ebe0ad5e87a97cbbff7097092ed8afe5a2d1ecae0f4d4f9a7bf694e221d40")
    version("1.0.2", sha256="83ba7876d884406463cc8ae42214038b7d6c40ead77a1532d64bc96887173f75")
    version("1.0.1", sha256="4bfccc4f4380becb776343e546deb2474deeae79f053ba8ca22287827b8bd4b1")
    version("1.0.0", sha256="4f71c2bee6736ed87d0151e62546d2fc9ff639db58172c26dcf033e5bb1ea04c")

    def build(self, spec, prefix):
        return

    def install(self, spec, prefix):
        make("install", "PREFIX={0}".format(prefix))
