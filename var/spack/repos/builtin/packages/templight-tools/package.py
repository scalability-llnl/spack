# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class TemplightTools(CMakePackage):
    """Supporting tools for the Templight Profiler"""

    homepage = "https://github.com/mikael-s-persson/templight-tools"
    git      = "https://github.com/mikael-s-persson/templight-tools.git"

    version('develop', branch='master')

    depends_on('cmake @2.8.7:', type='build')
    depends_on('boost @1.48.1: +filesystem +graph +program_options +test')
