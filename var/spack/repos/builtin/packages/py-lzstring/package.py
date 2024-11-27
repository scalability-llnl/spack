# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyLzstring(PythonPackage):
    """lz-string for python."""

    homepage = "https://github.com/gkovacs/lz-string-python"
    pypi = "lzstring/lzstring-1.0.3.tar.gz"

    version("1.0.3", sha256="d54dd5a5f86837ccfc1343cc9f1cb0674d2d6ebd4b49f6408c35104f0a996cb4")

    depends_on("py-setuptools", type="build")
    depends_on("py-future", type=("build", "run"))
