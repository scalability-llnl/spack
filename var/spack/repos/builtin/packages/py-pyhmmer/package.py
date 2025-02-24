# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyhmmer(PythonPackage):
    """HMMER is a biological sequence analysis tool that uses profile hidden
    Markov models to search for sequence homologs. HMMER3 is developed and
    maintained by the Eddy/Rivas Laboratory at Harvard University.  pyhmmer
    is a Python package, implemented using the Cython language, that provides
    bindings to HMMER3."""

    homepage = "https://github.com/althonos/pyhmmer"
    pypi = "pyhmmer/pyhmmer-0.10.14.tar.gz"

    license("MIT", checked_by="luke-dt")

    version("0.10.15", sha256="bf8e97ce8da6fb5850298f3074640f3e998d5a655877f865c1592eb057dc7921")
    version("0.10.14", sha256="eb50bdfdf67a3b1fecfe877d7ca6d9bade9a9f3dea3ad60c959453bbb235573d")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools@46.4:", type="build")
    depends_on("py-cython@3.0", type="build")
    depends_on("py-psutil@5.8:", type=("build", "run"))
