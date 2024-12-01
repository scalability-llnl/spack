# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGraphqlRelay(PythonPackage):
    """Relay library for graphql-core."""

    homepage = "https://github.com/graphql-python/graphql-relay-py"
    pypi = "graphql-relay/graphql-relay-2.0.1.tar.gz"

    maintainers("LydDeb")

    license("MIT")

    version("2.0.1", sha256="870b6b5304123a38a0b215a79eace021acce5a466bf40cd39fa18cb8528afabb")

    depends_on("py-setuptools", type="build")
    depends_on("py-graphql-core@2.2:2", type=("build", "run"), when="@2")
    depends_on("py-six@1.12:", type=("build", "run"), when="@2")
    depends_on("py-promise@2.2:2", type=("build", "run"), when="@2")
