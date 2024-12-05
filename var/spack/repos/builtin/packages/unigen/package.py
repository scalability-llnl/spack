# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Unigen(MakefilePackage):
    """The United Generators project was launched by the Virtual Institute 146
    VI-SIM in September 2005 following a proposal of Herbert Strobele.
    The goal was to facilitate comparison between various models (see below)
    and/or various experiments (HADES, FOPI, CERES, NA49, CBM). The package
    at present allows to convert output of various event generators to a
    generic root format."""

    homepage = "https://www.gsi.de/work/wissenschaftliche_netzwerke/helmholtz_virtuelle_institute/unigen.htm"
    url = "https://github.com/FairRootGroup/UniGen/archive/v2.3.tar.gz"

    tags = ["hep"]

    license("GPL-3.0-only")

    version("2.3", sha256="8783bcabbdf8c50dab6e93153cff9cfb267a9a9e61aef51bf1e17679ba42a717")

    depends_on("cxx", type="build")  # generated
    patch("unigen-2.3.patch", level=0)

    depends_on("root", type=("build", "link"))

    def build(self, spec, prefix):
        mkdirp(join_path(self.build_directory, "lib"))
        make("TOPDIR=" + self.build_directory, "all")

    def install(self, spec, prefix):
        make("DESTDIR=" + prefix, "TOPDIR=" + self.build_directory, "install")
