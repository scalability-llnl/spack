# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPytestCpp(PythonPackage):
    """Use pytest runner to discover and execute C++ tests."""

    homepage = "https://github.com/pytest-dev/pytest-cpp"
    pypi = "pytest-cpp/pytest-cpp-1.4.0.tar.gz"

    license("MIT")

    version("1.5.0", sha256="efb7eaac30f9f61515be181d04b70d80d60ce8871426f726ef1844e2db4f3353")
    version("1.4.0", sha256="aa3a04fe7906e50094d1a9b8d38bc10eb59d0a8330a11a0f7a660405228b48ca")

    depends_on("cxx", type="build")  # generated

    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools-scm", type="build")
    depends_on("py-pytest@:5.3,5.4.2:", type=("build", "run"))
    depends_on("py-colorama", type=("build", "run"))
