# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Ncvis(CMakePackage):
    """A NetCDF file viewer. ncvis is inspired by David Pierce's
    most excellent ncview utility."""

    homepage = "https://github.com/SEATStandards/ncvis"
    url = "https://github.com/SEATStandards/ncvis/archive/refs/tags/2022.08.28.tar.gz"
    git = "https://github.com/SEATStandards/ncvis.git"

    maintainers("vanderwb")

    version(
        "2022.08.28", sha256="a522926739b2a05ef0b436fe67a2014557f9e5fecf3b7d7700964e9006a4bf3e"
    )

    depends_on("cxx", type="build")  # generated

    depends_on("cmake", type="build")
    depends_on("netcdf-c", type="link")
    depends_on("wxwidgets+opengl", type="link")

    @run_after("install")
    def install_resources(self):
        install_tree("resources", self.prefix.resources)

    def setup_run_environment(self, env):
        env.set("NCVIS_RESOURCE_DIR", self.prefix.resources)
