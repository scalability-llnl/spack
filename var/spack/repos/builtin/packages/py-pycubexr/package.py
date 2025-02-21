# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPycubexr(PythonPackage):
    """pyCubexR is a Python package for reading the Cube4 file format."""

    homepage = "https://github.com/extra-p/pycubexr"
    pypi = "pycubexr/pycubexr-2.0.0.tar.gz"

    license("BSD-3-Clause")

    version("2.0.0", sha256="03504fbbc9cbd514943e8aeb57919ad49731fe264bdbab86711bf10851276924")

    depends_on("py-setuptools", type="build")
    depends_on("py-numpy@1.18:1", type=("build", "run"))
