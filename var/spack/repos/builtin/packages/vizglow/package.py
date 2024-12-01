# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob
import os

from spack.package import *


class Vizglow(Package):
    """VizGlow software tool is used for high-fidelity multi-dimensional
    modeling of non-equilibrium plasma discharges.

    Note: VizGlow is licensed software. You will need to create an account on
    the EsgeeTech homepage and download VizGlow yourself. Spack will search
    your current directory for a file of this format. Alternatively, add this
    file to a mirror so that Spack can find it. For instructions on how to
    set up a mirror, see https://spack.readthedocs.io/en/latest/mirrors.html"""

    homepage = "https://esgeetech.com/products/vizglow-plasma-modeling/"
    manual_download = True

    version(
        "2.2alpha20",
        md5="2bef890c66f3a44aaf96f7c96788c89e",
        expand=False,
        url="file://{0}/VizGlow_v2.2alpha20-Linux-x86_64-R09December2016-Install".format(
            os.getcwd()
        ),
    )
    version(
        "2.2alpha17",
        md5="1de268564363e0ee86f9ffff1c3b82e1",
        expand=False,
        url="file://{0}/VizGlow_v2.2alpha17-R21November2016-Linux-x86_64-Install".format(
            os.getcwd()
        ),
    )
    version(
        "2.2alpha15",
        md5="be2b5044f30f2b2c3bbe87a0037bf228",
        expand=False,
        url="file://{0}/VizGlow_v2.2alpha15-Linux-x86_64-R31October2016-Install".format(
            os.getcwd()
        ),
    )

    # depends_on('mesa')  # TODO: mesa build doesn't work for me
    depends_on("zlib-api")
    depends_on("freetype")
    depends_on("fontconfig")
    depends_on("libxrender")
    depends_on("xterm")
    # Can't get mozjs to build, packagekit -> polkit -> mozjs
    # depends_on('packagekit+gtk')
    depends_on("libcanberra+gtk")

    # Licensing
    license_required = True
    license_comment = "#"
    license_files = ["esgeelm.lic"]
    license_vars = ["ESGEE_LICENSE_FILE"]

    def configure(self, prefix):
        # Dictionary of responses
        responses = {
            "CreateDesktopShortcut": "No",
            "CreateQuickLaunchShortcut": "No",
            "InstallDir": prefix,
        }

        # Write response file
        with open("spack-responses.txt", "w") as response_file:
            for key in responses:
                response_file.write("{0}: {1}\n".format(key, responses[key]))

    def install(self, spec, prefix):
        self.configure(prefix)

        installer = glob.glob("VizGlow*Install")[0]

        chmod = which("chmod")
        chmod("+x", installer)

        installer = Executable(installer)
        installer("--mode", "silent", "--response-file", "spack-responses.txt")

        self.filter_ld_library_path(spec, prefix)

    def filter_ld_library_path(self, spec, prefix):
        """Run after install to inject dependencies into LD_LIBRARY_PATH.

        If we don't do this, the run files will clear the LD_LIBRARY_PATH.
        Since the installer is a binary file, we have no means of specifying
        an RPATH to use."""

        files = glob.glob(prefix + "/binaries/*.run")

        ld_library_path = ":".join(
            [
                spec["zlib-api"].prefix.lib,
                spec["freetype"].prefix.lib,
                spec["fontconfig"].prefix.lib,
                spec["libxrender"].prefix.lib,
                spec["libcanberra"].prefix.lib,
            ]
        )

        for runfile in files:
            filter_file("(export LD_LIBRARY_PATH=)$", r"\1{0}".format(ld_library_path), runfile)
