# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHstspreload(PythonPackage):
    """Chromium HSTS Preload list as a Python package and updated daily"""

    homepage = "https://github.com/sethmlarson/hstspreload"
    pypi = "hstspreload/hstspreload-2020.9.23.tar.gz"

    license("BSD-3-Clause")

    version("2020.9.23", sha256="35822733ba67cfb4efc6cd7d1230b509f0bd42c90eeb329faf2fe679f801e40f")

    depends_on("py-setuptools", type="build")
    depends_on("py-wheel", type="build")
