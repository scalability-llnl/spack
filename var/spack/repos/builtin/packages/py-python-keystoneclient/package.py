# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPythonKeystoneclient(PythonPackage):
    """
    This is a client for the OpenStack Identity API, implemented by the
    Keystone team
    """

    homepage = "https://docs.openstack.org/python-keystoneclient"
    pypi = "python-keystoneclient/python-keystoneclient-4.2.0.tar.gz"

    maintainers("haampie")

    version("4.2.0", sha256="0248426e483b95de395086482c077d48e45990d3b1a3e334b2ec8b2e108f5a8a")

    depends_on("python@3.6:", type=("build", "run"))

    depends_on("py-pbr@2.0.0:2.0,2.1.1:", type="build")
    depends_on("py-setuptools", type="build")

    depends_on("py-debtcollector@1.2.0:", type=("build", "run"))
    depends_on("py-keystoneauth1@3.4.0:", type=("build", "run"))
    depends_on("py-oslo-config@5.2.0:", type=("build", "run"))
    depends_on("py-oslo-i18n@3.15.3:", type=("build", "run"))
    depends_on("py-oslo-serialization@2.18.0:2.19.0,2.19.2:", type=("build", "run"))
    depends_on("py-oslo-utils@3.33.0:", type=("build", "run"))
    depends_on("py-requests@2.14.2:", type=("build", "run"))
    depends_on("py-six@1.10.0:", type=("build", "run"))
    depends_on("py-stevedore@1.20.0:", type=("build", "run"))
