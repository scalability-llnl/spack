# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Changa(AutotoolsPackage):
    """ChaNGa (Charm N-body GrAvity solver) is a code to perform collisionless
    N-body simulations. It can perform cosmological simulations with periodic
    boundary conditions in comoving coordinates or simulations of isolated
    stellar systems. It also can include hydrodynamics using the Smooth
    Particle Hydrodynamics (SPH) technique. It uses a Barnes-Hut tree to
    calculate gravity, with hexadecapole expansion of nodes and
    Ewald summation for periodic forces. Timestepping is done with a leapfrog
    integrator with individual timesteps for each particle."""

    homepage = "http://faculty.washington.edu/trq/hpcc/tools/changa.html"
    url      = "https://github.com/N-BodyShop/changa/archive/v3.4.tar.gz"
    git      = "https://github.com/N-BodyShop/changa.git"

    version('master', branch='master')
    version('3.4', sha256='c2bceb6ac00025dfd704bb6960bc17c6df7c746872185845d1e75f47e6ce2a94')
    patch("fix_configure_path.patch")

    resource(
        name="utility",
        url="https://github.com/N-BodyShop/utility/archive/v3.4.tar.gz",
        sha256="19f9f09023ce9d642e848a36948788fb29cd7deb8e9346cdaac4c945f1416667",
        placement="utility"
    )

    depends_on("charmpp build-target=ChaNGa")

    def configure_args(self):
        args = []
        args.append("STRUCT_DIR={0}/utility/structures"
                    .format(self.stage.source_path))
        return args

    def install(self, spec, prefix):
        with working_dir(self.build_directory):
            mkdirp(prefix.bin)
            install('ChaNGa', prefix.bin)
            install('charmrun', prefix.bin)
