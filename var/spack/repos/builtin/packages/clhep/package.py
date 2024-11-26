# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Clhep(CMakePackage):
    """CLHEP is a C++ Class Library for High Energy Physics."""

    homepage = "https://proj-clhep.web.cern.ch/proj-clhep/"
    url = "https://proj-clhep.web.cern.ch/proj-clhep/dist1/clhep-2.4.1.3.tgz"
    list_url = "https://proj-clhep.web.cern.ch/proj-clhep/"
    list_depth = 1

    tags = ["hep"]

    maintainers("drbenmorgan")

    version("2.4.7.1", sha256="1c8304a7772ac6b99195f1300378c6e3ddf4ad07c85d64a04505652abb8a55f9")
    version("2.4.7.0", sha256="7fa460030bc1a804ea7da8cce7611b93261493bbb66c3cfd3ceec935d7e1b8d3")
    version("2.4.6.4", sha256="49c89330f1903ef707d3c5d79c16a7c5a6f2c90fc290e2034ee3834809489e57")
    version("2.4.6.3", sha256="fcd007f11b10ba4af28d027222b63148d0eb44ff7a082eee353bdf921f9c684a")
    version("2.4.6.2", sha256="aded73e49bac85a5b4e86f64a0ee3d6f3cfe5551b0f7731c78b6d8f9dac6e8dc")
    version("2.4.6.0", sha256="e8d16debb84ced28e40e9ae84789cf5a0adad45f9213fbac3ce7583e06caa7b1")
    version("2.4.5.4", sha256="983fb4ea1fe423217fe9debc709569495a62a3b4540eb790d557c5a34dffbbb6")
    version("2.4.5.3", sha256="45f63eeb097f02fe67b86a7dadbf10d409b401c28a1a3e172db36252c3097c13")
    version("2.4.5.1", sha256="2517c9b344ad9f55974786ae6e7a0ef8b22f4abcbf506df91194ea2299ce3813")
    version("2.4.4.0", sha256="5df78c11733a091da9ae5a24ce31161d44034dd45f20455587db85f1ca1ba539")
    version("2.4.1.3", sha256="27c257934929f4cb1643aa60aeaad6519025d8f0a1c199bc3137ad7368245913")
    version("2.4.1.2", sha256="ff96e7282254164380460bc8cf2dff2b58944084eadcd872b5661eb5a33fa4b8")
    version("2.4.1.0", sha256="d14736eb5c3d21f86ce831dc1afcf03d423825b35c84deb6f8fd16773528c54d")
    version("2.4.0.4", sha256="eb013841c57990befa1e977a11a552ab8328733c1c3b6cecfde86da40dc22113")
    version("2.4.0.2", sha256="1e9891c5badb718c24933e7a5c6ee4d64fd4d5cf3a40c150ad18e864ec86b8a4")
    version("2.4.0.1", sha256="4c7e2c6ac63e0237100e4ddcbfdc3d7e7dc6592f95bdbdcc0e43a6892b9fd6e0")
    version("2.4.0.0", sha256="5e5cf284323898b4c807db6e684d65d379ade65fe0e93f7b10456890a6dee8cc")
    version("2.3.4.6", sha256="3e53947036f8570c7a08bed670a862426dbca17328afcecd6c875d8487fef204")
    version("2.3.4.5", sha256="1199d04626cb8bc1307e282b143018691077cc61fe2f286a382030262eda8764")
    version("2.3.4.4", sha256="e54de15ffa5108a1913c4910845436345c89ddb83480cd03277a795fafabfb9d")
    version("2.3.4.3", sha256="1019479265f956bd660c11cb439e1443d4fd1655e8d51accf8b1e703e4262dff")
    version("2.3.4.2", sha256="6d1e15ccbe1ca6e71d541e78ca7e8c9f3d986ee0da5177a4b8cda00c619dc691")
    version("2.3.3.2", sha256="4e69a5afb1b7ecc435395195140afc85bbbb9f4d3572f59451c3882f3015a7c1")
    version("2.3.3.1", sha256="cd74bfae4773620dd0c7cc9c1696a08386931d7e47a3906aa632cc5cb44ed6bd")
    version("2.3.3.0", sha256="0bcae1bed8d3aa4256e3a553a4f60484312f2121dcc83492a40f08a70881c8c0")
    version("2.3.2.2", sha256="885481ae32c2f31c3b7f14a5e5d68bc56dc3df0c597be464d7ffa265b8a5a1af")
    version("2.3.1.1", sha256="0e2b170df99176feb0aa4f20ea3b33463193c086682749790c5b9b79388d0ff4")
    version("2.3.1.0", sha256="66272ae3100d3aec096b1298e1e24ec25b80e4dac28332b45ec3284023592963")
    version("2.3.0.0", sha256="63e77f4f34baa5eaa0adb1ca2438734f2d6f5ca112d830650dd005a6109f2397")
    version("2.2.0.8", sha256="f735e236b1f023ba7399269733b2e84eaed4de615081555b1ab3af25a1e92112")
    version("2.2.0.5", sha256="92e8b5d32ae96154edd27d0c641ba048ad33cb69dd4f1cfb72fc578770a34818")
    version("2.2.0.4", sha256="9bf7fcd9892313c8d1436bc4a4a285a016c4f8e81e1fc65bdf6783207ae57550")
    version("2.1.2.3", sha256="4353231be09c134507092161cd3ced27a065ca0ebb31ee0256e60a8163c47c3b")

    depends_on("cxx", type="build")  # generated

    variant(
        "cxxstd",
        default="11",
        values=(
            "11",
            "14",
            conditional("17", when="@2.3.4.3:"),
            conditional("20", when="@2.4.6.4:"),
        ),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    depends_on("cmake@2.8.12.2:", when="@2.2.0.4:2.3.0.0", type="build")
    depends_on("cmake@3.2:", when="@2.3.0.1:", type="build")

    variant("cms", default=False, description="Apply CMS-specific changes")

    root_cmakelists_dir = "CLHEP"  # Extra directory layer.

    patch("clhep-cms.patch", when="+cms", level=0)

    def patch(self):
        # Patched line removed since 2.3.2.2
        # https://gitlab.cern.ch/CLHEP/CLHEP/-/commit/5da6830d69c71dc178632f7f5121a3a00e379f94
        if self.spec.satisfies("@2.3.2.2:"):
            return

        filter_file(
            "SET CMP0042 OLD",
            "SET CMP0042 NEW",
            "%s/CLHEP/CMakeLists.txt" % self.stage.source_path,
        )

    def cmake_args(self):
        cmake_args = [
            "-DCLHEP_BUILD_CXXSTD=-std=c++{0}".format(self.spec.variants["cxxstd"].value)
        ]
        return cmake_args
