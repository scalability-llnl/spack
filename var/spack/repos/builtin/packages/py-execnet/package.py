# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyExecnet(PythonPackage):
    """execnet provides a share-nothing model with channel-send/receive
    communication for distributing execution across many Python interpreters
    across version, platform and network barriers."""

    homepage = "https://codespeak.net/execnet"
    pypi = "execnet/execnet-1.7.1.tar.gz"

    license("MIT")

    version("1.9.0", sha256="8f694f3ba9cc92cab508b152dcfe322153975c29bda272e2fd7f3f00f36e47c5")
    version("1.7.1", sha256="cacb9df31c9680ec5f95553976c4da484d407e85e41c83cb812aa014f0eddc50")
    version("1.4.1", sha256="f66dd4a7519725a1b7e14ad9ae7d3df8e09b2da88062386e08e941cafc0ef3e6")

    depends_on("python@2.7:2.8,3.4:", type=("build", "run"))
    depends_on("python@2.7:2.8,3.5:", type=("build", "run"), when="@1.9:")
    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools-scm", type="build")
    depends_on("py-apipkg@1.4:", type=("build", "run"), when="@:1.7")
