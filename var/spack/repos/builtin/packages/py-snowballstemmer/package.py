# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySnowballstemmer(PythonPackage):
    """This package provides 29 stemmers for 28 languages generated from
    Snowball algorithms."""

    homepage = "https://github.com/snowballstem/snowball"
    pypi = "snowballstemmer/snowballstemmer-2.0.0.tar.gz"

    license("BSD-3-Clause")

    version("2.2.0", sha256="09b16deb8547d3412ad7b590689584cd0fe25ec8db3be37788be3810cbf19cb1")
    version("2.0.0", sha256="df3bac3df4c2c01363f3dd2cfa78cce2840a79b9f1c2d2de9ce8d31683992f52")
    version("1.2.1", sha256="919f26a68b2c17a7634da993d91339e288964f93c274f1343e3bbbe2096e1128")

    depends_on("py-setuptools", type="build")
