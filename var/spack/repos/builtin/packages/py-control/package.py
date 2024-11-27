# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyControl(PythonPackage):
    """The Python Control Systems Library is a Python module that implements
    basic operations for analysis and design of feedback control systems."""

    homepage = "https://python-control.org/"
    pypi = "control/control-0.9.1.tar.gz"

    maintainers("haralmha")

    license("BSD-3-Clause")

    version("0.9.1", sha256="8c9084bf386eafcf5d74008f780fae6dec68d243d18a380c866ac10a3549f8d3")

    depends_on("py-setuptools", type="build")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-matplotlib", type=("build", "run"))
