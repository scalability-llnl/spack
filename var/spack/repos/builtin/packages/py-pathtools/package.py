# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPathtools(PythonPackage):
    """Path utilities for Python"""

    homepage = "https://github.com/gorakhargosh/pathtools"
    pypi = "pathtools/pathtools-0.1.2.tar.gz"

    maintainers("dorton21")

    license("MIT")

    version("0.1.2", sha256="7c35c5421a39bb82e58018febd90e3b6e5db34c5443aaaf742b3f33d4655f1c0")

    depends_on("py-setuptools", type="build")
