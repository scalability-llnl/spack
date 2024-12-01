# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyDiskcache(PythonPackage):
    """Disk Cache -- Disk and file backed persistent cache."""

    homepage = "http://www.grantjenks.com/docs/diskcache/"
    pypi = "diskcache/diskcache-4.1.0.tar.gz"

    license("Apache-2.0")

    version("5.2.1", sha256="1805acd5868ac10ad547208951a1190a0ab7bbff4e70f9a07cde4dbdfaa69f64")
    version("4.1.0", sha256="bcee5a59f9c264e2809e58d01be6569a3bbb1e36a1e0fb83f7ef9b2075f95ce0")

    depends_on("python", type=("build", "run"), when="@:4.1.0")
    depends_on("python@3:", type=("build", "run"), when="@5.2.1:")
    depends_on("py-setuptools", type="build")
