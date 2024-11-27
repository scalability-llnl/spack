# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDebtcollector(PythonPackage):
    """
    A collection of Python deprecation patterns and strategies that help you
    collect your technical debt in a non-destructive manner.
    """

    homepage = "https://docs.openstack.org/debtcollector/latest"
    pypi = "debtcollector/debtcollector-2.2.0.tar.gz"

    maintainers("haampie")

    version("2.2.0", sha256="787981f4d235841bf6eb0467e23057fb1ac7ee24047c32028a8498b9128b6829")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-pbr@2.0.0:2.0,2.1.1:", type="build")

    depends_on("py-six@1.10.0:", type=("build", "run"))
    depends_on("py-wrapt@1.7.0:", type=("build", "run"))
