# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPandas(PythonPackage):
    """pandas is a fast, powerful, flexible and easy to use open source
    data analysis and manipulation tool, built on top of the Python
    programming language."""

    homepage = "https://pandas.pydata.org/"
    pypi = "pandas/pandas-1.2.0.tar.gz"

    skip_modules = ["pandas.tests", "pandas.plotting._matplotlib", "pandas.core._numba.kernels"]

    license("Apache-2.0")
    maintainers("adamjstewart", "rgommers")

    version("2.2.3", sha256="4f18ba62b61d7e192368b84517265a99b4d7ee8912f8708660fb4a366cc82667")
    version("2.2.2", sha256="9e79019aba43cb4fda9e4d983f8e88ca0373adbb697ae9c6c43093218de28b54")
    version("2.2.1", sha256="0ab90f87093c13f3e8fa45b48ba9f39181046e8f3317d3aadb2fffbb1b978572")
    version("2.2.0", sha256="30b83f7c3eb217fb4d1b494a57a2fda5444f17834f5df2de6b2ffff68dc3c8e2")
    version("2.1.4", sha256="fcb68203c833cc735321512e13861358079a96c174a61f5116a1de89c58c0ef7")
    version("2.1.3", sha256="22929f84bca106921917eb73c1521317ddd0a4c71b395bcf767a106e3494209f")
    version("2.1.2", sha256="52897edc2774d2779fbeb6880d2cfb305daa0b1a29c16b91f531a18918a6e0f3")
    version("2.1.1", sha256="fecb198dc389429be557cde50a2d46da8434a17fe37d7d41ff102e3987fd947b")
    version("2.1.0", sha256="62c24c7fc59e42b775ce0679cfa7b14a5f9bfb7643cfbe708c960699e05fb918")
    version("2.0.3", sha256="c02f372a88e0d17f36d3093a644c73cfc1788e876a7c4bcb4020a77512e2043c")
    version("2.0.2", sha256="dd5476b6c3fe410ee95926873f377b856dbc4e81a9c605a0dc05aaccc6a7c6c6")
    version("2.0.1", sha256="19b8e5270da32b41ebf12f0e7165efa7024492e9513fb46fb631c5022ae5709d")
    version("2.0.0", sha256="cda9789e61b44463c1c4fe17ef755de77bcd13b09ba31c940d20f193d63a5dc8")
    version("1.5.3", sha256="74a3fd7e5a7ec052f183273dc7b0acd3a863edf7520f5d3a1765c04ffdb3b0b1")
    version("1.5.2", sha256="220b98d15cee0b2cd839a6358bd1f273d0356bf964c1a1aeb32d47db0215488b")
    version("1.5.1", sha256="249cec5f2a5b22096440bd85c33106b6102e0672204abd2d5c014106459804ee")
    version("1.5.0", sha256="3ee61b881d2f64dd90c356eb4a4a4de75376586cd3c9341c6c0fcaae18d52977")
    version("1.4.4", sha256="ab6c0d738617b675183e5f28db32b5148b694ad9bba0a40c3ea26d96b431db67")
    version("1.4.3", sha256="2ff7788468e75917574f080cd4681b27e1a7bf36461fe968b49a87b5a54d007c")
    version("1.4.2", sha256="92bc1fc585f1463ca827b45535957815b7deb218c549b7c18402c322c7549a12")
    version("1.4.1", sha256="8db93ec98ac7cb5f8ac1420c10f5e3c43533153f253fe7fb6d891cf5aa2b80d2")
    version("1.4.0", sha256="cdd76254c7f0a1583bd4e4781fb450d0ebf392e10d3f12e92c95575942e37df5")
    version("1.3.5", sha256="1e4285f5de1012de20ca46b188ccf33521bff61ba5c5ebd78b4fb28e5416a9f1")
    version("1.3.4", sha256="a2aa18d3f0b7d538e21932f637fbfe8518d085238b429e4790a35e1e44a96ffc")
    version("1.3.3", sha256="272c8cb14aa9793eada6b1ebe81994616e647b5892a370c7135efb2924b701df")
    version("1.3.2", sha256="cbcb84d63867af3411fa063af3de64902665bb5b3d40b25b2059e40603594e87")
    version("1.3.1", sha256="341935a594db24f3ff07d1b34d1d231786aa9adfa84b76eab10bf42907c8aed3")
    version("1.3.0", sha256="c554e6c9cf2d5ea1aba5979cc837b3649539ced0e18ece186f055450c86622e2")
    version("1.2.5", sha256="14abb8ea73fce8aebbb1fb44bec809163f1c55241bcc1db91c2c780e97265033")
    version("1.2.4", sha256="649ecab692fade3cbfcf967ff936496b0cfba0af00a55dfaacd82bdda5cb2279")
    version("1.2.3", sha256="df6f10b85aef7a5bb25259ad651ad1cc1d6bb09000595cab47e718cbac250b1d")
    version("1.2.2", sha256="14ed84b463e9b84c8ff9308a79b04bf591ae3122a376ee0f62c68a1bd917a773")
    version("1.2.1", sha256="5527c5475d955c0bc9689c56865aaa2a7b13c504d6c44f0aadbf57b565af5ebd")
    version("1.2.0", sha256="e03386615b970b8b41da6a68afe717626741bb2431cec993640685614c0680e4")
    version("1.1.5", sha256="f10fc41ee3c75a474d3bdf68d396f10782d013d7f67db99c0efbfd0acb99701b")
    version("1.1.4", sha256="a979d0404b135c63954dea79e6246c45dd45371a88631cdbb4877d844e6de3b6")
    version("1.1.3", sha256="babbeda2f83b0686c9ad38d93b10516e68cdcd5771007eb80a763e98aaf44613")
    version("1.1.2", sha256="b64ffd87a2cfd31b40acd4b92cb72ea9a52a48165aec4c140e78fd69c45d1444")
    version("1.1.1", sha256="53328284a7bb046e2e885fd1b8c078bd896d7fc4575b915d4936f54984a2ba67")
    version("1.1.0", sha256="b39508562ad0bb3f384b0db24da7d68a2608b9ddc85b1d931ccaaa92d5e45273")
    version("1.0.5", sha256="69c5d920a0b2a9838e677f78f4dde506b95ea8e4d30da25859db6469ded84fa8")
    version("1.0.4", sha256="b35d625282baa7b51e82e52622c300a1ca9f786711b2af7cbe64f1e6831f4126")
    version("1.0.3", sha256="32f42e322fb903d0e189a4c10b75ba70d90958cc4f66a1781ed027f1a1d14586")
    version("1.0.2", sha256="76334ba36aa42f93b6b47b79cbc32187d3a178a4ab1c3a478c8f4198bcd93a73")
    version("1.0.1", sha256="3c07765308f091d81b6735d4f2242bb43c332cc3461cae60543df6b10967fe27")
    version("1.0.0", sha256="3ea6cc86931f57f18b1240572216f09922d91b19ab8a01cf24734394a3db3bec")
    version("0.25.3", sha256="52da74df8a9c9a103af0a72c9d5fdc8e0183a90884278db7f386b5692a2220a4")
    version("0.25.2", sha256="ca91a19d1f0a280874a24dca44aadce42da7f3a7edb7e9ab7c7baad8febee2be")

    variant("performance", default=True, description="Build recommended performance dependencies")
    variant("excel", when="@1.4:", default=False, description="Build with support for Excel")

    depends_on("c", type="build")

    with default_args(type="build"):
        depends_on("py-meson-python@0.13.1:", when="@2.1:")
        depends_on("meson@1.2.1:", when="@2.1.1:")
        depends_on("meson@1.0.1:", when="@2.1.0")
        depends_on("py-cython@3.0.5:", when="@2.2:")
        depends_on("py-cython@0.29.33:2", when="@2.0:2.1")
        depends_on("py-cython@0.29.32:2", when="@1.4.4:1")
        depends_on("py-cython@0.29.30:2", when="@1.4.3")
        depends_on("py-cython@0.29.24:2", when="@1.3.4:1.4.2")
        depends_on("py-cython@0.29.21:2", when="@1.1.3:1.3.3")
        depends_on("py-cython@0.29.16:2", when="@1.1.0:1.1.2")
        depends_on("py-cython@0.29.13:2", when="@1.0")
        depends_on("py-versioneer+toml", when="@2:")

        # Historical dependencies
        depends_on("py-setuptools@61:", when="@2.0")
        depends_on("py-setuptools@51:", when="@1.3.2:1")
        depends_on("py-setuptools@38.6:", when="@1.3.0:1.3.1")
        depends_on("py-setuptools@24.2:", when="@:1.2")

    with default_args(type=("build", "run")):
        # Based on PyPI wheel versions
        depends_on("python@3.9:3.13", when="@2.2.3:")
        depends_on("python@3.9:3.12", when="@2.1.1:")
        depends_on("python@3.9:3.11", when="@2.1.0")
        depends_on("python@3.8:3.11", when="@1.5:2.0")
        depends_on("python@3.8:3.10", when="@1.4")
        depends_on("python@:3.10", when="@1.3.3:1.3")
        depends_on("python@:3.9", when="@1.1.3:1.3.2")
        depends_on("python@:3.8", when="@0.25.2:1.1.2")

        depends_on("py-numpy@1.22.4:", when="@2.1:")
        depends_on("py-numpy@1.20.3:", when="@1.5:")
        depends_on("py-numpy@1.18.5:", when="@1.4")
        depends_on("py-numpy@1.17.3:", when="@1.3")
        depends_on("py-numpy@1.16.5:", when="@1.2")
        depends_on("py-numpy@1.15.4:", when="@1.1")
        depends_on("py-numpy@1.13.3:", when="@1.0")
        # 'NUMPY_IMPORT_ARRAY_RETVAL' was removed in numpy@1.19
        depends_on("py-numpy@1.13.3:1.18", when="@0.25")
        # https://github.com/pandas-dev/pandas/issues/55519
        depends_on("py-numpy@:1", when="@:2.2.1")
        depends_on("py-python-dateutil@2.8.2:", when="@2:")
        depends_on("py-python-dateutil@2.8.1:", when="@1.4:")
        depends_on("py-python-dateutil@2.7.3:", when="@1.1:")
        depends_on("py-python-dateutil@2.6.1:", when="@0.25:")
        depends_on("py-python-dateutil")
        depends_on("py-pytz@2020.1:", when="@1.4:")
        depends_on("py-pytz@2017.3:", when="@1.2:")
        depends_on("py-pytz@2017.2:")
        depends_on("py-tzdata@2022.1:", when="@2:")

    with default_args(type="run"):
        with when("+performance"):
            depends_on("py-bottleneck@1.3.4:", when="@2.1:")
            depends_on("py-bottleneck@1.3.2:", when="@1.5:")
            depends_on("py-bottleneck@1.3.1:", when="@1.4:")
            depends_on("py-bottleneck@1.2.1:", when="@0.25:")
            depends_on("py-numba@0.55.2:", when="@2.1:")
            depends_on("py-numba@0.53.1:", when="@2.0:")
            depends_on("py-numexpr@2.8.0:", when="@2.1:")
            depends_on("py-numexpr@2.7.3:", when="@1.5:")
            depends_on("py-numexpr@2.7.1:", when="@1.4:")
            depends_on("py-numexpr@2.7.0:", when="@1.3:")
            depends_on("py-numexpr@2.6.8:", when="@1.2:")
            depends_on("py-numexpr@2.6.2:", when="@0.25:")

        with when("+excel"):
            # Excel dependencies for 1.4+ (not coded up for earlier versions)
            depends_on("py-odfpy@1.4.1:", when="@2.0:")
            depends_on("py-openpyxl@3.1:", when="@2.2:")
            depends_on("py-openpyxl@3.0.10:", when="@2.1:")
            depends_on("py-openpyxl@3.0.7:", when="@1.5:")
            depends_on("py-openpyxl@3.0.3:", when="@1.4:")
            depends_on("py-python-calamine@0.1.7:", when="@2.2:")
            depends_on("py-pyxlsb@1.0.10:", when="@2.2:")
            depends_on("py-pyxlsb@1.0.9:", when="@2.1:")
            depends_on("py-pyxlsb@1.0.8:", when="@1.5:")
            depends_on("py-pyxlsb@1.0.6:", when="@1.4:")
            depends_on("py-xlrd@2.0.1:", when="@2.2:")
            depends_on("py-xlrd@2.0.1:", when="@1.4:")
            depends_on("py-xlwt@1.3.0:", when="@1.4:1.5")
            depends_on("py-xlsxwriter@3.0.5:", when="@2.2:")
            depends_on("py-xlsxwriter@3.0.3:", when="@2.1:")
            depends_on("py-xlsxwriter@1.4.3:", when="@1.5:")
            depends_on("py-xlsxwriter@1.2.2:", when="@1.4:")
