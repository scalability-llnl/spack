# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
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

    version('2017r1', '06a8057d33a519607720d4c621cd3f50', expand=False)
    version('2018r2', 'd3cf54a7555e0259b7ba0d82fef23bc3', expand=False)

    def url_for_version(self, version):
        return "file://{0}/tecplot360ex{1}_linux64.sh".format(os.getcwd(), version)

    def install(self, spec, prefix):
        makefile = FileFilter(self.stage.archive_file)
        makefile.filter('interactive=TRUE', 'interactive=FALSE')
        makefile.filter('cpack_skip_license=FALSE', 'cpack_skip_license=TRUE')

        set_executable(self.stage.archive_file)
        installer = Executable(self.stage.archive_file)
        installer('--prefix=%s' % prefix)
