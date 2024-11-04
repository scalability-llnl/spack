# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Wxpropgrid(Package, SourceforgePackage):
    """wxPropertyGrid is a property sheet control for wxWidgets. In
    other words, it is a specialized two-column grid for editing
    properties such as strings, numbers, flagsets, string arrays,
    and colours."""

    homepage = "https://wxpropgrid.sourceforge.net/"
    sourceforge_mirror_path = "wxpropgrid/wxpropgrid-1.4.15-src.tar.gz"

    version("1.4.15", sha256="f0c9a86656828f592c8e57d2c89401f07f0af6a45b17bbca3990e8d29121c2b8")

    depends_on("cxx", type="build")  # generated

    depends_on("wxwidgets")

    def install(self, spec, prefix):
        configure(
            "--prefix=%s" % prefix,
            "--with-wxdir=%s" % spec["wxwidgets"].prefix.bin,
            "--enable-unicode",
        )

        make()
        make("install")
