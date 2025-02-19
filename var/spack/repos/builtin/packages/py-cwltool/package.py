# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyCwltool(PythonPackage):
    """Common workflow language reference implementation"""

    homepage = "https://github.com/common-workflow-language/cwltool"
    pypi = "cwltool/cwltool-3.1.20221201130942.tar.gz"

    license("Apache-2.0")
    maintainers("mr-c")

    version(
        "3.1.20241112140730",
        sha256="84f597429d964b54aaa0de427dcc24c94dd45aacae87311b3bdebe3258c4c900",
    )
    version(
        "3.1.20241024121129",
        sha256="fc04356416fef31746b12c9c96e6e077c9614e7a93b2282bc13985fbb3d89cdc",
    )
    version(
        "3.1.20241007082533",
        sha256="f7e65f276ebf40caaafef24992a6e3911ef5b260c6d1e884a2ab3068757f6936",
    )
    version(
        "3.1.20240909164951",
        sha256="4222c0bc21ac0be43da011fdf53bd6354f6203695f71a7e0fa46d8c3662db9ec",
    )
    version(
        "3.1.20240708091337",
        sha256="44794bd5e4e67210284f1d66f18ce9f765e3b258485f2e667faaa7e7486ac736",
    )
    # version(
    #     "3.1.20240508115724",
    #     sha256="72e238f281ac1622fc97a2bce970b475e0e8263d1579b0ba67359ef4ffbf0e2a",
    # )
    version(
        "3.1.20240404144621",
        sha256="41e0fdcf4650acfe5df482848b302d7003a53d98cb8596411380841182b41bcc",
    )
    version(
        "3.1.20240112164112",
        sha256="d646c9b3baac8b3549ddd82df66073739e2281b160515f4c5faa46476c8a3446",
    )
    version(
        "3.1.20231207110929",
        sha256="449f5bed0dc740184bafc44490d2674b5f34b2ae00b6851fddaf6900afd2293b",
    )
    version(
        "3.1.20231206180100",
        sha256="439d9c4088682660a4be1820e286fbef78579674e2dfe23fe5349e8e14c47c88",
    )
    version(
        "3.1.20231114134824",
        sha256="3047bd979978e4aeff4f9e51415d1d10e520f26cc09eac38bc467834aaf152ba",
    )
    version(
        "3.1.20231020140205",
        sha256="fbeb1eba7c57187a8651611702dad41576e36f4e04e75935837d6b1917c598df",
    )
    version(
        "3.1.20231020113452",
        sha256="ebbecded9c4b4fc25382ac20fca56f7b4a81bcfcfdf803c44432674587ac3326",
    )
    version(
        "3.1.20231016170136",
        sha256="0523b6b723203980bc855f85d23d583e61407c61d89a85d1706d30fa2a13ecdf",
    )
    version(
        "3.1.20230906142556",
        sha256="011433069e595b3de397874e2fc22bff6828475fd878f4dd7c01430e5768782e",
    )
    version(
        "3.1.20230719185429",
        sha256="608d91cab03756c7201446a0e4e0e05af66351effa91ac887beaa60148645b64",
    )
    version(
        "3.1.20230624081518",
        sha256="7adb9fc0bc0fd68b940c96bef6b72772f0d5f27399024cc912804c09de475847",
    )
    version(
        "3.1.20230601100705",
        sha256="9a5ce021c80e8c9276003c67caf26f163ce0fc03b3ca8b5828cfdb9a1e263fab",
    )
    version(
        "3.1.20230527103121",
        sha256="149d997734fff38c29530494fd5e1139b9b0c8ad62280e3e9da41a0c7a305d30",
    )
    version(
        "3.1.20230526180938",
        sha256="88fb324129a9649ab364dfc25ff9c0a1d5d3d71d215d5df7ebb7550f1ab8e878",
    )
    version(
        "3.1.20230513155734",
        sha256="e358a95783498b42f2d1ae93fef625e507f9f43a0eacee4e93f9e27d676cb666",
    )
    version(
        "3.1.20230425144158",
        sha256="b6307c536ec94a94cb9215a26057ea792b907144ca57b015699cb180ca309086",
    )
    version(
        "3.1.20230425122939",
        sha256="58c9886db72eb52a1cb655469bae7cb859b08a884078f01e3aa5b33ec6583dc2",
    )
    version(
        "3.1.20230424211314",
        sha256="87c5a3d40fb1a46288e82d2c81c9b631daf0da38aad481d7b91498c60fe155fe",
    )
    version(
        "3.1.20230325110543",
        sha256="ff4456d78b453c7f6ca94020af5752930eb35e0fd860ac23cbc3f4e30e9c98cb",
    )
    version(
        "3.1.20230302145532",
        sha256="3e6a64fe5d9184fac6cc62ba4e396e51545d4b7b342b79fb205b3e401a18c9dc",
    )
    version(
        "3.1.20230213100550",
        sha256="49c2778eabbb824010f2b423b1ae4540cca5a32d1e3bd4033552b724460ff218",
    )
    version(
        "3.1.20230209161050",
        sha256="fed2e604d249094df61a480baa7c493a2af0a8c9b6d8764c449a935756557298",
    )
    version(
        "3.1.20230127121939",
        sha256="2dd445ea05156fdf27d73b33cd3488c80c7605571f71930394a6c21554f69390",
    )
    version(
        "3.1.20221201130942",
        sha256="0152d8cdf6acaf3620f557b442941f577bff2851d9e2e866e6051ea48a37bdbe",
    )
    version(
        "3.1.20221109155812",
        sha256="82676ea315ce84fc4057d92c040af15dde3e897527ea4ae70c1033b0eca20c2a",
    )
    version(
        "3.1.20211107152837",
        sha256="ae1cd4626b5330457b1a62bcb2580f36f530264a80222f2cc17cf65899ebf04e",
    )

    extends("python@3.6:3", type=("build", "run"), when="@:3.1.20230719185429")
    extends("python@3.8:3", type=("build", "run"), when="@3.1.20230906142556:3.1.20241007082533")
    extends("python@3.9:3", type=("build", "run"), when="@3.1.20241024121129")
    depends_on("py-setuptools@45:", type="build")
    # depends_on("py-setuptools-scm@8.0.4:8+toml", type="build")
    # depends_on("py-types-setuptools", type="build")
    # depends_on("py-types-mock", type="build")
    depends_on("py-mypy@1.0", type="build", when="@3.1.20230209161050:3.1.20230213100550")
    depends_on("py-mypy@1.0.1", type="build", when="@3.1.20230302145532")
    depends_on("py-mypy@1.1.1", type="build", when="@3.1.20230325110543:3.1.20230425122939")
    depends_on("py-mypy@1.2.0", type="build", when="@3.1.20230425144158")
    depends_on("py-mypy@1.3.0", type="build", when="@3.1.20230513155734:3.1.20230906142556")
    depends_on("py-mypy@1.6.0", type="build", when="@3.1.20231016170136:3.1.20231114134824")
    depends_on("py-mypy@1.7.1", type="build", when="@3.1.20231206180100:3.1.20231207110929")
    depends_on("py-mypy@1.8.0", type="build", when="@3.1.20240112164112")
    depends_on("py-mypy@1.9.0", type="build", when="@3.1.20240404144621:3.1.20240404144621")
    # depends_on("py-mypy@1.10.0", type="build", when="@3.1.20240508115724")
    depends_on("py-mypy@1.10.1", type="build", when="@3.1.20240708091337")
    depends_on("py-mypy@1.11.2", type="build", when="@3.1.20240909164951:3.1.20241007082533")
    depends_on("py-mypy@1.13.0", type="build", when="@3.1.20241024121129:")
    depends_on(
        "py-types-pkg-resources", type="build", when="@3.1.20230209161050:3.1.20230513155734"
    )
    depends_on("py-types-requests", type="build", when="@3.1.20230209161050:")
    depends_on("py-types-psutil", type="build", when="@3.1.20230209161050:")
    depends_on("py-setuptools-scm@8.0.4:8+toml", type="build", when="@3.1.20231016170136:")

    depends_on("py-requests@2.6.1:", type=("build", "run"))
    depends_on("py-ruamel-yaml@0.16:0.17.21", type=("build", "run"), when="@:3.1.20230425144158")
    depends_on(
        "py-ruamel-yaml@0.16:0.17.26",
        type=("build", "run"),
        when="@3.1.20230513155734:3.1.20230513155734",
    )
    depends_on(
        "py-ruamel-yaml@0.16:0.17.27",
        type=("build", "run"),
        when="@3.1.20230526180938:3.1.20230601100705",
    )
    depends_on(
        "py-ruamel-yaml@0.16:0.17",
        type=("build", "run"),
        when="@3.1.20230624081518:3.1.20231020140205",
    )
    depends_on("py-ruamel-yaml@0.16:0.18", type=("build", "run"), when="@3.1.20231114134824:")
    depends_on("py-rdflib@4.2.2:6.2", type=("build", "run"), when="@:3.1.20230302145532")
    depends_on(
        "py-rdflib@4.2.2:6.3", type=("build", "run"), when="@3.1.20230325110543:3.1.20230719185429"
    )
    depends_on(
        "py-rdflib@4.2.2:7.0", type=("build", "run"), when="@3.1.20230906142556:3.1.20241007082533"
    )
    depends_on("py-rdflib@4.2.2:7.1", type=("build", "run"), when="@3.1.20241024121129")
    depends_on("py-shellescape@3.4.1:3.8", type=("build", "run"), when="@:3.1.20241007082533")
    depends_on(
        "py-schema-salad@8.2.20211104054942:8", type=("build", "run"), when="@:3.1.20221201130942"
    )
    depends_on(
        "py-schema-salad@8.4:8",
        type=("build", "run"),
        when="@3.1.20230127121939:3.1.20230719185429",
    )
    depends_on(
        "py-schema-salad@8.4.20230426093816:8",
        type=("build", "run"),
        when="@3.1.20230906142556:3.1.20240708091337",
    )
    depends_on("py-schema-salad@8.7:8", type=("build", "run"), when="@3.1.20240909164951:")
    depends_on("py-prov@1.5.1", type=("build", "run"))
    depends_on("py-bagit@1.6.4:", type=("build", "run"), when="@:3.1.20230526180938")
    depends_on("py-mypy-extensions", type=("build", "run"))
    depends_on("py-psutil@5.6.6:", type=("build", "run"))
    depends_on("py-typing-extensions", type=("build", "run"), when="@:3.1.20230906142556")
    depends_on("py-coloredlogs", type=("build", "run"))
    depends_on("py-pydot@1.4.1:", type=("build", "run"))
    depends_on("py-argcomplete", type=("build", "run"), when="@:3.1.20230719185429")
    depends_on("py-argcomplete@1.12.0:", type=("build", "run"), when="@3.1.20230906142556:")
    depends_on("py-pyparsing@:3.0.1,3.0.3:", type=("build", "run"), when="@:3.1.20230719185429")
    depends_on("py-cwl-utils@0.19:", type=("build", "run"), when="@:3.1.20221201130942")
    depends_on(
        "py-cwl-utils@0.22:", type=("build", "run"), when="@3.1.20230127121939:3.1.20231114134824"
    )
    depends_on("py-cwl-utils@0.32:", type=("build", "run"), when="@3.1.20231206180100:")
    depends_on("py-importlib-resources@1.4:", type=("build", "run"), when="@3.1.20230526180938:")
    depends_on("py-spython@0.3.0:", type=("build", "run"), when="@3.1.20231206180100:")
