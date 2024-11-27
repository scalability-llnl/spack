# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyWcwidth(PythonPackage):
    """Measures number of Terminal column cells of wide-character codes"""

    homepage = "https://github.com/jquast/wcwidth"
    pypi = "wcwidth/wcwidth-0.1.7.tar.gz"

    license("MIT")

    version("0.2.7", sha256="1b6d30a98ddd5ce9bbdb33658191fd2423fc9da203fe3ef1855407dcb7ee4e26")
    version("0.2.5", sha256="c4d647b99872929fdb7bdcaa4fbe7f01413ed3d98077df798530e5b04f116c83")
    version("0.1.7", sha256="3df37372226d6e63e1b1e1eda15c594bca98a22d33a23832a90998faa96bc65e")

    depends_on("py-setuptools", type="build")
