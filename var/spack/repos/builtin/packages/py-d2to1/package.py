# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyD2to1(PythonPackage):
    """d2to1 (the 'd' is for 'distutils') allows
    using distutils2-like setup.cfg files for a package's
    metadata with a distribute/setuptools setup.py script."""

    homepage = "https://github.com/embray/d2to1"
    url = "https://github.com/embray/d2to1/archive/0.2.12.tar.gz"

    version(
        "0.2.12.post1", sha256="80e026ccc604850d8171fd8599b3130d234c0d443e1dc4e2039be0b204cea9b4"
    )
    version("0.2.12", sha256="04ab9f3ac255d367ecda1eb59379e5031816740c3a3eda95d0dba9f6bb3b7ca4")

    depends_on("c", type="build")  # generated

    depends_on("py-setuptools", type="build")
