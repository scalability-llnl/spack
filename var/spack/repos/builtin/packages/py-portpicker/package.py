# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPortpicker(PythonPackage):
    """A library to choose unique available network ports."""

    homepage = "https://github.com/google/python_portpicker"
    pypi = "portpicker/portpicker-1.5.2.tar.gz"

    license("Apache-2.0")

    version("1.5.2", sha256="c55683ad725f5c00a41bc7db0225223e8be024b1fa564d039ed3390e4fd48fb3")

    depends_on("py-setuptools@40.9:", type="build")
    depends_on("py-psutil", type=("build", "run"))
