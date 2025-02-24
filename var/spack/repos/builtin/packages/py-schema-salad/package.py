# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PySchemaSalad(PythonPackage):
    """Schema Annotations for Linked Avro Data (SALAD)"""

    homepage = "https://github.com/common-workflow-language/schema_salad"
    pypi = "schema-salad/schema_salad-8.7.20241021092521.tar.gz"

    license("Apache-2.0")
    version(
        "8.7.20241021092521",
        sha256="287b27adff70e55dd715bfbea18bb1a58fd73de14b4273be4038559308089cdf",
    )
    version(
        "8.3.20221209165047",
        sha256="d97cc9a4d7c4255eb8000bcebaa8ac0d1d31801c921fd4113ab3051c1e326c7c",
    )

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("python@3.8:", when="@8.4.20230927144413:", type=("build", "run"))
    depends_on("python@3.9:", when="@8.7.20241021092521:", type=("build", "run"))
    depends_on("py-setuptools@45:", type="build")
    depends_on("py-setuptools@50:", when="@8.4.20231117150958:", type="build")

    depends_on("py-requests@1:", type=("build", "run"))
    depends_on("py-ruamel-yaml@0.17.6:0.17.21", type=("build", "run"))
    depends_on("py-ruamel-yaml@0.17.6:0.18", when="@8.4.20231113094720:", type=("build", "run"))
    depends_on("py-rdflib@4.2.2:6", type=("build", "run"))
    depends_on("py-mistune@2.0.3:2.0", type=("build", "run"))
    depends_on("py-cachecontrol@0.11.7:0.12+filecache", type=("build", "run"))
    depends_on(
        "py-cachecontrol@0.13.1:0.14+filecache",
        when="@8.7.20240820070935:8.7.20241021092521",
        type=("build", "run"),
    )

    depends_on("py-setuptools-scm@6.2:+toml", type="build")
    depends_on("py-setuptools-scm@8.0.4:8+toml", when="@8.4.20231024070348:", type="build")
    depends_on("py-mypy@0.961", when="@8.3.20220717184004:8.3.20221028160159", type="build")
    depends_on("py-mypy@0.991", when="@8.3.20221209165047:8.4.20230201194352", type="build")
    depends_on("py-mypy@1.12.1", when="@8.7.20241021092521", type="build")
    depends_on("py-black@19.10b0:", type="build")
    depends_on("py-black@19.10b0:24.10", when="@8.7.20241021092521:", type="build")
    depends_on("py-types-pkg-resources", when="@:8.4.20231117150958", type="build")
    depends_on("py-types-requests", type="build")
    depends_on("py-types-dataclasses", type="build")
    depends_on("py-types-setuptools", type="build")

    def url_for_version(self, version):
        url = (
            "https://files.pythonhosted.org/packages/source/s/schema-salad/schema{}salad-{}.tar.gz"
        )
        if version >= Version("8.5.20240503091721"):
            sep = "_"
        else:
            sep = "-"
        return url.format(sep, version)
