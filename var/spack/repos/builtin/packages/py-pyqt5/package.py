# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyqt5(SIPPackage):
    """PyQt is a set of Python v2 and v3 bindings for The Qt Company's Qt
    application framework and runs on all platforms supported by Qt including
    Windows, OS X, Linux, iOS and Android. PyQt5 supports Qt v5."""

    homepage = "https://www.riverbankcomputing.com/software/pyqt/intro"
    url = "https://files.pythonhosted.org/packages/source/P/PyQt5/PyQt5-5.15.9.tar.gz"
    list_url = "https://pypi.org/simple/PyQt5/"

    license("GPL-3.0-only")

    version("5.15.9", sha256="dc41e8401a90dc3e2b692b411bd5492ab559ae27a27424eed4bd3915564ec4c0")

    depends_on("cxx", type="build")  # generated

    # pyproject.toml
    depends_on("py-sip@6.6.2:6", type="build")
    depends_on("py-pyqt-builder@1.14.1:1", type="build")

    # PKG-INFO
    depends_on("py-pyqt5-sip@12.11:12", type=("build", "run"))

    # README
    depends_on("qt@5+opengl")

    def configure_args(self):
        # https://www.riverbankcomputing.com/static/Docs/PyQt5/installation.html
        return ["--confirm-license", "--no-make", "--qmake", self.spec["qt"].prefix.bin.qmake]
