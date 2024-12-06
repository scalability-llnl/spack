# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

import llnl.util.tty as tty

from spack.package import *
from spack.util.environment import EnvironmentModifications


class Heasoft(AutotoolsPackage):
    """A Unified Release of the FTOOLS and XANADU Software Packages.

    XANADU: High-level, multi-mission tasks for X-ray astronomical spectral,
    timing, and imaging data analysis. FTOOLS: General and mission-specific
    tools to manipulate FITS files. FITSIO: Core library responsible for reading
    and writing FITS files. fv: General FITS file browser/editor/plotter with a
    graphical user interface. XSTAR: Tool for calculating the physical
    conditions and emission spectra of photoionized gases"""

    homepage = "https://heasarc.gsfc.nasa.gov/docs/software/lheasoft/"
    url = "https://heasarc.gsfc.nasa.gov/FTP/software/lheasoft/lheasoft6.29/heasoft-6.29src.tar.gz"

    license("BSD-3-Clause")

    version("6.30", sha256="7f828f6050809653319f94d715c1b6815fbc09adfdcb61f2f0f1d7a6af10684a")
    version("6.29", sha256="534fec04baa2586326fd7240805f2606620f3b7d7078a80fdd95c9c1177c9e68")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("X", default=True, description="Enable X11 support")

    depends_on("zlib-api")
    depends_on("ncurses")
    depends_on("curl")
    depends_on("libxt", when="+X")
    depends_on("libx11", when="+X")
    depends_on("readline")
    depends_on("libpng")
    depends_on("perl-extutils-makemaker")
    depends_on("py-numpy")

    extends("python")

    conflicts("%gcc@:4,10:")

    # Do not create directory in $HOME during environment sourcing and use a
    # predictable name for the file to be sourced.
    patch("setup.patch")

    # tcltk-configure: Remove redundant X11 header test because spack has X11
    # headers in different directories
    #
    # xspec: The HEASOFT project provides a tarball of replacement files for
    # Xspec, along with a Tcl patch utility. This is meant for updating a
    # source tree in place with minimal rebuilding. This does not fit Spack's
    # model so convert those to patches. These are kept in sync with what is on
    # https://heasarc.gsfc.nasa.gov/docs/software/lheasoft/xanadu/xspec/issues/issues.html
    with when("@6.29"):
        patch("heasoft-6.29_tcltk-configure.patch")

        patch("heasoft-6.29_xspec-12.12.0a.patch")
        patch("heasoft-6.29_xspec-12.12.0b.patch")
        patch("heasoft-6.29_xspec-12.12.0c.patch")
        patch("heasoft-6.29_xspec-12.12.0d.patch")
        patch("heasoft-6.29_xspec-12.12.0e.patch")
        patch("heasoft-6.29_xspec-12.12.0f.patch")
        patch("heasoft-6.29_xspec-12.12.0g.patch")
        patch("heasoft-6.29_xspec-12.12.0ver.patch")

    with when("@6.30"):
        patch("heasoft-6.30_tcltk-configure.patch")

    configure_directory = "BUILD_DIR"

    parallel = False

    def patch(self):
        filter_file(
            r"(--with-readline-library=)\\\$READLINE_DIR",
            r"\1{0}".format(self.spec["readline"].libs.directories[0]),
            join_path("tcltk", "BUILD_DIR", "hd_config_info"),
        )

        filter_file(
            r"(--with-readline-includes=)\\\$READLINE_DIR",
            r"\1{0}".format(join_path(self.spec["readline"].headers.directories[0], "readline")),
            join_path("tcltk", "BUILD_DIR", "hd_config_info"),
        )

        if self.spec.satisfies("+X"):
            filter_file(
                r"(\s+XDIR => ).*",
                r"\1'{0}',".format(self.spec["libx11"].libs.directories[0]),
                join_path("tcltk", "PGPLOT-perl", "Makefile.PL"),
            )

    def configure_args(self):
        config_args = [
            "--with-png={0}".format(self.spec["libpng"].prefix),
            "CPPFLAGS={0}".format(self.spec["zlib-api"].headers.include_flags),
            "LDFLAGS={0}".format(self.spec["zlib-api"].libs.search_flags),
        ]

        config_args += self.enable_or_disable("x", variant="X")

        if self.spec.satisfies("+X"):
            config_args.extend(
                [
                    "--x-includes={0}".format(self.spec["libx11"].headers.directories[0]),
                    "--x-libraries={0}".format(self.spec["libx11"].libs.directories[0]),
                ]
            )

        return config_args

    @run_after("install")
    def generate_environment(self):
        host_family = self.spec.target.family
        host_platform = self.spec.platform
        host_libc = os.confstr("CS_GNU_LIBC_VERSION").split()[1]
        target = "{0}-pc-{1}-gnu-libc{2}".format(host_family, host_platform, host_libc)
        headas_setup_file = join_path(self.spec.prefix, target, "BUILD_DIR", "headas-setup")

        filter_file(
            r"(^headas_config=).*",
            r"\1{0}".format(join_path(self.prefix, "headas-config_spack")),
            headas_setup_file,
        )

        filter_file(
            r"(^flavor.*\n)",
            r"\1HEADAS={0}".format(join_path(self.spec.prefix, target)) + "\n",
            headas_setup_file,
        )

        headas_setup = Executable(headas_setup_file)
        headas_setup("sh")

    def setup_run_environment(self, env):
        try:
            env.extend(
                EnvironmentModifications.from_sourcing_file(
                    join_path(self.spec.prefix, "headas-config_spack.sh"), clean=True
                )
            )
        except Exception as e:
            msg = "unexpected error when sourcing HEASOFT setup [{0}]"
            tty.warn(msg.format(str(e)))
