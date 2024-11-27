# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTestrepository(PythonPackage):
    """A repository of test results."""

    homepage = "https://launchpad.net/testrepository"
    pypi = "testrepository/testrepository-0.0.20.tar.gz"

    license("Apache-2.0")

    version("0.0.20", sha256="752449bc98c20253ec4611c40564aea93d435a5bf3ff672208e01cc10e5858eb")

    depends_on("py-setuptools", type="build")
    depends_on("py-fixtures", type=("build", "run"))
    depends_on("py-python-subunit@0.0.18:", type=("build", "run"))
    depends_on("py-testtools@0.9.30:", type=("build", "run"))
