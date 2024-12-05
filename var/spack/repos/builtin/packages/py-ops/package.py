# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyOps(PythonPackage):
    """The Python library behind great charms"""

    homepage = "https://github.com/canonical/operator"
    pypi = "ops/ops-1.4.0.tar.gz"

    license("Apache-2.0", checked_by="qwertos")

    version("2.16.0", sha256="c4405185744c82589fca4752a76cd7eabd667cf2d3f07d2700b82777186b8de9")
    version("1.4.0", sha256="6bb7c8d8cd3eb1da99469564e37a04f9677205c4c07ef97167e0b93a17ccb59a")

    depends_on("python@3.8:", when="@2.16:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-pyyaml", type=("build", "run"))
    depends_on("py-pyyaml@6", when="@2.16:", type=("build", "run"))
    depends_on("py-websocket-client@1", when="@2.16:", type=("build", "run"))
