# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPythonqwt(PythonPackage):
    """Qt plotting widgets for Python"""

    homepage = "https://github.com/PierreRaybaut/PythonQwt"
    pypi = "PythonQwt/PythonQwt-0.5.5.zip"

    license("LGPL-2.1-or-later")

    version("0.5.5", sha256="1f13cc8b555a57f8fe0f806d6c2f6d847050e4d837649503932b81316d12788a")

    depends_on("py-setuptools", type="build")
    depends_on("py-numpy@1.3:", type=("build", "run"))
    depends_on("py-sip", type=("build", "run"))
    depends_on("py-pyqt4", type=("build", "run"))
