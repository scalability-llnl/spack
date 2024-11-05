# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Soqt(CMakePackage):
    """Old Coin GUI binding for Qt, replaced by Quarter"""

    homepage = "https://github.com/coin3d/soqt/"
    url = "https://github.com/coin3d/soqt/releases/download/v1.6.3/soqt-1.6.3-src.tar.gz"
    git = "https://github.com/coin3d/soqt/"

    maintainers("paulgessinger")  # reluctantly

    depends_on("cxx", type="build")
    depends_on("cmake@3:", type="build")

    license("BSD-3-Clause", checked_by="paulgessinger")

    version("1.6.3", sha256="79342e89290783457c075fb6a60088aad4a48ea072ede06fdf01985075ef46bd")
    version("1.6.2", sha256="fb483b20015ab827ba46eb090bd7be5bc2f3d0349c2f947c3089af2b7003869c")
    version("1.6.1", sha256="80289d9bd49ffe709ab85778c952573f43f1c725ea958c6d5969b2e9c77bb3ba")
    version("1.6.0", sha256="9f535af59f07c907022815679681bd345c9dec2f408c74833f6b1b24bca40e1f")

    depends_on("coin3d")
    depends_on("opengl")

    variant("qt", default="6", values=("5", "6"), description="Qt version to use")
    variant(
        "static_defaults",
        default=True,
        description="Enable statically linked in default materials",
    )
    variant("spacenav", default=True, description="Enable Space Navigator support")
    variant("tests", default=False, description="Build small test programs.")
    variant("iv", default=True, description="Enable extra Open Inventor extensions")

    depends_on("qt +gui +opengl", when="qt=5")
    depends_on("qt-base +gui +opengl +widgets", when="qt=6")

    def cmake_args(self):
        args = [
            self.define_from_variant("COIN_IV_EXTENSIONS", "iv"),
            self.define_from_variant("WITH_STATIC_DEFAULTS", "static_defaults"),
            self.define_from_variant("HAVE_SPACENAV_SUPPORT", "spacenav"),
            self.define_from_variant("SOQT_BUILD_TESTS", "tests"),
        ]
        qtversion = self.spec.variants["qt"].value
        if qtversion == "5":
            args.append(self.define("SOQT_USE_QT5", True))
            args.append(self.define("SOQT_USE_QT6", False))
        else:
            args.append(self.define("SOQT_USE_QT5", False))
            args.append(self.define("SOQT_USE_QT6", True))
        return args
