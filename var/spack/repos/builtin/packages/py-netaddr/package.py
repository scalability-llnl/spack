# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNetaddr(PythonPackage):
    """A system-independent network address manipulation library for Python"""

    homepage = "https://netaddr.readthedocs.io/en/latest/"
    pypi = "netaddr/netaddr-0.8.0.tar.gz"

    maintainers("haampie")

    license("BSD-3-Clause")

    version("0.8.0", sha256="d6cc57c7a07b1d9d2e917aa8b36ae8ce61c35ba3fcd1b83ca31c5a0ee2b5a243")

    depends_on("python@2.7:2.8,3.5:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
