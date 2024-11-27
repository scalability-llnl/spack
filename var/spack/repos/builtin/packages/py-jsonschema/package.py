# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyJsonschema(PythonPackage):
    """Jsonschema: An(other) implementation of JSON Schema for Python."""

    homepage = "https://github.com/python-jsonschema/jsonschema"
    pypi = "jsonschema/jsonschema-3.2.0.tar.gz"

    license("MIT", checked_by="wdconinc")

    version("4.22.0", sha256="5b22d434a45935119af990552c862e5d6d564e8f6601206b305a61fdf661a2b7")
    version("4.21.1", sha256="85727c00279f5fa6bedbe6238d2aa6403bedd8b4864ab11207d07df3cc1b2ee5")
    version("4.20.0", sha256="4f614fd46d8d61258610998997743ec5492a648b33cf478c1ddc23ed4598a5fa")
    version("4.19.2", sha256="c9ff4d7447eed9592c23a12ccee508baf0dd0d59650615e847feb6cdca74f392")
    version("4.18.6", sha256="ce71d2f8c7983ef75a756e568317bf54bc531dc3ad7e66a128eae0d51623d8a3")
    version("4.17.3", sha256="0f864437ab8b6076ba6707453ef8f98a6a0d512a80e93f8abdb676f737ecb60d")
    version("4.16.0", sha256="165059f076eff6971bae5b742fc029a7b4ef3f9bcf04c14e4776a7605de14b23")
    version("4.10.0", sha256="8ff7b44c6a99c6bfd55ca9ac45261c649cefd40aaba1124c29aaef1bcb378d84")
    version("4.4.0", sha256="636694eb41b3535ed608fe04129f26542b59ed99808b4f688aa32dcf55317a83")
    version("3.2.0", sha256="c8a85b28d377cc7737e46e2d9f2b4f44ee3c0e1deac6bf46ddefc7187d30797a")
    version("3.1.1", sha256="2fa0684276b6333ff3c0b1b27081f4b2305f0a36cf702a23db50edb141893c3f")
    version("3.0.2", sha256="8d4a2b7b6c2237e0199c8ea1a6d3e05bf118e289ae2b9d7ba444182a2959560d")
    version("3.0.1", sha256="0c0a81564f181de3212efa2d17de1910f8732fa1b71c42266d983cd74304e20d")
    version("2.6.0", sha256="6ff5f3180870836cae40f06fa10419f557208175f13ad7bc26caa77beb1f6e02")
    version("2.5.1", sha256="36673ac378feed3daa5956276a829699056523d7961027911f064b52255ead41")

    # for versions @:4.5 this same variant was called format_nongpl
    variant(
        "format-nongpl",
        default=False,
        when="@3.2:",
        description="Enable format-nongpl functionality",
    )

    depends_on("python@3.8:", when="@4.18:", type="build")

    depends_on("py-hatchling", when="@4.10:", type="build")
    depends_on("py-hatch-vcs", when="@4.10:", type="build")
    depends_on("py-hatch-fancy-pypi-readme", when="@4.11:", type="build")

    depends_on("py-attrs@17.4:", when="@3:", type=("build", "run"))
    depends_on("py-attrs@22.2:", when="@4.18:", type=("build", "run"))
    depends_on("py-jsonschema-specifications@2023.03.6:", when="@4.18:", type=("build", "run"))
    depends_on("py-referencing@0.28.4:", when="@4.18:", type=("build", "run"))
    depends_on("py-rpds-py@0.7.1:", when="@4.18:", type=("build", "run"))
    depends_on("py-importlib-resources@1.4:", when="@4.2.1: ^python@:3.8", type=("build", "run"))
    depends_on("py-importlib-resources", when="@4.2.0 ^python@:3.8", type=("build", "run"))
    depends_on("py-pkgutil-resolve-name@1.3.10:", when="@4.10.0: ^python@:3.8")

    # Historical dependencies
    depends_on("py-setuptools@40.6.0:", when="@4:4.4", type="build")
    depends_on("py-setuptools", when="@3", type=("build", "run"))
    depends_on("py-setuptools", when="@:2", type="build")
    depends_on("py-vcversioner", when="@:2", type="build")
    depends_on("py-setuptools-scm+toml@3.4:", when="@4.4.0", type="build")
    depends_on("py-setuptools-scm", when="@3", type="build")
    depends_on("py-six@1.11:", when="@3", type=("build", "run"))
    depends_on("py-pyrsistent@0.14:", when="@3:4.17", type=("build", "run"))
    depends_on("py-importlib-metadata", when="@3.1.1:4.17 ^python@:3.7", type=("build", "run"))
    depends_on("py-typing-extensions", when="@4.3:4.17 ^python@:3.7", type=("build", "run"))

    conflicts("^py-pyrsistent@0.17.0:0.17.2")

    with when("+format-nongpl"):
        depends_on("py-fqdn", when="@4:", type=("build", "run"))
        depends_on("py-idna", type=("build", "run"))
        depends_on("py-isoduration", when="@4:", type=("build", "run"))
        depends_on("py-jsonpointer@1.14:", type=("build", "run"))
        depends_on("py-rfc3339-validator", type=("build", "run"))
        depends_on("py-rfc3986-validator@0.1.1:", type=("build", "run"))
        depends_on("py-uri-template", when="@4:", type=("build", "run"))
        depends_on("py-webcolors@1.11:", when="@4:", type=("build", "run"))
        depends_on("py-webcolors", type=("build", "run"))
