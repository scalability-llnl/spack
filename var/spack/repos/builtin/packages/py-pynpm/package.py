# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPynpm(PythonPackage):
    """Python interface to your NPM and package.json."""

    homepage = "https://pynpm.readthedocs.io/en/latest/"
    pypi = "pynpm/pynpm-0.2.0.tar.gz"
    git = "https://github.com/inveniosoftware/pynpm"
    maintainers("jeremyfix")

    license("BSD-3-Clause")

    version("0.2.0", sha256="212a1e5f86fe8b790945dd856682c6dcd8eddc6f8803a51e7046fe427d7f801b")

    depends_on("py-setuptools", type="build")
    depends_on("py-babel@2.9:", type="build")
