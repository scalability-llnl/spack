# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySlepc4py(PythonPackage):
    """This package provides Python bindings for the SLEPc package."""

    homepage = "https://gitlab.com/slepc/slepc4py"
    url = "https://slepc.upv.es/download/distrib/slepc4py-3.17.1.tar.gz"
    git = "https://gitlab.com/slepc/slepc.git"

    maintainers("joseeroman", "balay")

    license("BSD-2-Clause")

    version("main", branch="main")
    version("3.22.0", sha256="53db52a72e126787768732790ca73dbc6ff6e49d4d1152e9c3641ba71b97738e")
    version("3.21.2", sha256="f611ff74e4749f21445b2369dbd0edf404cdf639eecafd54187d0a2865d521a0")
    version("3.21.1", sha256="bc8e0e270643eef9b63b249080b8fe4433be0b697d55032d9f768ef310bd7b07")
    version("3.21.0", sha256="bfbd90162633486f67a448d2052e1f7182529d18e8bde87367bc4f4dd58e857f")
    version("3.20.2", sha256="89ebd1964edd0eb63d4dbfa977d6f35408f4e19a3da290696fd1197901544bd8")
    version("3.20.1", sha256="7e6d156f7b0891bfa0616b38a502460c62797f16ca146b321e16cce4cf139d07")
    version("3.20.0", sha256="56cbea1f56746136e5a934bf4a481e566f35e475cb950c0a5bce7d5c3cc7690a")
    version("3.19.2", sha256="da8b6a7aaaf5e4497b896b2e478c42dd9de4fb31da93eb294181bea3bb60c767")
    version("3.19.1", sha256="68303f4acef8efc0542ab288a19159d0e6cdf313726f573e0bea2edb3d2c9595")
    version("3.19.0", sha256="ae84d33cce259c1d6ff64308b2f819d1c0f7b018e048f9049ec6d5be15614ba5")
    version("3.18.3", sha256="93c978f115683900a575026111ff2abe6f3ce4de8c21eec53c07dfd97ea43c85")
    version("3.18.2", sha256="402297fd8e583ed2618d2cba05e5cae8e9d0a2c3943812a1a138f431ef3479b3")
    version("3.18.1", sha256="4c2bc0947d6a9cdb209e3174b7f54fe7b029220e2c90106f52844e8f8795f8f0")
    version("3.18.0", sha256="aa83f46f942aca05ffcbc8be29b496f56837f564e0396f5b39cec4946654ee78")
    version("3.17.2", sha256="e5b235486b6901cd4ff0d94083f0e5eeacaef3a2893e1714769717ad488a3885")
    version("3.17.1", sha256="967d5d045526088ff5b7b2cde76f8b4d1fee3a2a68481f85224b0795e6613eb9")
    version("3.17.0", sha256="cab298eb794739579167fd60ff900db90476c4c93b4ae4e0204e989a6eeb3767")
    version("3.16.3", sha256="d97652efe60163d30c24eb1ef1b1ba98bb8239fd7452bdf8207c2505da48d77e")
    version("3.16.2", sha256="a3950b2d4876e8b7429cf5b7d0faed580a70bbd17735b0279aeda460a4a32e18")
    version("3.16.1", sha256="3ce93de975fa3966794efb09c315b6aff17e412197f99edb66bbfa71fc49093b")
    version("3.16.0", sha256="e18850ebccb1e7c59accfbdbe4d004402abbde7f4e1291b0d2c5b560b308fb88")
    version("3.15.2", sha256="c87135989c4d95b9c92a5b615a95eddc34b69dad9cc28b27d3cb7dfaec46177b")
    version("3.15.1", sha256="bcdab6d2101ae00e189f4b33072805358cee2dda806a6b6a8e3c2f1b9f619dfd")
    version("3.15.0", sha256="2f5f5cc25ab4dd3782046c65e97265b39be0cf9cc74c5c0100c3c580c3c32395")
    version("3.13.0", sha256="780eff0eea1a5217642d23cd563786ef22df27e1d772a1b0bb4ccc5701df5ea5")
    version("3.12.0", sha256="d8c06953b7d00f529a9a7fd016dfa8efdf1d05995baeea7688d1d59611f424f7")
    version("3.11.0", sha256="1e591056beee209f585cd781e5fe88174cd2a61215716a71d9eaaf9411b6a775")

    patch("ldshared.patch", when="@:3.18")

    depends_on("py-cython@3:", when="@3.20:", type="build")
    depends_on("py-cython@0.29.32:", when="^python@3.11:", type="build")
    depends_on("py-cython@0.24:", type="build")
    depends_on("py-setuptools", type="build")
    depends_on("py-numpy", type=("build", "run"))

    depends_on("py-petsc4py@main", when="@main", type=("build", "run"))
    depends_on("slepc@main", when="@main")
    for ver in [
        "3.22",
        "3.21",
        "3.20",
        "3.19",
        "3.18",
        "3.17",
        "3.16",
        "3.15",
        "3.13",
        "3.12",
        "3.11",
    ]:
        depends_on(f"py-petsc4py@{ver}", when=f"@{ver}", type=("build", "run"))
        depends_on(f"slepc@{ver}", when=f"@{ver}")

    @property
    def build_directory(self):
        import os

        if self.spec.satisfies("@main"):
            return os.path.join(self.stage.source_path, "src", "binding", "slepc4py")
        else:
            return self.stage.source_path

    @run_before("install")
    def cythonize(self):
        with working_dir(self.build_directory):
            python(join_path("conf", "cythonize.py"))
