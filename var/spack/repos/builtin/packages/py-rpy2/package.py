# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRpy2(PythonPackage):
    """rpy2 is a redesign and rewrite of rpy. It is providing a low-level
    interface to R from Python, a proposed high-level interface,
    including wrappers to graphical libraries, as well as R-like
    structures and functions.
    """

    homepage = "https://rpy2.github.io"
    pypi = "rpy2/rpy2-2.5.4.tar.gz"

    license("GPL-2.0-or-later")

    maintainers("Chrismarsh")

    version("3.5.17", sha256="dbff08c30f3d79161922623858a5b3b68a3fba8ee1747d6af41bc4ba68f3d582")
    version("3.0.4", sha256="2af5158a5d56af7f7bf5e54d8d7e87b6f115ff40f056d82f93cad0cbf6acc0cb")
    version("3.0.0", sha256="34efc2935d9015527837d6b1de29641863d184b19d39ad415d5384be8a015bce")

    variant("numpy", default=True, description="Numpy", when="@3.5.17:")
    variant("pandas", default=True, description="Pandas", when="@3.5.17:")

    depends_on("py-setuptools", type="build")

    with when("@3.5.17:"):
        depends_on("python@3.7:", type=("build", "run"))
        depends_on("r@4.0:", type=("build", "run"))

        depends_on("readline")

        depends_on("py-setuptools@61:", type="build")
        depends_on("py-cffi@1.15.0:", type=("build", "run"))
        depends_on("py-jinja2", type=("build", "run"))
        depends_on("py-tzlocal", type=("build", "run"))
        depends_on("py-ipython", type=("build", "run"))

        depends_on("py-numpy@1.26:", type=("build", "run"), when="+numpy")
        depends_on("py-pandas@1.3.5:", type=("build", "run"), when="+pandas")

    # @3.0.0:
    with when("@3.0.0:"):
        depends_on("py-cffi@1.0.0:", type=("build", "run"))
        depends_on("py-simplegeneric", type=("build", "run"))
        depends_on("py-pytest", type=("build", "run"))
        depends_on("r@3.3:", type=("build", "run"))
        depends_on("python@3.5:", type=("build", "run"))
