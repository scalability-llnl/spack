# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PySchemaSalad(PythonPackage):
    """Schema Annotations for Linked Avro Data (SALAD)"""

    homepage = "https://github.com/common-workflow-language/schema_salad"
    pypi = "schema-salad/schema_salad-8.7.20241021092521.tar.gz"

    license("Apache-2.0")

    maintainers("mr-c")

    version(
        "8.8.20241204110045",
        sha256="a674840324b9b496d84d78adbdbfd9a1ba23f10468f2a8100b68b04e2077bbd5",
    )
    version(
        "8.7.20241021092521",
        sha256="287b27adff70e55dd715bfbea18bb1a58fd73de14b4273be4038559308089cdf",
    )
    version(
        "8.7.20241010092723",
        sha256="f0f15890402531bec4bb18a5dfbb592dae4413c71e444f82ada95274b83d34bc",
    )
    version(
        "8.7.20240905150001",
        sha256="1753891704aa5b6664cef45ef194ebdf984a84b1f71c7d1d68af61e67d3b0950",
    )
    version(
        "8.7.20240820070935",
        sha256="5f9ef40a35b14bd101f5833fd681c642f07f3d89f79279c63283ad5633bcdaf8",
    )
    version(
        "8.7.20240718183047",
        sha256="8174c62a6b108bd89a9391cc0dd5e8404f24a0773f3461cfd18983a61f1fe074",
    )
    version(
        "8.6.20240710082410",
        sha256="65a497f91994967a46206535eac5ff3d27b00f318b8b50ebc8dea43be73dd369",
    )
    # version(
    #     "8.5.20240503091721",
    #     sha256="ce836ffb4cfb340cebc9e7aac6b82c2970e3ca2f25922bc8cbb08ede31433bd1",
    # )
    version(
        "8.5.20240410123758",
        sha256="36da8097ece4cc327d5e1151179efb189043d7cd8d5ce282f5b369ad17647d7b",
    )
    version(
        "8.5.20240311110950",
        sha256="76bd1d0792622c12c5882cc8448bb9ce9a6083ca7d0c02e7884f746dd011fedc",
    )
    version(
        "8.5.20240102191335",
        sha256="7d32704f50e3fc6c096dc162084bf00bebce70aa762cb4a897239a64ae00a20c",
    )
    version(
        "8.5.20231201181309",
        sha256="ab8763701b7ef0f1147a458d2a58af2a70d7ac904050a199d76e76ca6fc4e1b2",
    )
    version(
        "8.4.20231117150958",
        sha256="b3e2c2fe00dfb943f8fa15893809bb241875abe0cdefa831cf5df2351dafc245",
    )
    version(
        "8.4.20231113094720",
        sha256="e6f1f5c216bc7aa446a300ea5f71c0ab19734df64ee55980c89b4ce4f5a9416a",
    )
    version(
        "8.4.20231024070348",
        sha256="a7cdd70f75a67f08ca5068cc4c4b6b266358953435d8519d6ae22458a0c53984",
    )
    version(
        "8.4.20230927144413",
        sha256="2018cca36ed29c304010fd89daf2f8e42ba7257efb4447af17bfb6cc59a81534",
    )
    version(
        "8.4.20230808163024",
        sha256="6a2e2fbfa1055f8c9347cb2046ca621be33c6bca1af372c89493c65fbabe29dd",
    )
    version(
        "8.4.20230606143604",
        sha256="f19a3d6614b4afecec93b9c7121d31ee01d8c1aa169b272d41844ca61d3d9af6",
    )
    version(
        "8.4.20230601112322",
        sha256="8d2c8ac3caf2eb404bdd94a4c2a0e31345c5cc0884801d1c5dc5ca86d18040b4",
    )
    version(
        "8.4.20230511084951",
        sha256="c96b6a81a40f4ee94b7c49416bdb41808428af368494053a33c168e33fbe484d",
    )
    version(
        "8.4.20230426093816",
        sha256="71627de53552955d91b094ce34832dd883fd48547b3dbca08f530d70deefcd32",
    )
    version(
        "8.4.20230213094415",
        sha256="c76728f168cbf9ee27059774a46530bf7f67ccd90ee46ddd62b60965ea8fdf5a",
    )
    version(
        "8.4.20230201194352",
        sha256="ad9b13f63a58d6fe58b485c9fc46469e9f7d49aa5067dc5064d98d87b08e5e69",
    )
    version(
        "8.4.20230128170514",
        sha256="159a6a00603ca4bd2abea605e1be472db9012bcb04ddb9c79ef7f71d264b9b1b",
    )
    version(
        "8.4.20230127112827",
        sha256="9e9b594cdbdebad57d6c64a40cf58b7e206eb196e556a77fe66ec33781f01896",
    )
    version(
        "8.3.20230109181936",
        sha256="e0fb8fbe793dda42133f374642be9f1af1651bbfb3ca37e341d8866d695de45a",
    )
    version(
        "8.3.20221209165047",
        sha256="d97cc9a4d7c4255eb8000bcebaa8ac0d1d31801c921fd4113ab3051c1e326c7c",
    )

    extends("python@3.6:3.11", type=("build", "run"), when="@:8.4.20230606143604")
    extends(
        "python@3.6:3.12", type=("build", "run"), when="@8.4.20230808163024:8.4.20230927144413"
    )
    extends(
        "python@3.8:3.12", type=("build", "run"), when="@8.4.20230927144413:8.7.20240820070935"
    )
    extends(
        "python@3.8:3.13", type=("build", "run"), when="@8.7.20240905150001:8.7.20241010092723"
    )
    extends("python@3.9:3.13", type=("build", "run"), when="@8.7.20241021092521:")
    depends_on("py-setuptools@45:", type="build", when="@:8.4.20231113094720")
    depends_on("py-setuptools@50:", type="build", when="@8.4.20231117150958:")

    depends_on("py-requests@1:", type=("build", "run"))
    depends_on("py-ruamel-yaml@0.17.6:0.17.21", type=("build", "run"), when="@:8.4.20230511084951")
    depends_on(
        "py-ruamel-yaml@0.17.6:0.17",
        type=("build", "run"),
        when="@8.4.20230601112322:8.4.20230927144413",
    )
    depends_on("py-ruamel-yaml@0.17.6:0.18", type=("build", "run"), when="@8.4.20231024070348:")
    depends_on("py-rdflib@4.2.2:6", type=("build", "run"), when="@:8.4.20230808163024")
    depends_on("py-rdflib@4.2.2:8", type=("build", "run"), when="@8.4.20230927144413:")
    depends_on("py-mistune@2.0.3:2.0", type=("build", "run"), when="@:8.5.20240102191335")
    depends_on("py-mistune@3.0", type=("build", "run"), when="@8.5.20240311110950")
    depends_on(
        "py-cachecontrol@0.11.7:0.12+filecache", type=("build", "run"), when="@:8.4.20230511084951"
    )
    depends_on(
        "py-cachecontrol@0.11.7:0.13+filecache",
        type=("build", "run"),
        when="@8.4.20230601112322:8.5.20240102191335",
    )
    depends_on(
        "py-cachecontrol@0.11.7:0.14+filecache",
        type=("build", "run"),
        when="@8.5.20240311110950:8.7.20240718183047",
    )
    depends_on(
        "py-cachecontrol@0.13.1:0.14+filecache",
        when="@8.7.20240820070935:8.7.20241010092723",
        type=("build", "run"),
    )
    depends_on(
        "py-cachecontrol@0.14:0.14+filecache", type=("build", "run"), when="@8.7.20241021092521:"
    )
    depends_on("py-mypy-extensions@1:", when="@8.4.20230128170514:", type=("build", "run"))
    depends_on("py-importlib-resources", type=("build", "run"), when="@8.4.20230808163024:")

    depends_on("py-setuptools-scm@6.2:7+toml", type="build", when="@:8.4.20230927144413")
    depends_on("py-setuptools-scm@8.0.4:8+toml", when="@8.4.20231024070348:", type="build")
    depends_on("py-mypy@0.961", when="@8.3.20220717184004:8.3.20221028160159", type="build")
    depends_on("py-mypy@0.991", when="@8.3.20221209165047:8.4.20230201194352", type="build")
    depends_on("py-mypy@0.991", type="build", when="@:8.4.20230201194352")
    depends_on("py-mypy@1.0.0", type="build", when="@8.4.20230213094415:8.4.20230426093816")
    depends_on("py-mypy@1.3.0", type="build", when="@8.4.20230511084951:8.4.20230606143604")
    depends_on("py-mypy@1.4.1", type="build", when="@8.4.20230808163024")
    depends_on("py-mypy@1.5.1", type="build", when="@8.4.20230927144413")
    depends_on("py-mypy@1.6.0", type="build", when="@8.4.20231024070348")
    depends_on("py-mypy@1.7.0", type="build", when="@8.4.20231113094720:8.5.20231201181309")
    depends_on("py-mypy@1.8.0", type="build", when="@8.5.20240102191335")
    depends_on("py-mypy@1.9.0", type="build", when="@8.5.20240311110950:8.5.20240410123758")
    # depends_on("py-mypy@1.10.0", type="build", when="@8.5.20240503091721")
    depends_on("py-mypy@1.10.1", type="build", when="@8.6.20240710082410:8.7.20240718183047")
    depends_on("py-mypy@1.11.1", type="build", when="@8.7.20240820070935")
    depends_on("py-mypy@1.11.2", type="build", when="@8.7.20240905150001:8.7.20241010092723")
    depends_on("py-mypy@1.12.1", type="build", when="@8.7.20241021092521:8.7.20241021092521")
    depends_on("py-mypy@1.13.0", type="build", when="@8.8.20241204110045:")
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

    def setup_build_environment(self, env):
        env.set("SCHEMA_SALAD_USE_MYPYC", "1")
        env.set("MYPYPATH", join_path(self.stage.source_path, "mypy-stubs"))
