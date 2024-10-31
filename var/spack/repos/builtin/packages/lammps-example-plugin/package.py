# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import datetime as dt

from spack.package import *
from spack.pkg.builtin.lammps import Lammps


class LammpsExamplePlugin(CMakePackage):
    """LAMMPS Example Plugin"""

    homepage = "https://www.lammps.org/"
    url = "https://github.com/lammps/lammps/archive/patch_1Sep2017.tar.gz"
    git = "https://github.com/lammps/lammps.git"

    maintainers("rbberger")

    license("GPL-2.0-only")

    # rules for new versions and deprecation
    # * new stable versions should be added to stable_versions set
    # * a stable version that has updates and any of its outdated update releases should be
    #   marked deprecated=True
    # * patch releases older than a stable release should be marked deprecated=True
    version("develop", branch="develop")
    version(
        "20240829",
        sha256="6112e0cc352c3140a4874c7f74db3c0c8e30134024164509ecf3772b305fde2e",
        preferred=True,
    )
    version("20240627", sha256="2174a99d266279823a8c57629ee1c21ec357816aefd85f964d9f859fe9222aa5")
    version("20240417", sha256="158b288725c251fd8b30dbcf61749e0d6a042807da92af865a7d3c413efdd8ea")
    version(
        "20240207.1", sha256="3ba62c2a1ed463fceedf313a1c3ea2997994aa102379a8d35b525ea424f56776"
    )
    version(
        "20240207",
        sha256="d518f32de4eb2681f2543be63926411e72072dd7d67c1670c090b5baabed98ac",
        deprecated=True,
    )
    version("20231121", sha256="704d8a990874a425bcdfe0245faf13d712231ba23f014a3ebc27bc14398856f1")
    version(
        "20230802.4", sha256="6eed007cc24cda80b5dd43372b2ad4268b3982bb612669742c8c336b79137b5b"
    )
    version(
        "20230802.3", sha256="6666e28cb90d3ff01cbbda6c81bdb85cf436bbb41604a87f2ab2fa559caa8510"
    )

    depends_on("cxx", type="build")

    def url_for_version(self, version):
        split_ver = str(version).split(".")
        vdate = dt.datetime.strptime(split_ver[0], "%Y%m%d")
        if len(split_ver) < 2:
            update = ""
        else:
            update = "_update{0}".format(split_ver[1])

        return "https://github.com/lammps/lammps/archive/{0}_{1}{2}.tar.gz".format(
            "stable" if str(version) in Lammps.stable_versions else "patch",
            vdate.strftime("%d%b%Y").lstrip("0"),
            update,
        )

    depends_on("lammps+plugin+lib+openmp-package")

    root_cmakelists_dir = "examples/plugins"

    def patch(self):
        with open("examples/plugins/CMakeLists.txt", "a") as f:
            print("include(GNUInstallDirs)", file=f)
            print(
                "install(TARGETS morse2plugin nve2plugin helloplugin zero2plugin morse2plugin "
                "LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}/lammps/plugins)",
                file=f,
            )
