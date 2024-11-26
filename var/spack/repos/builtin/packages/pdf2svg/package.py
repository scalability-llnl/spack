# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Pdf2svg(AutotoolsPackage):
    """A simple PDF to SVG converter using the Poppler and Cairo libraries."""

    homepage = "http://www.cityinthesky.co.uk/opensource/pdf2svg"
    url = "https://github.com/dawbarton/pdf2svg/archive/v0.2.3.tar.gz"

    license("GPL-2.0-only")

    version("0.2.3", sha256="4fb186070b3e7d33a51821e3307dce57300a062570d028feccd4e628d50dea8a")
    version("0.2.2", sha256="e5f1d9b78821e44cd85379fb07f38a42f00bb2bde3743b95301ff8c0a5ae229a")

    depends_on("c", type="build")  # generated

    depends_on("pkgconfig@0.9.0:", type="build")
    depends_on("cairo@1.2.6:")
    depends_on("poppler@0.5.4:+glib")

    # Note: the latest version of poppler requires glib 2.41+,
    # but pdf2svg uses g_type_init, which is deprecated in glib 2.36+.
    # At some point, we will need to force pdf2svg to use older
    # versions of poppler and glib.
