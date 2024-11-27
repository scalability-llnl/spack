# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFiscalyear(PythonPackage):
    """fiscalyear is a small, lightweight Python module providing helpful
    utilities for managing the fiscal calendar.

    It is designed as an extension of the built-in datetime and calendar
    modules, adding the ability to query the fiscal year, fiscal quarter,
    fiscal month, and fiscal day of a date or datetime object."""

    homepage = "https://github.com/adamjstewart/fiscalyear"
    pypi = "fiscalyear/fiscalyear-0.2.0.tar.gz"
    git = "https://github.com/adamjstewart/fiscalyear.git"

    maintainers("adamjstewart")

    license("MIT")

    version("master", branch="master")
    version("0.4.0", sha256="12857a48bd7b97bda78d833b29e81f30ec5aa018241f690e714b472b25fa1b47")
    version("0.3.2", sha256="0697b2af4ab2d4c6188fac33d340f31dea9b0e1f0d3666d6752faeedd744f019")
    version("0.3.1", sha256="5964b4be71453c1fa5da804343cea866e0299aff874aa59ae186a8a9b9ff62d0")
    version("0.3.0", sha256="64f97b3a0ab6b2857d09f0016bd3aae37646a454a5c2c66e907fef03ae54a816")
    version("0.2.0", sha256="f513616aeb03046406c56d7c69cd9e26f6a12963c71c1410cc3d4532a5bfee71")
    version("0.1.0", sha256="3fde4a12eeb72da446beb487e078adf1223a92d130520e589b82d7d1509701a2")

    depends_on("python@3.6:", when="@0.4:", type=("build", "run"))
    depends_on("python@2.5:", type=("build", "run"))
    depends_on("py-setuptools@42:", when="@0.4:", type="build")
    depends_on("py-setuptools", type="build")
