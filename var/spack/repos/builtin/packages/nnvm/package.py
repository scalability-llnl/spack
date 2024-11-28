# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Nnvm(CMakePackage):
    """nnvm is a modular, decentralized and lightweight
    part to help build deep learning libraries."""

    homepage = "https://github.com/dmlc/nnvm"
    git = "https://github.com/dmlc/nnvm.git"

    license("Apache-2.0")

    version("master", branch="master")
    version("20170418", commit="b279286304ac954098d94a2695bca599e832effb")

    depends_on("cxx", type="build")  # generated

    variant("shared", default=True, description="Build a shared NNVM lib.")

    depends_on("dmlc-core")

    patch("cmake.patch")
    patch("cmake2.patch", when="@20170418")

    def cmake_args(self):
        spec = self.spec
        return [
            self.define_from_variant("USE_SHARED_NNVM", "shared"),
            "-DUSE_STATIC_NNVM=%s" % ("ON" if "~shared" in spec else "OFF"),
        ]
