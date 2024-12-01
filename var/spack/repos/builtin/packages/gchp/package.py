# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import shutil

from spack.package import *


class Gchp(CMakePackage):
    """GEOS-Chem High Performance model of atmospheric chemistry"""

    homepage = "https://gchp.readthedocs.io/"
    url = "https://github.com/geoschem/GCHP/archive/13.4.0.tar.gz"
    git = "https://github.com/geoschem/GCHP.git"
    maintainers("lizziel", "laestrada")

    license("MIT")

    version("13.4.0", commit="d8c6d4d8db1c5b0ba54d4893185d999a619afc58", submodules=True)
    version("13.3.4", commit="efb2346381648ffff04ce441d5d61d7fec0c53fe", submodules=True)
    version("13.2.1", commit="9dc2340cac684971fa961559a4dc3d8818326ab8", submodules=True)
    version("13.1.2", commit="106b8f783cafabd699e53beec3a4dd8aee45234b", submodules=True)
    version("13.1.1", commit="a17361a78aceab947ca51aa1ecd3391beaa3fcb2", submodules=True)
    version("13.1.0", commit="4aca45370738e48623e61e38b26d981d3e20be76", submodules=True)
    version("13.0.2", commit="017ad7276a801ab7b3d6945ad24602eb9927cf01", submodules=True)
    version("13.0.1", commit="f40a2476fda901eacf78c0972fdb6c20e5a06700", submodules=True)
    version("13.0.0", commit="1f5a5c5630c5d066ff8306cbb8b83e267ca7c265", submodules=True)
    version("dev", branch="dev", submodules=True)

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    patch("for_aarch64.patch", when="target=aarch64:")

    depends_on("esmf@8.0.1", when="@13.0.0:")
    depends_on("mpi@3")
    depends_on("netcdf-fortran")
    depends_on("cmake@3.13:")
    depends_on("libfabric", when="+ofi")
    depends_on("m4")

    variant("omp", default=False, description="OpenMP parallelization")
    variant("real8", default=True, description="REAL*8 precision")
    variant("apm", default=False, description="APM Microphysics (Experimental)")
    variant("rrtmg", default=False, description="RRTMG radiative transfer model")
    variant("luo", default=False, description="Luo et al 2019 wet deposition scheme")
    variant("tomas", default=False, description="TOMAS Microphysics (Experimental)")
    variant("ofi", default=False, description="Build with Libfabric support")

    def cmake_args(self):
        args = [
            self.define("RUNDIR", self.prefix),
            self.define_from_variant("OMP", "omp"),
            self.define_from_variant("USE_REAL8", "real8"),
            self.define_from_variant("APM", "apm"),
            self.define_from_variant("RRTMG", "rrtmg"),
            self.define_from_variant("LUO_WETDEP", "luo"),
            self.define_from_variant("TOMAS", "tomas"),
        ]
        return args

    def install(self, spec, prefix):
        super().install(spec, prefix)
        # Preserve source code in prefix for two reasons:
        # 1. Run directory creation occurs independently of code compilation,
        # possibly multiple times depending on user needs,
        # and requires the preservation of some of the source code structure.
        # 2. Run configuration is relatively complex and can result in error
        # messages that point to specific modules / lines of the source code.
        # Including source code thus facilitates runtime debugging.
        shutil.move(self.stage.source_path, join_path(prefix, "source_code"))
