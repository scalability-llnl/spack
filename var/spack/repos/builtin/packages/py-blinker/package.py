# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBlinker(PythonPackage):
    """Fast, simple object-to-object and broadcast signaling"""

    homepage = "https://blinker.readthedocs.io"
    pypi = "blinker/blinker-1.4.tar.gz"
    git = "https://github.com/pallets-eco/blinker.git"

    license("MIT")

    version("1.6.2", sha256="4afd3de66ef3a9f8067559fb7a1cbe555c17dcbe15971b05d1b625c3e7abe213")
    version("1.4", sha256="471aee25f3992bd325afa3772f1063dbdbbca947a041b8b89466dc00d606f8b6")

    depends_on("py-setuptools@61.2:", when="@1.6:", type="build")
    depends_on("py-setuptools", type="build")
