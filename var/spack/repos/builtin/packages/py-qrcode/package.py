# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyQrcode(PythonPackage):
    """Generate QR codes"""

    homepage = "https://github.com/lincolnloop/python-qrcode"
    pypi = "qrcode/qrcode-7.3.1.tar.gz"

    license("BSD-3-Clause")

    version("7.3.1", sha256="375a6ff240ca9bd41adc070428b5dfc1dcfbb0f2507f1ac848f6cded38956578")

    depends_on("python@3.6:", type=("build", "run"))

    depends_on("py-setuptools", type="build")

    depends_on("py-pillow", type=("build", "run"))
    depends_on("py-typing-extensions", type=("build", "run"))
