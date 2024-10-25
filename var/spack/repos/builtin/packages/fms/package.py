# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Fms(CMakePackage):
    """GFDL's Flexible Modeling System (FMS) is a software environment
    that supports the efficient development, construction, execution,
    and scientific interpretation of atmospheric, oceanic, and climate
    system models."""

    homepage = "https://github.com/NOAA-GFDL/FMS"
    url = "https://github.com/NOAA-GFDL/FMS/archive/refs/tags/2022.04.tar.gz"
    git = "https://github.com/NOAA-GFDL/FMS.git"

    license("LGPL-3.0-or-later")

    maintainers("AlexanderRichert-NOAA", "Hang-Lei-NOAA", "edwardhartnett", "rem1776", "climbfuji")
    version("2024.02", sha256="47e5740bb066f5eb032e1de163eb762c7258880a2932f4cc4e34e769e0cc2b0e")
    version(
        "2024.01.01", sha256="41c8686bad2b1aed76275e35cbe1af855f7dfce9b6d8907744ea2e8174758f6a"
    )
    version("2024.01", sha256="29ac23a5a2a4765ae66d218bb261cb04f7ad44618205ab0924c4e66c9ef8fa38")
    version("2023.04", sha256="feb895ea2b3269ca66df296199a36af335f0dc281e2dab2f1bfebb19fd9c22c4")
    version("2023.03", sha256="008a9ff394efe6a8adbcf37dd45ca103e00ae25748fc2960b7bc54f2f3b08d85")
    version(
        "2023.02.01", sha256="1597f7a485d02e401ce76444b2401060d74bd032cbb060cef917f001b4ff14bc"
    )
    version("2023.02", sha256="dc029ffadfd82c334f104268bedd8635c77976485f202f0966ae4cf06d2374be")
    version(
        "2023.01.01", sha256="f83e2814a1e3ba439ab847ec8bb251f3889d5ca14fb20849507590adbbe8e899"
    )
    version("2023.01", sha256="6079ea885e9365513b453c77aadfc7c305bf413b840656bb333db1eabba0f18e")
    version("2022.04", sha256="f741479128afc2b93ca8291a4c5bcdb024a8cbeda1a26bf77a236c0f629e1b03")
    version("2022.03", sha256="42d2ac53d3c889a8177a6d7a132583364c0f6e5d5cbde0d980443b6797ad4838")
    version("2022.02", sha256="ad4978302b219e11b883b2f52519e1ee455137ad947474abb316c8654f72c874")
    version("2022.01", sha256="a1cba1f536923f5953c28729a28e5431e127b45d6bc2c15d230939f0c02daa9b")
    version("2021.04", sha256="dcb4fe80cb3b7846f7cf89b812afff09a78a10261ea048a851f28935d6b241b1")
    version(
        "2021.03.01", sha256="1f70e2a57f0d01e80fceb9ca9ce9661f5c1565d0437ab67618c2c4dfea0da6e9"
    )
    version("2021.03", sha256="a9fb6e85f44ff79e6f9e61e65f42a5ffd38fa661fe1a3e4da6f85ffacd2697ac")
    version(
        "2021.02.01", sha256="9b11d9474d7c90464af66d81fb86c4798cfa309b9a0da20b0fccf33c4f65386b"
    )
    version("2021.02", sha256="db810b2452a6952239f064b52c0c5c58fc62126057982111b9fcd64f1b3bd879")
    version("2021.01", sha256="38c748e2edb94ffeb021095d8bde4d74b7834610ce0ef1dbb4dce353eeb5cd96")
    version(
        "2020.04.02", sha256="bd6ce752b1018d4418398f14b9fc486f217de76bcbaaf2cdbf4c43e0b3f39f69"
    )
    version(
        "2020.04.01", sha256="2c409242de7dea0cf29f8dbf7495698b6bcac1eeb5c4599a728bdea172ffe37c"
    )

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    # https://github.com/NOAA-GFDL/FMS/issues/1417
    patch(
        "https://github.com/NOAA-GFDL/FMS/commit/c9bba516ba1115d4a7660fba92f9d67cf3fd32ad.patch?full_index=1",
        sha256="07d5b68838bba61ee547bd4cd7c12d81228c91a80a966b8693694fa236d0ac30",
        when="@2023.03",
    )

    variant("shared", description="Build shared libraries", when="@2024.02:", default=False)
    # What the following patch is providing is available in version 2024.03
    # and newer so it is only needed to 2024.02
    patch(
        "https://github.com/NOAA-GFDL/fms/pull/1559.patch?full_index=1",
        sha256="2b12a6c35f357c3dddcfa5282576e56ab0e8e6c1ad1dab92a2c85ce3dfb815d4",
        when="@2024.02",
    )

    variant(
        "precision",
        values=("32", "64"),
        description="Build a version of the library with default 32 or 64 bit reals or both",
        default="32",
        multi=True,
    )
    conflicts(
        "precision=32,64",
        when="@:2022.03",
        msg="FMS versions prior to 2022.04 do not support both 32 and 64 bit precision",
    )

    variant("gfs_phys", default=True, description="Use GFS Physics")
    variant("openmp", default=True, description="Use OpenMP")
    variant("quad_precision", default=True, description="quad precision reals")
    variant(
        "yaml",
        default=False,
        description="yaml input file support(requires libyaml)",
        when="@2021.04:",
    )
    variant(
        "constants",
        default="GFDL",
        description="Build with <X> constants parameter definitions",
        values=("GFDL", "GEOS", "GFS"),
        multi=False,
        when="@2022.02:",
    )
    variant(
        "pic", default=False, description="Build with position independent code", when="@2022.02:"
    )
    variant(
        "deprecated_io",
        default=False,
        description="Compiles with support for deprecated io modules fms_io and mpp_io",
        when="@2023.02:",
    )
    variant("large_file", default=False, description="Enable compiler definition -Duse_LARGEFILE.")
    variant(
        "internal_file_nml",
        default=True,
        description="Enable compiler definition -DINTERNAL_FILE_NML.",
    )

    depends_on("netcdf-c")
    depends_on("netcdf-fortran")
    depends_on("mpi")
    depends_on("libyaml", when="+yaml")
    depends_on("llvm-openmp", when="+openmp %apple-clang", type=("build", "run"))

    def cmake_args(self):
        args = [
            self.define_from_variant("GFS_PHYS"),
            self.define_from_variant("OPENMP"),
            self.define_from_variant("ENABLE_QUAD_PRECISION", "quad_precision"),
            self.define_from_variant("SHARED_LIBS", "shared"),
            self.define_from_variant("WITH_YAML", "yaml"),
            self.define_from_variant("CONSTANTS"),
            self.define_from_variant("LARGEFILE", "large_file"),
            self.define_from_variant("INTERNAL_FILE_NML"),
            self.define("32BIT", "precision=32" in self.spec),
            self.define("64BIT", "precision=64" in self.spec),
            self.define_from_variant("FPIC", "pic"),
            self.define_from_variant("USE_DEPRECATED_IO", "deprecated_io"),
        ]

        return args
