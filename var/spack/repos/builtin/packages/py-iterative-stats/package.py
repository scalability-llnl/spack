# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyIterativeStats(PythonPackage):
    """Bacis iterative statistics implementation."""

    pypi = "iterative-stats/iterative_stats-0.1.0.tar.gz"
    git = "https://github.com/IterativeStatistics/BasicIterativeStatistics.git"
    maintainers("robcaulk", "viperML", "abhishek1297")

    license("BSD-3-Clause")

    version("main", branch="main")
    version("0.1.1", sha256="c2be6045e720aa7ff5c8dbbcd01d082d1b66f2c2a8613ad825528535e3ce0436")
    version("0.1.0", sha256="bb4f378a8fa117d1f24e9ea5ac0f1bd13c04b1ab3693a148ba936ffb237f2fba")
    version("0.0.4", sha256="7e838aa79de867b0e312be8cdf9319bb70824b624c684e968636cc8d4c9d5712")

    with default_args(type=("build", "run")):
        depends_on("python@3.8:3.10", when="@:0.1.0")
        depends_on("python@3.9:3.12", when="@0.1.1:")
        depends_on("py-pyyaml@6.0:")
        depends_on("py-numpy@1.19:1")

    depends_on("py-poetry-core@1.0.0:", type=("build"))

    with default_args(type=("test")):
        depends_on("py-pytest@6.2.1:6")
        depends_on("py-autopep8@1.6.0")
        depends_on("openturns@1.19+python+libxml2")
        depends_on("py-scipy@1.8:1")

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def install_test(self):
        pytest = which("pytest")
        pytest()
