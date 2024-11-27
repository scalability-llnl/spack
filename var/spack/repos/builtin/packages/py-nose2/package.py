# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNose2(PythonPackage):
    """unittest2 with plugins, the succesor to nose"""

    homepage = "https://github.com/nose-devs/nose2"
    pypi = "nose2/nose2-0.9.1.tar.gz"

    license("BSD-2-Clause")

    version("0.9.1", sha256="0ede156fd7974fa40893edeca0b709f402c0ccacd7b81b22e76f73c116d1b999")
    version("0.6.0", sha256="daa633e92a52e0db60ade7e105a2ba5cad7ac819f3608740dcfc6140b9fd0a94")

    depends_on("py-setuptools", type="build")
    depends_on("py-six@1.7:", type=("build", "run"))
    depends_on("py-cov-core@1.12:", type=("build", "run"), when="@0.6.0:0.6.5")
    depends_on("py-coverage@4.4.1:", type=("build", "run"), when="@0.7.0:")
