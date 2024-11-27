# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Madis(MakefilePackage):
    """
    Meteorological Assimilation Data Ingest System (MADIS) is an observational
    database and delivery system which integrates real-time observations from a
    wide variety of observing infrastructures to make them useable for
    numerical weather prediction models and nowcasting.
    """

    homepage = "https://madis-data.ncep.noaa.gov/"
    url = "https://madis-data.ncep.noaa.gov/source/madis-4.3.tar.gz"

    maintainers("AlexanderRichert-NOAA")

    version("4.3", sha256="5d1ee9800c84e623dcf4271653aa66d17a744143e58354e70f8a0646cd6b246c")

    depends_on("fortran", type="build")  # generated

    variant("pic", default=True, description="Build with position-independent code (PIC)")
    variant("pnetcdf", default=False, description="Build with parallel NetCDF")

    depends_on("netcdf-fortran")
    depends_on("parallel-netcdf", when="+pnetcdf")

    def setup_build_environment(self, env):
        fflags = []
        if self.spec.satisfies("%gcc@10:"):
            fflags += ["-fallow-argument-mismatch"]

        if self.spec.satisfies("+pic"):
            fflags += ["-fPIC"]

        env.set("FFLAGS", " ".join(fflags))

        ldflags = []
        libs = []

        if self.spec.satisfies("+pnetcdf"):
            pnetcdf = self.spec["parallel-netcdf"]
            ldflags.append(pnetcdf.libs.ld_flags)
            libs.append(pnetcdf.libs.link_flags)

        nfconfig = which(os.path.join(self.spec["netcdf-fortran"].prefix.bin, "nf-config"))
        ldflags.append(nfconfig("--flibs", output=str).strip())
        netcdf_f = self.spec["netcdf-fortran"]
        env.set("NETCDF_INC", netcdf_f.prefix.include)

        env.set("NETCDF_LIB", " ".join(ldflags))
        env.set("LIBS", " ".join(libs))

    def build(self, spec, prefix):
        with working_dir("src"):
            make("-j1")

    def install(self, spec, prefix):
        with working_dir("src"):
            make("-j1")
        with working_dir(self.build_directory):
            copy_tree("bin", prefix.bin)
            copy_tree("doc", prefix.doc)
            copy_tree("include", prefix.include)
            copy_tree("lib", prefix.lib)
            copy_tree("src", prefix.src)
            copy_tree("static", prefix.static)

    def patch(self):
        for pattern in ["NETCDF_LIB", "NETCDF_INC", "FC", "FFLAGS", "LDFLAGS"]:
            filter_file(pattern + "=", "#" + pattern + "=", "src/makefile")
