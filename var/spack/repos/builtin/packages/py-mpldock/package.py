# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMpldock(PythonPackage):
    """Dock matplotlib figures and other widgets."""

    homepage = "https://github.com/peper0/mpldock"
    pypi = "mpldock/mpldock-0.1.tar.gz"

    maintainers("LydDeb")

    license("MIT")

    version("0.1", sha256="8fee2e9cb25e122c9e11c15ea3ad22c9d03e78a08a0bc2b7f453230d58a31a55")

    depends_on("py-setuptools", type="build")
    depends_on("py-pyqt5", type=("build", "run"))
    depends_on("py-matplotlib", type=("build", "run"))
    depends_on("py-appdirs", type=("build", "run"))
