# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Tecplot(Package):
    """Tecplot 360 is a Computational Fluid Dynamics (CFD) and numerical
    simulation software package used in post-processing simulation results.
    It is also used in chemistry applications to visualize molecule structure
    by post-processing charge density data."""

    homepage = "https://www.tecplot.com/"
    manual_download = True

    maintainers("LRWeber")

    version(
        "2024r1",
        sha256="709022a5d5532d46a47cfa3bf0698a4ea8428c7a0dea2feb708a5add8091a8f0",
        expand=False,
    )
    version(
        "2023r1",
        sha256="58e7f4de875e65047f4edd684013d0ff538df6246f00c059458989f281be4c93",
        expand=False,
    )
    version(
        "2022r2",
        sha256="e30cb7bf894e7cd568a2b24beb4bf667f1781ae27b59bb73410fafe12ddfdcdf",
        expand=False,
    )
    # Deprecated versions
    version("2018r2", md5="d3cf54a7555e0259b7ba0d82fef23bc3", expand=False, deprecated=True)
    version("2017r1", md5="06a8057d33a519607720d4c621cd3f50", expand=False, deprecated=True)

    # Licensing
    license_required = True
    license_comment = "#"
    license_files = ["tecplotlm.lic"]

    def url_for_version(self, version):
        return "file://{0}/tecplot360ex{1}_linux64.sh".format(os.getcwd(), version)

    def install(self, spec, prefix):
        set_executable(self.stage.archive_file)
        installer = Executable(self.stage.archive_file)
        installer("--skip-license", "--prefix=%s" % prefix)
        # Link individual products to top level license file
        lic360 = "360ex_{0}/tecplotlm.lic".format(self.version)
        licChorus = "chorus_{0}/tecplotlm.lic".format(self.version)
        force_symlink("../tecplotlm.lic", join_path(self.prefix, lic360))
        force_symlink("../tecplotlm.lic", join_path(self.prefix, licChorus))

    def setup_run_environment(self, env):
        # Add Chorus bin
        binChorus = "chorus_{0}/bin".format(self.version)
        env.prepend_path("PATH", join_path(self.prefix, binChorus))
        # Add Tecplot 360 bin
        bin360 = "360ex_{0}/bin".format(self.version)
        env.prepend_path("PATH", join_path(self.prefix, bin360))
        # Add Tecplot 360 lib
        lib360 = "360ex_{0}/lib".format(self.version)
        env.prepend_path("LD_LIBRARY_PATH", join_path(self.prefix, lib360))
