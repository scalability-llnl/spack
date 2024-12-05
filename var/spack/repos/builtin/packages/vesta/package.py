# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Vesta(Package):
    """VESTA is a 3D visualization program for structural models, volumetric data
    such as electron/nuclear densities, and crystal morphologies."""

    homepage = "https://jp-minerals.org/vesta"
    url = "https://jp-minerals.org/vesta/archives/3.4.6/VESTA-x86_64.tar.bz2"

    version("3.4.6", sha256="fb00ac9a7bf46a3d9a1d745859c5e8757ba30f017a46470eb2c123b9afcf66ee")

    depends_on("gtkplus@2.1.0:")
    depends_on("mesa")
    depends_on("cairo@1.0:")

    conflicts("%gcc@:5.3")

    def setup_run_environment(self, env):
        env.prepend_path("PATH", self.prefix)
        env.prepend_path("LD_LIBRARY_PATH", self.prefix)

    def install(self, spec, prefix):
        install_tree(".", prefix)
