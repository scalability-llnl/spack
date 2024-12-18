# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Rdkit(CMakePackage):
    """RDKit is a collection of cheminformatics and machine-learning
    software written in C++ and Python."""

    homepage = "https://www.rdkit.org"
    url = "https://github.com/rdkit/rdkit/archive/refs/tags/Release_2021_03_2.tar.gz"

    maintainers("bvanessen", "RMeli")

    license("BSD-3-Clause")

    version("2024_03_3", sha256="52f79c6bf1d446cdb5c86a35de655d96bad0c52a5f4ecbe15f08eaf334e6f76a")
    version("2023_03_1", sha256="db346afbd0ba52c843926a2a62f8a38c7b774ffab37eaf382d789a824f21996c")
    version("2022_09_5", sha256="2efe7ce3b527df529ed3e355e2aaaf14623e51876be460fa4ad2b7f7ad54c9b1")
    version("2021_09_5", sha256="f720b3f6292c4cd0a412a073d848ffac01a43960082e33ee54b68798de0cbfa1")
    version("2021_09_4", sha256="ce192e85bbdc1dcf24d327197229099c8625ee20ef022fcbd980791fdbfc7203")
    version("2021_09_3", sha256="3d9d47e9ea3f7563ca83bf24fc6d3419c3892ea77d831e1cf68d81f602ad1afc")
    version("2021_09_2", sha256="1a6b41e4c5e2f1a98acfc9c0aa46aa32a97323f0531457d69fcdc70c4a964140")
    version(
        "2021_09_1b1", sha256="114935d980c4c52a1113aae26cd752dac6f24559b3098482663855f1b8c3e2a3"
    )
    version("2021_09_1", sha256="4d8d38adebdb0da51171ba67c6664555cb33d3fb5c62e35c8562d799dd812761")
    version("2021_03_5", sha256="ee7ed4189ab03cf805ab9db59121ab3ebcba4c799389d053046d7cab4dd8401e")
    version("2021_03_4", sha256="bed309df7f1e2ea25736a986cf951325681142ee49468b1c62d020a109d2ef52")
    version("2021_03_3", sha256="e95f07adaee9280df077cb147210ee75e16957d81687ab0836d62ebf1f6f715f")
    version("2021_03_2", sha256="9907a745405cc915c65504046e446199f8ad03d870714de57c27d3738f330fe4")
    version(
        "2021_03_1b1", sha256="2cd0673b289ba756c76a1bf57cf19e147ac4a9f6ecf9e79cc3dd86c8d39be414"
    )
    version("2021_03_1", sha256="9495f797a54ac70b3b6e12776de7d82acd7f7b5d5f0cc1f168c763215545610b")
    version("2020_09_5", sha256="85cec9618e7ef6365b9b908ed674c073d898b6627521cc7fd8c2e05fea8a5def")
    version("2020_09_4", sha256="9e734ca8f99d8be1ef2ac51efb67c393c62e88b98cfa550d6173ce3eaa87b559")
    version("2020_09_3", sha256="aa95bf3cbeef287eeb6d9759ff0992d2f92f2171b1758af71b7c9a0ec97a0660")
    version("2020_09_2", sha256="44663970859c0ec993f94a56b692231557df02c267853a2ee3c1f609cef93ae9")
    version(
        "2020_09_1b1", sha256="d9d836dc38cc45db44698e33325901452c94df9add10dd2675674594af1b73c2"
    )
    version("2020_09_1", sha256="ac105498be52ff77f7e9328c41d0e61a2318cac0789d6efc30f5f50dc78a992c")
    version("2020_03_6", sha256="a3663295a149aa0307ace6d1995094d0334180bc8f892fa325558a110154272b")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("freetype", default=True, description="Build freetype support")

    with when("@2022_09_5:"):
        variant(
            "python",
            default=True,
            when="@2022_09_5:",
            description="Build standard Python wrappers",
        )
        variant("contrib", default=False, description="Build Contrib directory")
        variant("freesasa", default=False, description="Build freesasa wrapper")
        variant("coordgen", default=True, description="Build coordgen wrapper")
        variant("maeparser", default=True, description="Build MAE parser wrapper")
        variant("yaehmop", default=True, description="Build YAeHMOP wrapper")
        variant("xyz2mol", default=False, description="Build support for RDKit xyz2mol")
        variant("descriptors3d", default=True, description="Build 3D descriptors calculators")

        depends_on("freesasa", when="+freesasa")
        depends_on("coordgen", when="+coordgen")
        depends_on("maeparser", when="+maeparser")
        depends_on("eigen@3:", when="+descriptors3d")
        depends_on("python@3:", when="+python")
        depends_on("py-numpy", when="+python")
        # https://github.com/rdkit/rdkit/issues/7477
        depends_on("py-numpy@:1", when="@:2024.03.3+python")

        extends("python", when="+python")

        conflicts("+xyz2mol", when="~yaehmop", msg="XY2MOL requires YAeHMOP")

    depends_on("boost@1.53.0: +python +serialization +iostreams +system")
    depends_on("sqlite")
    depends_on("freetype", when="@2020_09_1: +freetype")

    with when("@:2021_09_5"):
        depends_on("python@3:")
        depends_on("py-numpy")
        # https://github.com/rdkit/rdkit/issues/7477
        depends_on("py-numpy@:1")
        extends("python")

    def cmake_args(self):
        args = [
            "-DRDK_INSTALL_INTREE=OFF",
            self.define_from_variant("RDK_BUILD_FREETYPE_SUPPORT", "freetype"),
        ]
        if "@2022_09_5:" in self.spec:
            args.extend(
                [
                    self.define_from_variant("RDK_BUILD_PYTHON_WRAPPERS", "python"),
                    self.define_from_variant("RDK_BUILD_CONTRIB", "contrib"),
                    self.define_from_variant("RDK_BUILD_FREESASA_SUPPORT", "freesasa"),
                    self.define_from_variant("RDK_BUILD_COORDGEN_SUPPORT", "coordgen"),
                    self.define_from_variant("RDK_BUILD_MAEPARSER_SUPPORT", "maeparser"),
                    self.define_from_variant("RDK_BUILD_XYZ2MOL_SUPPORT", "xyz2mol"),
                    self.define_from_variant("RDK_BUILD_DESCRIPTORS3D", "descriptors3d"),
                ]
            )

        return args
