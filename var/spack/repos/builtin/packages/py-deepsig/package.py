# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDeepsig(PythonPackage):
    """deep-significance: Easy and Better Significance Testing for Deep Neural
    Networks"""

    homepage = "https://github.com/Kaleidophon/deep-significance"
    pypi = "deepsig/deepsig-1.2.1.tar.gz"

    version("1.2.1", sha256="8543630c00264898116a065f6461c131d026ef75d8703bc631a4fd2bafb31f89")

    depends_on("python@3.5.3:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-numpy@1.19.5", type=("build", "run"))
    depends_on("py-scipy@1.6.0", type=("build", "run"))
    depends_on("py-tqdm@4.59.0", type=("build", "run"))
    depends_on("py-joblib@1.0.1", type=("build", "run"))
    depends_on("py-pandas@1.3.3", type=("build", "run"))
    depends_on("py-dill@0.3.4", type=("build", "run"))

    def patch(self):
        filter_file("README_RAW.md", "README.md", "setup.py", string=True)
