# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.pkg.builtin.boost import Boost


class Ibmisc(CMakePackage):
    """Misc. reusable utilities used by IceBin."""

    homepage = "https://github.com/citibeth/ibmisc"
    url = "https://github.com/citibeth/ibmisc/archive/v0.1.0.tar.gz"

    maintainers("citibeth")

    license("LGPL-3.0-only")

    version("0.1.0", sha256="38481a8680aad4b40eca6723b2898b344cf0ef891ebc3581f5e99fbe420fa0d8")

    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("everytrace", default=False, description="Report errors through Everytrace")
    variant("proj", default=True, description="Compile utilities for PROJ.4 library")
    variant("blitz", default=True, description="Compile utilities for Blitz library")
    variant("netcdf", default=True, description="Compile utilities for NetCDF library")
    variant("boost", default=True, description="Compile utilities for Boost library")
    variant("udunits2", default=True, description="Compile utilities for UDUNITS2 library")
    variant("googletest", default=True, description="Compile utilities for Google Test library")
    variant("python", default=True, description="Compile utilities for use with Python/Cython")

    extends("python")

    depends_on("eigen")
    depends_on("everytrace", when="+everytrace")
    depends_on("proj@:4", when="+proj")
    depends_on("blitz", when="+blitz")
    depends_on("netcdf-cxx4", when="+netcdf")
    depends_on("udunits", when="+udunits2")
    depends_on("googletest", when="+googletest", type="build")
    depends_on("py-cython", when="+python", type=("build", "run"))
    depends_on("py-numpy", when="+python", type=("build", "run"))
    depends_on("boost", when="+boost")

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants, when="+boost")

    # Build dependencies
    depends_on("doxygen", type="build")

    def cmake_args(self):
        return [
            self.define_from_variant("USE_EVERYTRACE", "everytrace"),
            self.define_from_variant("USE_PROJ4", "proj"),
            self.define_from_variant("USE_BLITZ", "blitz"),
            self.define_from_variant("USE_NETCDF", "netcdf"),
            self.define_from_variant("USE_BOOST", "boost"),
            self.define_from_variant("USE_UDUNITS2", "udunits2"),
            self.define_from_variant("USE_GTEST", "googletest"),
        ]
