# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRequestsToolbelt(PythonPackage):
    """A toolbelt of useful classes and functions to be used with
    python-requests"""

    homepage = "https://toolbelt.readthedocs.org/"
    pypi = "requests-toolbelt/requests-toolbelt-0.9.1.tar.gz"
    git = "https://github.com/requests/toolbelt.git"

    license("Apache-2.0")

    version("1.0.0", sha256="7681a0a3d047012b5bdc0ee37d7f8f07ebe76ab08caeccfc3921ce23c88d5bc6")
    version("0.9.1", sha256="968089d4584ad4ad7c171454f0a5c6dac23971e9472521ea3b6d49d610aa6fc0")
    version("0.8.0", sha256="f6a531936c6fa4c6cfce1b9c10d5c4f498d16528d2a54a22ca00011205a187b5")

    depends_on("py-setuptools", type="build")
    depends_on("py-requests@2.0.1:2", type=("build", "run"))
