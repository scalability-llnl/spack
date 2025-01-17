# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCylcRose(PythonPackage):
    """A Cylc plugin providing support for the Rose rose-suite.conf file."""

    homepage = "https://cylc.github.io/cylc-doc/latest/html/plugins/cylc-rose.html"
    pypi = "cylc-rose/cylc-rose-1.3.0.tar.gz"
    git = "https://github.com/cylc/cylc-rose.git"

    maintainers("LydDeb", "climbfuji")

    license("GPL-3.0-only")

    # Version 1.4.2 is available at PyPI, but not at the URL that is considered canonical by Spack
    # https://github.com/spack/spack/issues/48479
    version("1.4.2", commit="8deda0480afed8cf92cfdf7938fc78d0aaf0c0e4")
    version("1.3.0", sha256="017072b69d7a50fa6d309a911d2428743b07c095f308529b36b1b787ebe7ab88")

    depends_on("py-setuptools", type="build")
    depends_on("py-metomi-isodatetime", type=("build", "run"))
    depends_on("py-jinja2", type=("build", "run"))

    with when("@1.3.0"):
        depends_on("py-metomi-rose@2.1", type=("build", "run"))
        depends_on("py-cylc-flow@8.2", type=("build", "run"))

    with when("@1.4.2"):
        depends_on("py-metomi-rose@2.3", type=("build", "run"))
        depends_on("py-cylc-flow@8.3.5:8.3", type=("build", "run"))
        depends_on("py-ansimarkup", type=("build", "run"))
