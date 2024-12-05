# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *

# Package automatically generated using 'pip2spack' converter


class PyHpbandster(PythonPackage):
    """
    A distributed Hyperband implementation with lots of room for improvement
    """

    homepage = "https://github.com/automl/HpBandSter"
    pypi = "hpbandster/hpbandster-0.7.4.tar.gz"
    maintainers("liuyangzhuan")

    version("0.7.4", sha256="49ffc32688155b509e62f3617b52ae15a96c9bff2c996a23df83f279106c5921")
    version("0.7.3", sha256="dd6c255f5dfe773a7f0c5ecf580b46a406d9f691303e2f849a14f7ae08ff9f13")
    version("0.7.2", sha256="24dd3311b14fa76ab8111062ced670ff888e7e99cad07dcc3398361689c09f90")
    version("0.7.1", sha256="41a55c95787eccd23def00f73013fbc9efad3cdc20d9e03270c7c959643dc5ff")
    version("0.7.0", sha256="b6a46c73cb6a62e2f2d20984087a3458cea056aef5aa0fc0cd606bdd116eed94")
    version("0.6.1", sha256="8812743b43b228dbf38fe2d5c5ecf238c6a742d02d8bdd264a2f193b96ca3b92")
    version("0.6.0", sha256="26e69a2f84c8d41bea2fd703f489453a3e9301dcb62f15271b16a3db4ccf225d")
    version("0.5.6", sha256="bc8a93638adda5cc0838c836402f18b456631363aefbfdf52942e9f8c7251893")

    depends_on("python@3:", type=("build", "run"))
    depends_on("py-configspace", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-statsmodels", type=("build", "run"))
    depends_on("py-netifaces", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-serpent", type=("build", "run"))
    depends_on("py-pyro4", type=("build", "run"))
    depends_on("py-setuptools", type="build")
