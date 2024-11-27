# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import shutil
from glob import glob

from spack.package import *


class PhotosF(MakefilePackage):
    """PHOTOS Monte-Carlo generator (Fortran version)"""

    homepage = "https://wasm.web.cern.ch/wasm/f77.html"
    url = (
        "http://cern.ch/service-spi/external/MCGenerators/distribution/photos/photos-215.5-src.tgz"
    )

    version("215.5", sha256="3e2b3f60ffe2d3a6a95cf2f156aa24b93e1fa3c439a85fa0ae780ca2f6e0dbb5")

    depends_on("fortran", type="build")  # generated

    patch("photos-215.5-update-configure.patch", level=2)

    def do_stage(self, mirror_only=False):
        # Fix directory structure - remove extra "<version>" subdirectory
        super().do_stage(mirror_only)
        root = join_path(self.stage.source_path, self.spec.version)
        for fn in os.listdir(root):
            shutil.move(join_path(root, fn), self.stage.source_path)
        shutil.rmtree(root)

    def edit(self, spec, prefix):
        configure_ = Executable("./configure")
        configure_("--enable-static", "--disable-shared")
        if self.spec.satisfies("platform=darwin"):
            filter_file("libphotos.so", "libphotos.dylib", "Makefile")

    def install(self, spec, prefix):
        install_tree("lib", prefix.lib)
        install_tree("include", prefix.include)
        for fn in glob(join_path(prefix.lib.archive, "*.a")):
            install(fn, prefix.lib)
        shutil.rmtree(prefix.lib.archive)
