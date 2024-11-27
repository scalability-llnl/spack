# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyCheroot(PythonPackage):
    """Highly-optimized, pure-python HTTP server"""

    homepage = "https://cheroot.readthedocs.io/en/latest/"
    pypi = "cheroot/cheroot-6.5.5.tar.gz"

    license("BSD-3-Clause")

    version("8.3.0", sha256="a0577e1f28661727d472671a7cc4e0c12ea0cbc5220265e70f00a8b8cb628931")
    version("6.5.5", sha256="f6a85e005adb5bc5f3a92b998ff0e48795d4d98a0fbb7edde47a7513d4100601")

    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools-scm@1.15.0:", type="build")
    depends_on("py-setuptools-scm-git-archive@1.0:", type="build")
    depends_on("py-more-itertools@2.6:", type=("build", "run"))
    depends_on("py-six@1.11.0:", type=("build", "run"))
    depends_on("py-jaraco-functools", when="@8.3.0:", type=("build", "run"))
    depends_on("python@2.7:2.8,3.4:", type=("build", "run"))
