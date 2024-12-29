# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyJsonlines(PythonPackage):
    """Library with helpers for the jsonlines file format"""

    homepage = "https://github.com/wbolster/jsonlines"
    pypi = "jsonlines/jsonlines-4.0.0.tar.gz"

    license("BSD-3-Clause", checked_by="alex391")

    version("4.0.0", sha256="0c6d2c09117550c089995247f605ae4cf77dd1533041d366351f6f298822ea74")

    depends_on("py-setuptools", type="build")
    depends_on("py-attrs@19.2.0:", type=("build", "run"))
