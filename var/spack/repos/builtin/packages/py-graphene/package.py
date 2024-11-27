# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGraphene(PythonPackage):
    """GraphQL Framework for Python."""

    homepage = "https://github.com/graphql-python/graphene"
    pypi = "graphene/graphene-3.3.tar.gz"

    maintainers("LydDeb")

    license("MIT")

    version("2.1.9", sha256="b9f2850e064eebfee9a3ef4a1f8aa0742848d97652173ab44c82cc8a62b9ed93")

    depends_on("py-setuptools", type="build")
    depends_on("py-graphql-core@2.1:2", type=("build", "run"))
    depends_on("py-graphql-relay@2", type=("build", "run"))
    depends_on("py-aniso8601@3:7", type=("build", "run"))
    depends_on("py-six@1.10.0:1", type=("build", "run"))
