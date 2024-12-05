# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyFabric(PythonPackage):
    """High level SSH command execution."""

    homepage = "http://fabfile.org/"
    pypi = "fabric/fabric-2.5.0.tar.gz"

    license("BSD-2-Clause")

    version("2.5.0", sha256="24842d7d51556adcabd885ac3cf5e1df73fc622a1708bf3667bf5927576cdfa6")

    depends_on("py-setuptools", type="build")
    depends_on("py-invoke@1.3:1", type=("build", "run"))
    depends_on("py-paramiko@2.4:", type=("build", "run"))
