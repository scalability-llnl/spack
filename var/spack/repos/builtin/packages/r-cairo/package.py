# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RCairo(RPackage):
    """R graphics device using cairo graphics library for creating high-quality
    bitmap (PNG, JPEG, TIFF), vector (PDF, SVG, PostScript) and display (X11
    and Win32) output.

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

    cran = "Cairo"

    version("1.6-2", sha256="6b6f4c6f93178a1295860a9dc6dc45e60fec70f684d5c8d0b59baf5b8dd44d62")
    version("1.6-0", sha256="c762ac1d8daa4af527342360c256ed742de4e3031d997e9e59c9a369fcafb7d3")
    version("1.5-15", sha256="bb3ab1ff6431c15eb01a66ddf90695cd9a2af3d5a384753f5180cd0401d2e89d")
    version("1.5-14", sha256="067751face3b5771e72f9fb49bfeefb3a7bbecc060b672ab4393cb5935204c7b")
    version("1.5-12.2", sha256="dd524105c83b82b5c3b3ee2583ef90d4cafa54b0c29817dac48b425b79f90f92")
    version("1.5-10", sha256="7837f0c384cd49bb3342cb39a916d7a80b02fffbf123913a58014e597f69b5d5")
    version("1.5-9", sha256="2a867b6cae96671d6bc3acf9334d6615dc01f6ecf1953a27cde8a43c724a38f4")

    depends_on("r+X", type=("build", "run"))
    depends_on("r@2.4.0:", type=("build", "run"))
    # "The Cairo package requires cairo library 1.2.0 or higher with PNG support enabled"
    # See https://www.rforge.net/Cairo/
    depends_on("cairo@1.2: +png")
    # Disabled PDF support results in compilation failures in 1.6-1:1.6-2
    # See https://github.com/s-u/Cairo/pull/48
    depends_on("cairo +pdf", type=("build", "run"), when="@1.6-1:1.6-2")
    # When cairo +ft, must also have +fc, for cairo_ft_font_face_create_for_pattern test
    conflicts(
        "^cairo ~fc", when="^cairo +ft", msg="For cairo freetype support, also need fontconfig."
    )
    depends_on("libxt")
