# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class GitRefPackage(AutotoolsPackage):
    """
    dummy package copied from zlib-ng
    """

    homepage = "https://github.com/dummy/dummy"
    url = "https://github.com/dummy/dummy/archive/2.0.0.tar.gz"
    git = "https://github.com/dummy/dummy.git"

    version("2.1.6", sha256="a5d504c0d52e2e2721e7e7d86988dec2e290d723ced2307145dedd06aeb6fef2")
    version("2.1.5", sha256="3f6576971397b379d4205ae5451ff5a68edf6c103b2f03c4188ed7075fbb5f04")
    version("2.1.4", sha256="a0293475e6a44a3f6c045229fe50f69dc0eebc62a42405a51f19d46a5541e77a")
    version(
        "2.1.3",
        sha256="d20e55f89d71991c59f1c5ad1ef944815e5850526c0d9cd8e504eaed5b24491a",
        deprecated=True,
    )
    version(
        "2.1.2",
        sha256="383560d6b00697c04e8878e26c0187b480971a8bce90ffd26a5a7b0f7ecf1a33",
        deprecated=True,
    )
    version("2.0.7", sha256="6c0853bb27738b811f2b4d4af095323c3d5ce36ceed6b50e5f773204fb8f7200")
    version("2.0.0", sha256="86993903527d9b12fc543335c19c1d33a93797b3d4d37648b5addae83679ecd8")

    variant("compat", default=True, description="Enable compatibility API")
    variant("opt", default=True, description="Enable optimizations")
    variant("shared", default=True, description="Build shared library")
    variant("pic", default=True, description="Enable position-independent code (PIC)")

    conflicts("+shared~pic")

    variant("new_strategies", default=True, description="Enable new deflate strategies")
