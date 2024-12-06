# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyIocapture(PythonPackage):
    """Capture stdout, stderr easily."""

    homepage = "https://github.com/oinume/iocapture"
    pypi = "iocapture/iocapture-0.1.2.tar.gz"

    maintainers("dorton21")

    license("MIT")

    version("0.1.2", sha256="86670e1808bcdcd4f70112f43da72ae766f04cd8311d1071ce6e0e0a72e37ee8")

    depends_on("python@2.4:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
