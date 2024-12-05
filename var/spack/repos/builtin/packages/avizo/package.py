# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import tarfile

from spack.package import *


class Avizo(Package):
    """Avizo is a 3D analysis software for scientific and industrial data.
    Wherever three-dimensional imaging data sets need to be processed, in
    materials science, geosciences or engineering applications, Avizo offers
    abundant state-of-the-art image data processing, exploration and analysis
    features within an intuitive workflow and easy-to-use graphical user
    interface."""

    homepage = "https://www.thermofisher.com/sa/en/home/industrial/electron-microscopy/electron-microscopy-instruments-workflow-solutions/3d-visualization-analysis-software.html"

    manual_download = True

    license("GPL-3.0")

    version(
        "2020.1",
        sha256="9321aaa276567eebf116e268353c33a4c930d768d22793f921338e1d8cefe991",
        url=f"file://{os.getcwd()}/Avizo-20201-Linux64-gcc48.bin",
        expand=False,
    )
    version(
        "2019.4",
        sha256="a637720535bcbe254ab56368004a9544c64ec36186373fa24f26cee279685248",
        url=f"file://{os.getcwd()}/Avizo-20194-Linux64-gcc48.bin",
        expand=False,
    )
    version(
        "2019.3",
        sha256="be109df81e2f7238f234862367841dae05e76cc62218c1f36b1d9bc9514ce5f7",
        url=f"file://{os.getcwd()}/Avizo-20193-Linux64-gcc48.bin",
        expand=False,
    )
    version(
        "9.7.0",
        sha256="9c9b9e81957387f4218df0c5adbb80717e9ae80ab3ca6ff8da523f7f499dcc5b",
        url=f"file://{os.getcwd()}/Avizo-970-Linux64-gcc44.bin",
        expand=False,
    )

    gcc_ver = {"9.7.0": "44", "2019.3": "48", "2019.4": "48", "2020.1": "48"}

    install_dir = {
        "9.7.0": "Avizo-9.7.0",
        "2019.3": join_path("..", "Avizo"),
        "2019.4": join_path("..", "Avizo"),
        "2020.1": join_path("..", "Avizo"),
    }

    # Licensing
    license_required = True
    license_comment = "#"
    license_files = ["share/license/password.dat"]
    license_vars = ["MCSLMD_LICENSE_FILE"]

    def setup_run_environment(self, env):
        env.set("MCSLMD_LICENSE_FILE", join_path(self.prefix.share.license, "password.dat"))

    def install(self, spec, prefix):
        ver = self.version.joined
        sh = which("sh")
        sh(f"Avizo-{ver}-Linux64-gcc{self.gcc_ver[self.version.string]}.bin", "--noexec", "--keep")

        with working_dir("Avizo"):
            avizo_tar = tarfile.open(
                name="Avizo-{}-Linux64-gcc{}.tar.bz2".format(
                    self.version, self.gcc_ver[self.version.string]
                )
            )
            avizo_tar.extractall()

            with working_dir(self.install_dir[self.version.string]):
                install_tree("bin", prefix.bin)
                install_tree("lib", prefix.lib)
                install_tree("data", prefix.data)
                install_tree("share", prefix.share)
                install_tree("python", prefix.python)
