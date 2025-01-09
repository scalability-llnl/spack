# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RStringi(RPackage):
    """Character String Processing Facilities.

    A multitude of character string/text/natural language processing tools:
    pattern searching (e.g., with 'Java'-like regular expressions or the
    'Unicode' collation algorithm), random string generation, case mapping,
    string transliteration, concatenation, sorting, padding, wrapping, Unicode
    normalisation, date-time formatting and parsing, and many more.  They are
    fast, consistent, convenient, and - owing to the use of the 'ICU'
    (International Components for Unicode) library - portable across all
    locales and platforms."""

    cran = "stringi"

    license("custom")

    version("1.8.4", sha256="c219f8f64d1a2bfd4ca9528452d44d30db1899af14f4b9ef248412443bc669f3")
    version("1.7.12", sha256="efe8ac2900001f986a75db5641fbb24587a6d23de274a6a85c39dfa58921e009")
    version("1.7.8", sha256="538918b1cd6ed1d8a2dd5ab146ba800a088e99f93c52dcd82615b6e127478b1c")
    version("1.7.6", sha256="0ea3d5afec5701977ff53de9afbaceb53b00aa34f5fb641cadc1eeb7759119ec")
    version("1.6.2", sha256="3a151dd9b982696370ac8df3920afe462f8abbd4e41b479ff8b66cfd7b602dae")
    version("1.5.3", sha256="224f1e8dedc962a676bc2e1f53016f6a129a0a38aa0f35daf6dece62ff714010")
    version("1.4.3", sha256="13cecb396b700f81af38746e97b550a1d9fda377ca70c78f6cdfc770d33379ed")
    version("1.3.1", sha256="32df663bb6e9527e1ac265eec2116d26f7b7e62ea5ae7cc5de217cbb8defc362")
    version("1.1.5", sha256="651e85fc4ec6cf71ad8a4347f2bd4b00a490cf9eec20921a83bf5222740402f2")
    version("1.1.3", sha256="9ef22062e4be797c1cb6c2c8822ad5c237edb08b0318a96be8bd1930191af389")
    version("1.1.2", sha256="e50b7162ceb7ebae403475f6f8a76a39532a2abc82112db88661f48aa4b9218e")
    version("1.1.1", sha256="243178a138fe68c86384feb85ead8eb605e8230113d638da5650bca01e24e165")

    depends_on("r@2.14:", type=("build", "run"))
    depends_on("r@3.1:", type=("build", "run"), when="@1.6.1:")
    depends_on("r@3.4:", type=("build", "run"), when="@1.8.1:")
    depends_on("icu4c@52:")
    depends_on("icu4c@55:", when="@1.5.3:")
    # since version 1.6.1 there is also a SystemRequirement on C++11
