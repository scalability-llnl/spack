# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyicu(PythonPackage):
    """Python extension wrapping the ICU C++ API"""

    homepage = "https://gitlab.pyicu.org/main/pyicu"
    pypi = "PyICU/PyICU-2.14.tar.gz"

    maintainers("Chrismarsh")

    license("MIT", checked_by="Chrismarsh")

    version("2.14", sha256="acc7eb92bd5c554ed577249c6978450a4feda0aa6f01470152b3a7b382a02132")

    depends_on("cxx", type="build")

    depends_on("py-setuptools", type="build")
    depends_on("pkgconfig", type="build")

    depends_on("icu4c@:76")  # ICU_MAX_MAJOR_VERSION in setup.py
