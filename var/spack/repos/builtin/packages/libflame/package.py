# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class LibflameBase(AutotoolsPackage):
    """Base class for building Libflame, shared with the AMD
    optimized version of the library in the 'libflame' package"""

    provides("lapack", when="+lapack2flame")

    variant(
        "lapack2flame",
        default=True,
        description="Map legacy LAPACK routine invocations"
        " to their corresponding native C implementations"
        " in libflame.",
    )

    variant(
        "threads",
        default="none",
        description="Multithreading support",
        values=("pthreads", "openmp", "none"),
        multi=False,
    )

    variant("static", default=True, description="Build static library")

    variant("shared", default=True, description="Build shared library")

    variant("debug", default=False, description="Build with debugging support")

    # TODO: Libflame prefers to defer to an external
    # LAPACK library for small problems. Is this to be
    # implemented in spack?

    # Libflame has a secondary dependency on BLAS:
    # https://github.com/flame/libflame/issues/24
    depends_on("blas")

    # There is a known issue with the makefile:
    # https://groups.google.com/forum/#!topic/libflame-discuss/lQKEfjyudOY
    patch("Makefile_5.1.0.patch", when="@5.1.0")

    # Problems with permissions on installed libraries:
    # https://github.com/flame/libflame/issues/24
    patch("Makefile_5.2.0.patch", when="@5.2.0")

    # Problems building on macOS:
    # https://github.com/flame/libflame/issues/23
    patch("Makefile_5.2.0_darwin.patch", when="@5.2.0")

    def flag_handler(self, name, flags):
        # -std=gnu99 at least required, old versions of GCC default to -std=c90
        if self.spec.satisfies("%gcc@:5.1") and name == "cflags":
            flags.append("-std=gnu99")
        return (flags, None, None)

    def enable_or_disable_threads(self):
        opt_val = self.spec.variants["threads"].value
        if opt_val == "none":
            opt_val = "no"
        return ["--enable-multithreading={0}".format(opt_val)]

    def configure_args(self):
        # Libflame has a secondary dependency on BLAS,
        # but doesn't know which library name to expect:
        # https://github.com/flame/libflame/issues/24
        config_args = ["LIBS=" + self.spec["blas"].libs.ld_flags]

        if self.spec.satisfies("+lapack2flame"):
            config_args.append("--enable-lapack2flame")
        else:
            config_args.append("--disable-lapack2flame")

        if self.spec.satisfies("+static"):
            config_args.append("--enable-static-build")
        else:
            config_args.append("--disable-static-build")

        if self.spec.satisfies("+shared"):
            config_args.append("--enable-dynamic-build")
        else:
            config_args.append("--disable-dynamic-build")

        if self.spec.satisfies("+debug"):
            config_args.append("--enable-debug")
        else:
            config_args.append("--disable-debug")

        config_args.extend(self.enable_or_disable_threads())

        if self.spec.variants["threads"].value != "none":
            config_args.append("--enable-supermatrix")
        else:
            config_args.append("--disable-supermatrix")

        # https://github.com/flame/libflame/issues/21
        config_args.append("--enable-max-arg-list-hack")

        if self.spec.satisfies("^blis"):
            config_args.append("LDFLAGS=-L{}".format(self.spec["blis"].prefix.lib))

        return config_args

    @run_after("install")
    def darwin_fix(self):
        # The shared library is not installed correctly on Darwin; fix this
        if self.spec.satisfies("platform=darwin"):
            fix_darwin_install_name(self.prefix.lib)


class Libflame(LibflameBase):
    """libflame is a portable library for dense matrix computations,
    providing much of the functionality present in LAPACK, developed
    by current and former members of the Science of High-Performance
    Computing (SHPC) group in the Institute for Computational
    Engineering and Sciences at The University of Texas at Austin.
    libflame includes a compatibility layer, lapack2flame, which
    includes a complete LAPACK implementation."""

    homepage = "https://www.cs.utexas.edu/~flame/web/libFLAME.html"
    url = "https://github.com/flame/libflame/archive/5.1.0.tar.gz"
    git = "https://github.com/flame/libflame.git"

    license("BSD-3-Clause")

    version("master", branch="master")
    version("5.2.0", sha256="997c860f351a5c7aaed8deec00f502167599288fd0559c92d5bfd77d0b4d475c")
    version("5.1.0", sha256="e7189b750890bd781fe773f366b374518dd1d89a6513d3d6261bf549826384d1")

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    provides("flame@5.2", when="@5.2.0")
    provides("flame@5.1", when="@5.1.0")

    depends_on("python", type="build")
