# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMplhepData(PythonPackage):
    """Font (Data) sub-package for mplhep"""

    homepage = "https://github.com/Scikit-HEP/mplhep_data"
    pypi = "mplhep_data/mplhep_data-0.0.3.tar.gz"

    license("MIT")

    version("0.0.3", sha256="b54d257f3f53c93a442cda7a6681ce267277e09173c0b41fd78820f78321772f")

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-setuptools@42:", type="build")
    depends_on("py-setuptools-scm@3.4:+toml", type="build")
