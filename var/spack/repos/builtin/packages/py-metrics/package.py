# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMetrics(PythonPackage):
    """metrics for Python, C, C++, Go and Javascript code"""

    homepage = "https://github.com/finklabs/metrics/"
    pypi = "metrics/metrics-0.3.3.tar.gz"

    version("0.3.3", sha256="60a2bceea8b56f3c408c4ea5d2e9891f5ddb17e4754f7ebc3feb8844faef9ecf")

    depends_on("py-setuptools", type="build")
    depends_on("py-pygments@2.2.0", type=("build", "run"))
    depends_on("py-pathspec@0.5.5", type=("build", "run"))
    depends_on("py-pathlib2@2.3.0:", type=("build", "run"))
