# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyStsciDistutils(PythonPackage):
    """This package contains utilities used to
    package some of STScI's Python projects."""

    homepage = "https://github.com/spacetelescope/stsci.distutils"
    url = "https://github.com/spacetelescope/stsci.distutils/archive/0.3.8.tar.gz"

    version("0.3.8", sha256="a52f3ec3b392a9cecd98d143b678c27346cbfa8f34c34698821d7e167907edce")

    depends_on("c", type="build")  # generated

    depends_on("py-setuptools", type="build")
    depends_on("py-d2to1", type="build")
