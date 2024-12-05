# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PySchemaSalad(PythonPackage):
    """Schema Annotations for Linked Avro Data (SALAD)"""

    homepage = "https://github.com/common-workflow-language/schema_salad"
    pypi = "schema-salad/schema-salad-8.3.20221209165047.tar.gz"

    license("Apache-2.0")

    version(
        "8.3.20221209165047",
        sha256="d97cc9a4d7c4255eb8000bcebaa8ac0d1d31801c921fd4113ab3051c1e326c7c",
    )

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools@45:", type="build")

    depends_on("py-requests@1:", type=("build", "run"))
    depends_on("py-ruamel-yaml@0.17.6:0.17.21", type=("build", "run"))
    depends_on("py-rdflib@4.2.2:6", type=("build", "run"))
    depends_on("py-mistune@2.0.3:2.0", type=("build", "run"))
    depends_on("py-cachecontrol@0.11.7:0.12+filecache", type=("build", "run"))

    depends_on("py-setuptools-scm@6.2:+toml", type="build")
    depends_on("py-mypy@0.991", type="build")
    depends_on("py-black@19.10b0:", type="build")
    depends_on("py-types-pkg-resources", type="build")
    depends_on("py-types-requests", type="build")
    depends_on("py-types-dataclasses", type="build")
    depends_on("py-types-setuptools", type="build")
