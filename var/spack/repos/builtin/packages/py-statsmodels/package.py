# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob
import os

from spack.package import *


class PyStatsmodels(PythonPackage):
    """Statistical computations and models for use with SciPy"""

    homepage = "https://www.statsmodels.org"
    pypi = "statsmodels/statsmodels-0.8.0.tar.gz"
    git = "https://github.com/statsmodels/statsmodels.git"

    license("BSD-3-Clause")

    version("0.14.0", sha256="6875c7d689e966d948f15eb816ab5616f4928706b180cf470fd5907ab6f647a4")
    version("0.13.5", sha256="593526acae1c0fda0ea6c48439f67c3943094c542fe769f8b90fe9e6c6cc4871")
    version("0.13.2", sha256="77dc292c9939c036a476f1770f9d08976b05437daa229928da73231147cde7d4")
    version("0.13.1", sha256="006ec8d896d238873af8178d5475203844f2c391194ed8d42ddac37f5ff77a69")
    version("0.13.0", sha256="f2efc02011b7240a9e851acd76ab81150a07d35c97021cb0517887539a328f8a")
    version("0.12.2", sha256="8ad7a7ae7cdd929095684118e3b05836c0ccb08b6a01fe984159475d174a1b10")
    version("0.12.1", sha256="a271b4ccec190148dccda25f0cbdcbf871f408fc1394a10a7dc1af4a62b91c8e")
    version("0.10.2", sha256="9cd2194c6642a8754e85f9a6e6912cdf996bebf6ff715d3cc67f65dadfd37cc9")
    version("0.10.1", sha256="320659a80f916c2edf9dfbe83512d9004bb562b72eedb7d9374562038697fa10")

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("python@3.8:", when="@0.14:", type=("build", "link", "run"))
    depends_on("python", type=("build", "link", "run"))

    depends_on("py-setuptools@59.2:", when="@0.13.3:", type="build")
    depends_on("py-setuptools@0.6c5:", type="build")

    # pyproject.toml
    depends_on("py-cython@0.29.26:2", when="@0.14:", type="build")
    depends_on("py-cython@0.29.32:2", when="@0.13.5:0.13", type="build")
    depends_on("py-cython@0.29.22:2", when="@0.13:", type="build")
    depends_on("py-cython@0.29.14:2", when="@0.12:", type="build")
    depends_on("py-cython@0.29:2", type="build")
    depends_on("py-setuptools-scm+toml@7.0", when="@0.13.3:", type="build")

    # patsy@0.5.1 works around a Python change
    #    https://github.com/statsmodels/statsmodels/issues/5343 and
    #    https://github.com/pydata/patsy/pull/131

    # requirements.txt
    depends_on("py-numpy@1.18:", when="@0.14:", type=("build", "link", "run"))
    depends_on("py-numpy@1.17:", when="@0.13:", type=("build", "link", "run"))
    depends_on("py-numpy@1.15:", when="@0.12.1:", type=("build", "link", "run"))
    depends_on("py-numpy@1.11:", when="@0.10.1:", type=("build", "link", "run"))
    # https://github.com/statsmodels/statsmodels/issues/9194
    depends_on("py-numpy@:1", when="@:0.14.1", type=("build", "link", "run"))
    depends_on("py-scipy@1.4:", when="@0.13.5:", type=("build", "run"))
    conflicts("^py-scipy@1.9.2")
    depends_on("py-scipy@1.3:", when="@0.13:", type=("build", "run"))
    depends_on("py-scipy@1.2:", when="@0.12:", type=("build", "run"))
    depends_on("py-scipy@0.18:", when="@0.10.1:", type=("build", "run"))
    depends_on("py-pandas@1:", when="@0.14:", type=("build", "run"))
    depends_on("py-pandas@0.25:", when="@0.13:", type=("build", "run"))
    depends_on("py-pandas@0.23:", when="@0.12:", type=("build", "run"))
    depends_on("py-pandas@0.19:", when="@0.10.1:", type=("build", "run"))
    depends_on("py-patsy@0.5.2:", when="@0.13:", type=("build", "run"))
    depends_on("py-patsy@0.5.1:", when="@0.12:", type=("build", "run"))
    depends_on("py-patsy@0.4:", when="@0.10.1:", type=("build", "run"))
    depends_on("py-packaging@21.3:", when="@0.13.2:", type=("build", "run"))

    depends_on("py-pytest", type="test")

    @run_before("install")
    def remove_generated_sources(self):
        # Automatic recythonization doesn't work here, because cythonize is called
        # with force=False by default, so remove generated C files manually.
        for f in find(".", "*.c"):
            os.unlink(f)

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def build_test(self):
        dirs = glob.glob("build/lib*")  # There can be only one...
        with working_dir(dirs[0]):
            pytest = which("pytest")
            pytest("statsmodels")
