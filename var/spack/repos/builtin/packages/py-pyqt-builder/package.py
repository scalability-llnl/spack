# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyqtBuilder(PythonPackage):
    """The PEP 517 compliant PyQt build system."""

    homepage = "https://www.riverbankcomputing.com/hg/PyQt-builder/"
    pypi = "PyQt-builder/PyQt-builder-1.12.2.tar.gz"

    license("GPL-2.0-or-later")

    version("1.15.1", sha256="a2bd3cfbf952e959141dfe55b44b451aa945ca8916d1b773850bb2f9c0fa2985")
    version("1.12.2", sha256="f62bb688d70e0afd88c413a8d994bda824e6cebd12b612902d1945c5a67edcd7")

    depends_on("py-setuptools@30.3:", type="build")
    depends_on("py-packaging", type=("build", "run"))
    depends_on("py-sip@6.7:6", when="@1.15:", type=("build", "run"))
    depends_on("py-sip@6.3:6", type=("build", "run"))
