# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPychecker(PythonPackage):
    """Python source code checking tool."""

    homepage = "https://pychecker.sourceforge.net/"
    url = (
        "http://sourceforge.net/projects/pychecker/files/pychecker/0.8.19/pychecker-0.8.19.tar.gz"
    )

    license("BSD-3-Clause")

    version("0.8.19", sha256="44fb26668f74aca3738f02d072813762a37ce1242f50dbff573720fa2e953279")

    # pip silently replaces distutils with setuptools
    depends_on("py-setuptools", type="build")
