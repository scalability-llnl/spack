# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHepdataConverter(PythonPackage):
    """This Python 3 library provides support for converting
    Old HepData input format (sample) to YAML as well as
    YAML to ROOT, YODA and CSV."""

    homepage = "https://github.com/HEPData/hepdata-converter"
    pypi = "hepdata-converter/hepdata-converter-0.2.3.tar.gz"

    maintainers("haralmha")

    version("0.2.3", sha256="cbed0ffc512a794fae023650f10f415b687bb8c07fc67ac3321da70ce8846085")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-pyyaml@5.3:", type=("build", "run"))
    depends_on("py-hepdata-validator@0.2.2:", type=("build", "run"))
