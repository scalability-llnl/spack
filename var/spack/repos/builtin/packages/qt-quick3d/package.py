# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class QtQuick3d(CMakePackage):
    """A new module and API for defining 3D content in Qt Quick."""

    homepage = "https://www.qt.io"
    url = "https://github.com/qt/qtquick3d/archive/refs/tags/v6.2.3.tar.gz"
    list_url = "https://github.com/qt/qtquick3d/tags"

    maintainers = ["wdconinc", "sethrj"]

    version("6.2.4", sha256="7292ed4373a92913c6811f2faa5191f0426f84bd93a3f6eb7d54b62626b56db5")
    version("6.2.3", sha256="35d06edbdd83b7d781b70e0bada18911fa9b774b6403589d5b21813a73584d80")

    generator = "Ninja"

    # Changing default to Release for typical use in HPC contexts
    variant(
        "build_type",
        default="Release",
        values=("Release", "Debug", "RelWithDebInfo", "MinSizeRel"),
        description="CMake build type",
    )

    depends_on("cmake@3.16:", type="build")
    depends_on("ninja", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("python", when="@5.7.0:", type="build")

    depends_on("assimp@5.0.1:")

    _versions = ["6.2.4", "6.2.3"]
    for v in _versions:
        depends_on("qt-base@" + v, when="@" + v)
        depends_on("qt-declarative@" + v, when="@" + v)
        depends_on("qt-quicktimeline@" + v, when="@" + v)

    def patch(self):
        import os
        import shutil

        vendor_dir = join_path(self.stage.source_path, "src/3rdparty")
        vendor_deps_to_keep = ["xatlas"]
        with working_dir(vendor_dir):
            for dep in os.listdir():
                if os.path.isdir(dep):
                    if dep not in vendor_deps_to_keep:
                        shutil.rmtree(dep)

    def cmake_args(self):
        args = [
            # Qt components typically install cmake config files in a single prefix
            self.define("QT_ADDITIONAL_PACKAGES_PREFIX_PATH", self.spec["qt-declarative"].prefix),
            self.define("FEATURE_quick3d_assimp", True),
            self.define("FEATURE_system_assimp", True),
        ]
        return args
