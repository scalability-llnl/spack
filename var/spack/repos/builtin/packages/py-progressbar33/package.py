# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyProgressbar33(PythonPackage):
    """Text progress bar library for Python"""

    homepage = "https://github.com/germangh/python-progressbar"
    pypi = "progressbar33/progressbar33-2.4.tar.gz"

    license("BSD-3-Clause")

    version("2.4", sha256="51fe0d9b3b4023db2f983eeccdfc8c9846b84db8443b9bee002c7f58f4376eff")

    depends_on("py-setuptools", type="build")
