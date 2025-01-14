# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRpaths(PythonPackage):
    """A path manipulation library, heavily inspired by Unipath and pathlib.

    It aims at total Python 2/3 and Windows/POSIX compatibility. To my
    knowledge, no other library can handle all the possible paths on every
    platform.

    """

    homepage = "https://github.com/remram44/rpaths"

    pypi = "rpaths/rpaths-1.0.0.tar.gz"

    maintainers("charmoniumQ")

    version("1.0.0", sha256="dd7418b2c837e1b4eb5c5490465d5f282645143e4638c809ddd250dc33395641")

    depends_on("py-setuptools", type="build")
