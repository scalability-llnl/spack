# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRobotframework(PythonPackage):
    """Cross-platform lib for process and system monitoring in Python."""

    homepage = "https://opencollective.com/psutil"
    url = "https://github.com/robotframework/robotframework/archive/v3.2.2.tar.gz"

    license("Apache-2.0")

    version("3.2.2", sha256="6b2bddcecb5d1c6198999e38aeaf4c0366542a5e7b5bd788c6a3a36b055d5ea2")
    version("3.2.1", sha256="9805faa0990125ff2c9689b673448d5f47e78470e7a8e95af1606a775fa8379f")

    depends_on("py-setuptools", type=("build", "run"))
