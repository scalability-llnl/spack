# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyIpaddress(PythonPackage):
    """Python 3.3's ipaddress for older Python versions"""

    homepage = "https://github.com/phihag/ipaddress"
    pypi = "ipaddress/ipaddress-1.0.23.tar.gz"

    license("PSF-2.0")

    version("1.0.23", sha256="b7f8e0369580bb4a24d5ba1d7cc29660a4a6987763faf1d8a8046830e020e7e2")
    version("1.0.22", sha256="b146c751ea45cad6188dd6cf2d9b757f6f4f8d6ffb96a023e6f2e26eea02a72c")
    version("1.0.18", sha256="5d8534c8e185f2d8a1fda1ef73f2c8f4b23264e8e30063feeb9511d492a413e1")

    depends_on("py-setuptools", type="build")
