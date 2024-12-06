# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyCloudbridge(PythonPackage):
    """A simple layer of abstraction over multiple cloud providers."""

    homepage = "http://cloudbridge.cloudve.org"
    pypi = "cloudbridge/cloudbridge-3.1.0.tar.gz"

    license("MIT")

    version("3.1.0", sha256="f9d3c1ae36b14a1c953d36c21a35fa2c72d42831cbbfe6117d13b25e9cccb28c")

    depends_on("python@3.4:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-nose@1:", type="build")

    depends_on("py-six@1.11:", type=("build", "run"))
    depends_on("py-tenacity@6.0:", type=("build", "run"))
    depends_on("py-deprecation@2.0.7:", type=("build", "run"))
    depends_on("py-pyeventsystem@:1", type=("build", "run"))
