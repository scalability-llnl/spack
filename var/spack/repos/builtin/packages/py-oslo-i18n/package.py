# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyOsloI18n(PythonPackage):
    """
    The oslo.i18n library contain utilities for working with
    internationalization (i18n) features, especially translation for text
    strings in an application or library.
    """

    homepage = "https://docs.openstack.org/oslo.i18n"
    pypi = "oslo.i18n/oslo.i18n-5.0.1.tar.gz"

    maintainers("haampie")

    version("5.0.1", sha256="3484b71e30f75c437523302d1151c291caf4098928269ceec65ce535456e035b")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-pbr@2.0.0:2.0,2.1.1:", type=("build", "run"))

    depends_on("py-six@1.10.0:", type=("build", "run"))
