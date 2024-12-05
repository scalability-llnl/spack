# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyscaf(PythonPackage):
    """pyScaf orders contigs from genome assemblies utilising several types of
    information"""

    pypi = "pyScaf/pyScaf-0.12a4.tar.gz"

    license("GPL-3.0-only")

    version("0.12a4", sha256="3ce3f6fe80bd058831b6a38a56d464ef10f3ebbdd6bc3dcb0d7f127c0b2c1b36")

    depends_on("py-setuptools", type="build")
    depends_on("py-fastaindex", type=("build", "run"))
