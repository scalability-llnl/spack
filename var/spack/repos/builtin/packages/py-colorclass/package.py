# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyColorclass(PythonPackage):
    """Colorful worry-free console applications for Linux, Mac OS X, and Windows."""

    homepage = "https://github.com/Robpol86/colorclass"
    pypi = "colorclass/colorclass-2.2.0.tar.gz"

    license("MIT")

    version("2.2.0", sha256="b05c2a348dfc1aff2d502527d78a5b7b7e2f85da94a96c5081210d8e9ee8e18b")

    depends_on("python@3.3.0:")
    depends_on("py-setuptools", type="build")
    depends_on("py-docopt", type=("build", "run"))
