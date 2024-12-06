# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPygetwindow(PythonPackage):
    """A simple, cross-platform module for obtaining GUI
    information on and controlling application's windows."""

    homepage = "https://github.com/asweigart/pygetwindow"
    pypi = "PyGetWindow/PyGetWindow-0.0.9.tar.gz"

    version("0.0.9", sha256="17894355e7d2b305cd832d717708384017c1698a90ce24f6f7fbf0242dd0a688")

    depends_on("py-setuptools", type="build")
    depends_on("py-pyrect", type=("build", "run"))
