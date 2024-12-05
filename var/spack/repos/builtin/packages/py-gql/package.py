# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyGql(PythonPackage):
    """This is a GraphQL client for Python. Plays nicely with
    graphene, graphql-core, graphql-js and any other GraphQL
    implementation compatible with the spec.
    GQL architecture is inspired by React-Relay and Apollo-Client."""

    homepage = "https://github.com/graphql-python/gql"
    pypi = "gql/gql-2.0.0.tar.gz"

    license("MIT")

    version("3.0.0a1", sha256="ecd8fd0b6a5a8bb5c9e1a97eefad3f267fc889bd03316211193640d49b3e4525")
    version("0.4.0", sha256="259b0c66d8dfe61feb06fe45b57713da0fe2e5ca13fa500a1fafc9bf2f195e81")

    depends_on("py-setuptools", type="build")
    depends_on("py-aiohttp@3.6.2", type=("build", "run"), when="@3.0:")
    depends_on("py-graphql-core@3.1.0:3.1", type=("build", "run"), when="@3.0:")
    depends_on("py-requests@2.23:2", type=("build", "run"), when="@3.0:")
    depends_on("py-websockets@8.1:8", type=("build", "run"), when="@3.0:")
    depends_on("py-yarl@1.4:1", type=("build", "run"), when="@3.0:")

    depends_on("py-graphql-core@2.0:2", type=("build", "run"), when="@0.4.0")
    depends_on("py-six@1.10.0:", type=("build", "run"), when="@0.4.0")
    depends_on("py-promise@2.0:2", type=("build", "run"), when="@0.4.0")
    depends_on("py-requests@2.12:2", type=("build", "run"), when="@0.4.0")
