# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyInterfaceMeta(PythonPackage):
    """A convenient way to expose an extensible API with enforced method
    signatures and consistent documentation."""

    homepage = "https://github.com/matthewwardrop/interface_meta"
    pypi = "interface_meta/interface_meta-1.2.4.tar.gz"

    license("MIT")

    version("1.3.0", sha256="8a4493f8bdb73fb9655dcd5115bc897e207319e36c8835f39c516a2d7e9d79a1")
    version("1.2.4", sha256="4c7725dd4b80f97b7eecfb26023e1a8a7cdbb6d6a7207a8e93f9d4bfef9ee566")

    depends_on("python@3.7:3", when="@1.3:", type=("build", "run"))
    depends_on("python@3.4:", type=("build", "run"))
    depends_on("py-poetry-core@1:", when="@1.3:", type="build")
    depends_on("py-poetry-dynamic-versioning", when="@1.3:", type="build")
    depends_on("py-setuptools", when="@:1.2", type="build")
    depends_on("py-setupmeta", when="@:1.2", type="build")
