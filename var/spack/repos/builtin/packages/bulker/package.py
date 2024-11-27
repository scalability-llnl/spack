# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Bulker(PythonPackage):
    """Bulker: multi-container environment manager"""

    homepage = "https://bulker.databio.org/"
    pypi = "bulker/bulker-0.7.3.tar.gz"

    license("BSD-2-Clause")

    version("0.7.3", sha256="a7a3a97184d50d2247dc3b116f31f90c27435d9872c6845152ff46f5c4e39d50")

    depends_on("py-setuptools", type="build")
    depends_on("py-yacman@0.8.4:", type=("build", "run"))
    depends_on("py-pyyaml@5.1:", type=("build", "run"))
    depends_on("py-logmuse@0.2.0:", type=("build", "run"))
    depends_on("py-jinja2", type=("build", "run"))
    depends_on("py-ubiquerg@0.5.1:", type=("build", "run"))
    depends_on("py-psutil", type=("build", "run"))
    depends_on("singularityce", type="run")
