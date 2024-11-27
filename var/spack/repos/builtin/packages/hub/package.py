# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Hub(Package):
    """The github git wrapper"""

    homepage = "https://github.com/github/hub"
    url = "https://github.com/github/hub/archive/v2.2.2.tar.gz"
    git = "https://github.com/github/hub.git"

    license("MIT")

    version("master", branch="master")
    version("2.14.2", sha256="e19e0fdfd1c69c401e1c24dd2d4ecf3fd9044aa4bd3f8d6fd942ed1b2b2ad21a")
    version(
        "2.2.2",
        sha256="610572ee903aea1fa8622c16ab7ddef2bd1bfec9f4854447ab8e0fbdbe6a0cae",
        deprecated=True,
    )
    version(
        "2.2.1",
        sha256="9350aba6a8e3da9d26b7258a4020bf84491af69595f7484f922d75fc8b86dc10",
        deprecated=True,
    )
    version(
        "2.2.0",
        sha256="2da1351197eb5696c207f22c69a5422af052d74277b73d0b8661efb9ec1d0eb1",
        deprecated=True,
    )
    version(
        "1.12.4",
        sha256="b7fe404d7dc5f60554f088bec12de5e80229331430ea0ced46d5bf89ecae5117",
        deprecated=True,
    )

    depends_on("c", type="build")  # generated

    extends("go")

    def install(self, spec, prefix):
        env = os.environ
        if spec.version < Version("2.14"):
            env["GOPATH"] = self.stage.source_path + ":" + env["GOPATH"]
            env["GO111MODULE"] = "off"
            bash = which("bash")
            bash(os.path.join("script", "build"), "-o", prefix.bin.hub)
            return
        env["GO111MODULE"] = "on"
        go("build", "-o", prefix.bin.hub)
