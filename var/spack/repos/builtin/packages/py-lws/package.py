# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyLws(PythonPackage):
    """Fast spectrogram phase recovery using Local Weighted Sums"""

    homepage = "https://pypi.org/project/lws/"
    pypi = "lws/lws-1.2.6.tar.gz"

    license("Apache-2.0")

    version("1.2.6", sha256="ac94834832aadfcd53fcf4a77e1d95155063b39adbce14c733f8345bdac76e87")

    depends_on("cxx", type="build")  # generated

    depends_on("python@3:", type=("build", "run"))
    depends_on("py-cython", type="build")
    depends_on("py-setuptools", type="build")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))

    def setup_build_environment(self, env):
        env.set("LWS_USE_CYTHON", 1)
