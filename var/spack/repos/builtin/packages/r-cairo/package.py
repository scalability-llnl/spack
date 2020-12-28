# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RCairo(RPackage):
    """R graphics device using cairo graphics library for creating high-quality
       bitmap (PNG, JPEG, TIFF), vector (PDF, SVG, PostScript) and display
       (X11 and Win32) output"""

    homepage = "https://cloud.r-project.org/package=Cairo"
    url      = "https://cloud.r-project.org/src/contrib/Cairo_1.5-9.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/Cairo"

    version('1.5-10', sha256='7837f0c384cd49bb3342cb39a916d7a80b02fffbf123913a58014e597f69b5d5')
    version('1.5-9', sha256='2a867b6cae96671d6bc3acf9334d6615dc01f6ecf1953a27cde8a43c724a38f4')

    depends_on('r@2.4.0:', type=('build', 'run'))
    depends_on('cairo@1.2:')
