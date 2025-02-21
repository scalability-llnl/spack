# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Soqt(CMakePackage):
    """Old Coin GUI binding for Qt, replaced by Quarter"""

    homepage = "https://github.com/coin3d/soqt/"
    url = "https://github.com/coin3d/soqt/releases/download/v1.6.3/soqt-1.6.3-src.tar.gz"
    git = "https://github.com/coin3d/soqt/"

    depends_on("cxx", type="build")
    depends_on("cmake@3:", type="build")

    license("BSD-3-Clause", checked_by="paulgessinger")

    version("1.6.3", sha256="79342e89290783457c075fb6a60088aad4a48ea072ede06fdf01985075ef46bd")
    version("1.6.2", sha256="fb483b20015ab827ba46eb090bd7be5bc2f3d0349c2f947c3089af2b7003869c")
    version("1.6.1", sha256="80289d9bd49ffe709ab85778c952573f43f1c725ea958c6d5969b2e9c77bb3ba")

    depends_on("coin3d")
    depends_on("opengl")

    variant(
        "static_defaults",
        default=True,
        description="Enable statically linked in default materials",
    )
    variant("spacenav", default=True, description="Enable Space Navigator support")
    variant("tests", default=False, description="Build small test programs.")
    variant("iv", default=True, description="Enable extra Open Inventor extensions")

    depends_on("qmake")
    with when("^[virtuals=qmake] qt"):
        depends_on("qt@5 +gui +opengl")
    with when("^[virtuals=qmake] qt-base"):
        depends_on("qt-base@6 +gui +opengl +widgets")

    def cmake_args(self):
        args = [
            self.define_from_variant("COIN_IV_EXTENSIONS", "iv"),
            self.define_from_variant("WITH_STATIC_DEFAULTS", "static_defaults"),
            self.define_from_variant("HAVE_SPACENAV_SUPPORT", "spacenav"),
            self.define_from_variant("SOQT_BUILD_TESTS", "tests"),
        ]
        if self.spec.satisfies("^[virtuals=qmake] qt"):
            args.append(self.define("SOQT_USE_QT5", True))
            args.append(self.define("SOQT_USE_QT6", False))
        if self.spec.satisfies("^[virtuals=qmake] qt-base"):
            args.append(self.define("SOQT_USE_QT5", False))
            args.append(self.define("SOQT_USE_QT6", True))
        return args
