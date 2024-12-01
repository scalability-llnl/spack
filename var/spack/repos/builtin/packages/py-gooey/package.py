# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGooey(PythonPackage):
    """Turn (almost) any command line program into
    a full GUI application with one line"""

    homepage = "https://pypi.org/project/Gooey/"
    pypi = "Gooey/Gooey-1.0.8.1.tar.gz"

    maintainers("dorton21")

    license("MIT")

    version("1.0.8.1", sha256="08d6bf534f4d50d50dafba5cfc68dcf31a6e9eeef13a94cbe3ea17c4e45c4671")

    depends_on("py-setuptools", type="build")
    depends_on("py-pillow@4.3.0:", type=("build", "run"))
    depends_on("py-psutil@5.4.2:", type=("build", "run"))
    depends_on("py-colored@1.3.93:", type=("build", "run"))
    depends_on("py-pygtrie@2.3.3:", type=("build", "run"))
    depends_on("py-wxpython")
