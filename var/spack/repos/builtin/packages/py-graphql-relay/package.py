# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGraphqlRelay(PythonPackage):
    """Relay library for graphql-core."""

    homepage = "https://github.com/graphql-python/graphql-relay-py"
    pypi = "graphql-relay/graphql-relay-3.2.0.tar.gz"

    maintainers("LydDeb")

    version("2.0.1", sha256="870b6b5304123a38a0b215a79eace021acce5a466bf40cd39fa18cb8528afabb")
    version("0.5.0", sha256="1c9bce36612d26ab08dd25d45b192722a9c7b6af3cef7ff83a3f087540ca2216")


    depends_on("python@3.6:3.10", type=("build", "run"))
    depends_on("py-setuptools@59:69", type="build")
    depends_on("py-poetry-core@1", type="build")
    depends_on("py-graphql-core@2.2:2", type=("build", "run"), when="@2")
    depends_on("py-six@1.12:", type=("build", "run"), when="@2")
    depends_on("py-promise@2.2:2", type=("build", "run"), when="@2")
    depends_on("py-graphql-core@0.5.0:1", type=("build", "run"), when="@0")
    depends_on("py-typing-extensions@4.1:4", type=("build", "run"), when="^python@:3.7")
