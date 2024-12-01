# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Mkfontdir(AutotoolsPackage, XorgPackage):
    """mkfontdir creates the fonts.dir files needed by the legacy X server
    core font system.   The current implementation is a simple wrapper script
    around the mkfontscale program, which must be built and installed first."""

    homepage = "https://cgit.freedesktop.org/xorg/app/mkfontdir"
    xorg_mirror_path = "app/mkfontdir-1.0.7.tar.gz"

    version("1.0.7", sha256="bccc5fb7af1b614eabe4a22766758c87bfc36d66191d08c19d2fa97674b7b5b7")

    depends_on("mkfontscale", type="run")

    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
