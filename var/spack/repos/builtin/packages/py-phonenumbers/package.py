# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPhonenumbers(PythonPackage):
    """Python version of Google's common library for parsing, formatting
    and validating international phone numbers."""

    homepage = "https://github.com/daviddrysdale/python-phonenumbers"
    pypi = "phonenumbers/phonenumbers-8.12.16.tar.gz"

    version("8.12.16", sha256="a820ab08c980ef24a2d2a1ead4f8d7016fdf008e484d1aecf7ff0b32cc475e16")
    version("8.12.15", sha256="b734bfcf33e87ddae72196a40b3d1af35abd0beb263816ae18e1bff612926406")
    version("8.12.14", sha256="58817072cf2b80fcc8710e7a2c395cd32fce2b70a259e36ff81916862f578d61")

    depends_on("python@2.5:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
