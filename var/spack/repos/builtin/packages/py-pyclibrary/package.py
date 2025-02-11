# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.pkg.builtin.boost import Boost


class PyPyclibrary(PythonPackage):
    """Pyclibrary"""

    homepage = "https://pyclibrary.readthedocs.io/en/latest/"
    pypi = "pyclibrary/pyclibrary-0.1.7.tar.gz"

    version("0.1.7", sha256="91ed4479754ef21744d8056f8d6c2d269ae7832a90c1e1d4b1128ab0fa76ed18")

    depends_on("py-setuptools", type=("build"))
    depends_on("python@3.8:", type=("build", "run"))
