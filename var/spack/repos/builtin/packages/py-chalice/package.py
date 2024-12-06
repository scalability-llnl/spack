# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyChalice(PythonPackage):
    """Python Serverless Microframework for AWS."""

    homepage = "https://github.com/aws/chalice"
    url = "https://github.com/aws/chalice/archive/1.20.0.tar.gz"

    license("Apache-2.0")

    version("1.20.0", sha256="0504fa8492379a658b123a7aa173b008be1a01c5a06d65f8ef1f1e6b87515e33")
    version("1.19.0", sha256="6d2f9e2d39e836c9cf32451a39443bb8d08d8dfd5ddc75792519ec97817b4fdd")
    version("1.18.1", sha256="fb52dc3851998ebe41813a5448d8e5687cc64e734a174db6e7e677c634d87823")
    version("1.18.0", sha256="e3f2bdd4acdc07b153318d3601f0795ddfdcdc33f2b046925725d1e6f1b699ff")
    version("1.17.0", sha256="e6371fe5a53be4b24bfadb7b1b9cbe0aa2a494531e1f51a4b6b8bb4a680021f0")
    version("1.16.0", sha256="ed70f044bdc99b07056f98fd325e2e8f0ec46cd480eebf22e9214523239b8764")
    version("1.15.1", sha256="4a50028be3964b95082e8c2a74c546f8fc317b847c8bea1e7e86f3cfff979d6f")
    version("1.15.0", sha256="3c86cf23649a40ea3cb017a16231eb46ce8f0ffda022d3ae4cfc8af52e377100")
    version("1.14.1", sha256="d8034247c1e7698d0b4747b534fd06ce518dcbee91b4e7054efa75efe27fba2e")
    version("1.14.0", sha256="59a63a098c05309efc0285dd2e38f8415e8618d05c08821fb7660377e30bda22")

    depends_on("python@2.0:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-click@7.0:8.0", type=("build", "run"))
    depends_on("py-botocore@1.12.86:2.0.0", type=("build", "run"))
    depends_on("py-mypy-extensions@0.4.3", type=("build", "run"))
    depends_on("py-six@1.10.0:2.0.0", type=("build", "run"))
    depends_on("py-pip@9:20.0", type=("build", "run"))
    depends_on("py-attrs@19.3.0:20.0.0", type=("build", "run"))
    depends_on("py-jmespath@0.9.3:1.0.0", type=("build", "run"))
    depends_on("py-pyyaml@5.3.1:6.0.0", type=("build", "run"))
    depends_on("py-wheel", type=("build", "run"))
