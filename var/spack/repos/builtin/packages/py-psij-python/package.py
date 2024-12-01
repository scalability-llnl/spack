# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPsijPython(PythonPackage):
    """PSI/J is an abstraction layer over cluster schedulers to write scheduler
    agnostic HPC applications."""

    homepage = "https://www.exaworks.org/"
    git = "https://github.com/exaworks/psij-python.git"
    pypi = "psij-python/psij-python-0.1.0.post2.tar.gz"

    maintainers("andre-merzky")

    license("MIT")

    version(
        "0.1.0.post2", sha256="78f4fb147248be479aa6128b583dff9052698c49f36c6e9811b4c3f9db326043"
    )

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-filelock", type=("build", "run"))
    depends_on("py-psutil", type=("build", "run"))
    depends_on("py-pystache", type=("build", "run"))
    depends_on("py-setuptools", type="build")
