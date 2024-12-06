# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPickleshare(PythonPackage):
    """Tiny 'shelve'-like database with concurrency support"""

    pypi = "pickleshare/pickleshare-0.7.4.tar.gz"

    license("MIT")

    version("0.7.5", sha256="87683d47965c1da65cdacaf31c8441d12b8044cdec9aca500cd78fc2c683afca")
    version("0.7.4", sha256="84a9257227dfdd6fe1b4be1319096c20eb85ff1e82c7932f36efccfe1b09737b")

    depends_on("python@2.7:2.8,3:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
