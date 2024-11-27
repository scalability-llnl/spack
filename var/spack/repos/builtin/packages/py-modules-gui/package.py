# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyModulesGui(PythonPackage):
    """MoGui is a Graphical User Interface (GUI) for Environment Modules.
    It helps users selecting modules to load and save module collections."""

    homepage = "https://github.com/cea-hpc/mogui"
    pypi = "modules-gui/modules-gui-0.2.tar.gz"

    maintainers("adrien-cotte")

    license("GPL-2.0")

    version("0.2", sha256="d58a3943f4631756afa4f84c13b70fae67a72365ab3cad28014f972b8d023aec")

    depends_on("py-setuptools@61:", type=("build"))
    depends_on("py-setuptools-scm", type=("build"))
    depends_on("py-pyqt5", type=("run"))
    depends_on("environment-modules@5.2:", type=("run"))
