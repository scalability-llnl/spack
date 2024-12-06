# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNeptuneClient(PythonPackage):
    """
    Flexible metadata store for MLOps, built for research and
    production teams that run a lot of experiments.
    """

    homepage = "https://neptune.ai/"
    pypi = "neptune-client/neptune-client-0.16.7.tar.gz"

    version("0.16.7", sha256="9b8bf2f59cb6b7ed6d96ea221b68ea20d9d481a1a4672d8173648ef998134454")
    version("0.16.1", sha256="821238f510486feacd87c745f4646916259a416545ab678b47195729c071f249")

    depends_on("python@3.7.0:", type=("build", "run"))
    depends_on("py-setuptools", type="build")

    depends_on("py-versioneer", type="build")
    depends_on("py-bravado", type=("build", "run"))
    depends_on("py-click@7.0:", type=("build", "run"))
    depends_on("py-future@0.17.1:", type=("build", "run"))
    depends_on("py-oauthlib@2.1.0:", type=("build", "run"))
    depends_on("py-pandas", type=("build", "run"))
    depends_on("pil@1.1.6:", type=("build", "run"))
    depends_on("py-pyjwt", type=("build", "run"))
    depends_on("py-requests@2.20.0:", type=("build", "run"))
    depends_on("py-requests-oauthlib@1.0.0:", type=("build", "run"))
    depends_on("py-six@1.12.0:", type=("build", "run"))
    depends_on("py-websocket-client@0.35:0,1.0.1:", type=("build", "run"))
    depends_on("py-gitpython@2.0.8:", type=("build", "run"))
    depends_on("py-boto3@1.16.0:", type=("build", "run"))
    depends_on("py-packaging", type=("build", "run"))
    depends_on("py-urllib3", type=("build", "run"))
    depends_on("py-dataclasses@0.6:", when="^python@:3.6", type=("build", "run"))
    depends_on("py-swagger-spec-validator@2.7.4:", type=("build", "run"))
    depends_on("py-psutil", type=("build", "run"))
    depends_on("py-jsonschema@:3", type=("build", "run"))
