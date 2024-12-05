# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPythonSubunit(PythonPackage):
    """Python implementation of subunit test streaming protocol."""

    homepage = "https://launchpad.net/subunit"
    pypi = "python-subunit/python-subunit-1.3.0.tar.gz"

    license("MIT")

    version("1.3.0", sha256="9607edbee4c1e5a30ff88549ce8d9feb0b9bcbcb5e55033a9d76e86075465cbb")

    depends_on("py-setuptools", type="build")
    depends_on("py-extras", type=("build", "run"))
    depends_on("py-testtools@0.9.34:", type=("build", "run"))
