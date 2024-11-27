# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCommon(PythonPackage):
    """Common tools and data structures implemented in pure python."""

    homepage = "https://pypi.python.org/pypi/common"
    pypi = "common/common-0.1.2.tar.gz"

    license("Unlicense")

    version("0.1.2", sha256="3dfa982670abefc870043b239eaa0ecd860be7aa952b1931c1356b426ff8c76a")

    depends_on("py-setuptools", type="build")
