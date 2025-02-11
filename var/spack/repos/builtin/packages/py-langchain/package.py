# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyLangchain(PythonPackage):
    """Building applications with LLMs through composability"""

    homepage = "https://www.github.com/hwchase17/langchain"
    pypi = "langchain/langchain-0.0.235.tar.gz"

    license("MIT", checked_by="qwertos")

    version("0.2.5", sha256="ffdbf4fcea46a10d461bcbda2402220fcfd72a0c70e9f4161ae0510067b9b3bd")
    version("0.0.262", sha256="2cb545cb855ce783f9f272f08a346018b087c0d842012d225ed479ac312624c8")
    version("0.0.235", sha256="6734849e111a4c60e187a1ce7856b31e623604326e48b96601316d108633abd1")
    version("0.0.101", sha256="ee3945c0b8f2d6ba34e5ba63d9362578290269d02999b0049206b508be11e5cc")

    depends_on("python@3.8.1:3", type=("build", "run"))
    depends_on("py-poetry-core@1:", type="build")

    with when("@0.0.101"):
        depends_on("py-pydantic@1", type=("build", "run"))
        depends_on("py-sqlalchemy@1", type=("build", "run"))
        depends_on("py-requests@2", type=("build", "run"))
        depends_on("py-pyyaml@6", type=("build", "run"))
        depends_on("py-numpy@1", type=("build", "run"))
        depends_on("py-dataclasses-json@0.5.7:0.5", type=("build", "run"))
        depends_on("py-tenacity@8.1:8", type=("build", "run"))
        depends_on("py-aiohttp@3.8.3:3", type=("build", "run"))

    with when("@0.0.235"):
        depends_on("py-pydantic@1", type=("build", "run"))
        depends_on("py-sqlalchemy@1.4:2", type=("build", "run"))
        depends_on("py-requests@2", type=("build", "run"))
        depends_on("py-pyyaml@5.4.1:", type=("build", "run"))
        depends_on("py-numpy@1", type=("build", "run"))
        depends_on("py-openapi-schema-pydantic@1.2:1", type=("build", "run"))
        depends_on("py-dataclasses-json@0.5.7:0.5", type=("build", "run"))
        depends_on("py-tenacity@8.1:8", type=("build", "run"))
        depends_on("py-aiohttp@3.8.3:3", type=("build", "run"))
        depends_on("py-async-timeout@4", when="^python@:3.10", type=("build", "run"))
        depends_on("py-numexpr@2.8.4:2", type=("build", "run"))
        depends_on("py-langsmith@0.0.7", type=("build", "run"))

    with when("@0.0.262"):
        depends_on("py-pydantic@1", type=("build", "run"))
        depends_on("py-sqlalchemy@1.4:2", type=("build", "run"))
        depends_on("py-requests@2", type=("build", "run"))
        depends_on("py-pyyaml@5.3:", type=("build", "run"))
        depends_on("py-numpy@1", type=("build", "run"))
        depends_on("py-openapi-schema-pydantic@1.2:1", type=("build", "run"))
        depends_on("py-dataclasses-json@0.5.7:0.5", type=("build", "run"))
        depends_on("py-tenacity@8.1:8", type=("build", "run"))
        depends_on("py-aiohttp@3.8.3:3", type=("build", "run"))
        depends_on("py-async-timeout@4", when="^python@:3.10", type=("build", "run"))
        depends_on("py-numexpr@2.8.4:2", type=("build", "run"))
        depends_on("py-langsmith@0.0.11:0.0", type=("build", "run"))

    with when("@0.2.5"):
        depends_on("py-langchain-core@0.2.7:0.2", type=("build", "run"))
        depends_on("py-langchain-text-splitters@0.2", type=("build", "run"))
        depends_on("py-langsmith@0.1.17:0.1", type=("build", "run"))
        depends_on("py-pydantic@1:2", type=("build", "run"))
        depends_on("py-sqlalchemy@1.4:2", type=("build", "run"))
        depends_on("py-requests@2", type=("build", "run"))
        depends_on("py-pyyaml@5.3:", type=("build", "run"))
        depends_on("py-aiohttp@3.8.3:3", type=("build", "run"))
        depends_on("py-tenacity@8.1:8", type=("build", "run"))
        depends_on("py-async-timeout@4:", type=("build", "run"), when="^python@:3.10")
        depends_on("py-numpy@1", type=("build", "run"), when="^python@:3.11")
        depends_on("py-numpy@1.26:1", type=("build", "run"), when="^python@3.12:")
