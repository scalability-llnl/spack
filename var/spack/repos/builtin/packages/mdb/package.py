# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Mdb(PythonPackage):
    """mdb is a command line debugger aimed at parallel programs using the MPI
    programming paradigm."""

    homepage = "https://mdb.readthedocs.io/en/latest"
    pypi = "mdb_debugger/mdb_debugger-1.0.3.tar.gz"

    maintainers("tommelt")

    license("MIT", checked_by="tommelt")

    version("1.0.3", sha256="c45cffb320a51274519753b950b7b72cd91a8a5804941556120ed41bb8b491d8")

    depends_on("python@3.10: +tkinter", type=("build", "run"))
    depends_on("py-pip", type=("build", "run"))
    depends_on("py-setuptools", type="build")

    depends_on("py-click@8.1.7", type=("build", "run"))
    depends_on("py-pexpect@4.9:", type=("build", "run"))
    depends_on("py-typing-extensions", type=("build", "run"))
    depends_on("py-matplotlib@3.8.3 backend=qt5agg", type=("build", "run"))
    depends_on("py-pyqt5", type=("build", "run"))

    depends_on("mpi", type=("run"))

    variant("manpage", default=False, description="build and install manpage")
    variant("termgraph", default=True, description="build with termgraph support")

    with when("+termgraph"):
        depends_on("py-termgraph", type=("build", "run"))

    with when("+manpage"):
        depends_on("py-sphinx", type=("build"))
        depends_on("py-sphinx-rtd-theme", type=("build"))
        depends_on("py-sphinx-click", type=("build"))

    @run_after("install")
    def build_docs(self):
        if self.spec.satisfies("+manpage"):
            make("-C", "docs", "man")

            mkdirp(prefix.share.man.man1)
            copy("docs/build/man/mdb.1", prefix.share.man.man1)
