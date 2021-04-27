# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RCairo(RPackage):
    """R graphics device using cairo graphics library for creating high-quality
    bitmap (PNG, JPEG, TIFF), vector (PDF, SVG, PostScript) and display (X11
    and Win32) output

    R graphics device using cairographics library that can be used to create
    high-quality vector (PDF, PostScript and SVG) and bitmap output
    (PNG,JPEG,TIFF), and high-quality rendering in displays (X11 and Win32).
    Since it uses the same back-end for all output, copying across formats is
    WYSIWYG. Files are created without the dependence on X11 or other external
    programs. This device supports alpha channel (semi-transparent drawing) and
    resulting images can contain transparent and semi-transparent regions. It
    is ideal for use in server environments (file output) and as a replacement
    for other devices that don't have Cairo's capabilities such as alpha
    support or anti-aliasing. Backends are modular such that any subset of
    backends is supported."""

    homepage = "https://cloud.r-project.org/package=Cairo"
    url      = "https://cloud.r-project.org/src/contrib/Cairo_1.5-9.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/Cairo"

    version('1.5-12.2', sha256='dd524105c83b82b5c3b3ee2583ef90d4cafa54b0c29817dac48b425b79f90f92')
    version('1.5-10', sha256='7837f0c384cd49bb3342cb39a916d7a80b02fffbf123913a58014e597f69b5d5')
    version('1.5-9', sha256='2a867b6cae96671d6bc3acf9334d6615dc01f6ecf1953a27cde8a43c724a38f4')

    depends_on('r@2.4.0:', type=('build', 'run'))
    depends_on('cairo@1.2:')
