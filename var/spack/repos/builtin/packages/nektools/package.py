# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import numbers
import os

from spack.package import *


def is_integral(x):
    """Any integer value"""
    try:
        return isinstance(int(x), numbers.Integral) and not isinstance(x, bool) and int(x) > 0
    except ValueError:
        return False


class Nektools(Package):
    """Tools required by Nek5000"""

    homepage = "https://nek5000.mcs.anl.gov/"
    url = "https://github.com/Nek5000/Nek5000/archive/v17.0.tar.gz"
    git = "https://github.com/Nek5000/Nek5000.git"

    tags = [
        "cfd",
        "flow",
        "hpc",
        "solver",
        "navier-stokes",
        "spectral-elements",
        "fluid",
        "ecp",
        "ecp-apps",
    ]

    version("develop", branch="master")
    version("19.0", sha256="db129877a10ff568d49edc77cf65f9e732eecb1fce10edbd91ffc5ac10c41ad6")
    version("17.0", sha256="4d8d4793ce3c926c54e09a5a5968fa959fe0ba46bd2e6b8043e099528ee35a60")

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    # Variant for MAXNEL, we need to read this from user
    variant(
        "MAXNEL",
        default=150000,
        description="Maximum number of elements for Nek5000 tools.",
        values=is_integral,
    )

    # Variants for Nek tools
    variant("genbox", default=True, description="Build genbox tool.")
    variant("n2to3", default=True, description="Build n2to3 tool.")
    variant("postnek", default=True, description="Build postnek tool.")
    variant("reatore2", default=True, description="Build reatore2 tool.")
    variant("genmap", default=True, description="Build genmap tool.")
    variant("nekmerge", default=True, description="Build nekmerge tool.")
    variant("prenek", default=True, description="Build prenek tool.")
    variant("visit", default=False, description="Enable support for visit")

    depends_on("libx11", when="+prenek")
    depends_on("libx11", when="+postnek")
    # libxt is needed for X11/Intrinsic.h but not for linking
    depends_on("libxt", when="+prenek")
    depends_on("xproto", when="+prenek")
    depends_on("libxt", when="+postnek")
    depends_on("visit", when="+visit")

    @run_before("install")
    def fortran_check(self):
        if not self.compiler.f77:
            msg = "Cannot build Nek5000 without a Fortran 77 compiler."
            raise RuntimeError(msg)

    def install(self, spec, prefix):
        tools_dir = "tools"
        bin_dir = "bin"

        fc = env["FC"]
        cc = env["CC"]

        fflags = spec.compiler_flags["fflags"]
        cflags = spec.compiler_flags["cflags"]
        if ("+prenek" in spec) or ("+postnek" in spec):
            libx11_h = find_headers("Xlib", spec["libx11"].prefix.include, recursive=True)
            if not libx11_h:
                raise RuntimeError("Xlib.h not found in %s" % spec["libx11"].prefix.include)
            cflags += ["-I%s" % os.path.dirname(libx11_h.directories[0])]

            xproto_h = find_headers("X", spec["xproto"].prefix.include, recursive=True)
            if not xproto_h:
                raise RuntimeError("X.h not found in %s" % spec["xproto"].prefix.include)
            cflags += ["-I%s" % os.path.dirname(xproto_h.directories[0])]

            libxt_h = find_headers("Intrinsic", spec["libxt"].prefix.include, recursive=True)
            if not libxt_h:
                raise RuntimeError(
                    "X11/Intrinsic.h not found in %s" % spec["libxt"].prefix.include
                )
            cflags += ["-I%s" % os.path.dirname(libxt_h.directories[0])]
        if self.compiler.name in ["xl", "xl_r"]:
            # Use '-qextname' to add underscores.
            # Use '-WF,-qnotrigraph' to fix an error about a string: '... ??'
            fflags += ["-qextname", "-WF,-qnotrigraph"]

        error = Executable(fc)("empty.f", output=str, error=str, fail_on_error=False)

        if "gfortran" in error or "GNU" in error or "gfortran" in fc:
            # Use '-std=legacy' to suppress an error that used to be a
            # warning in previous versions of gfortran.
            fflags += ["-std=legacy"]

        fflags = " ".join(fflags)
        cflags = " ".join(cflags)

        # Build the tools, maketools copy them to Nek5000/bin by default.
        # We will then install Nek5000/bin under prefix after that.
        with working_dir(tools_dir):
            # Update the maketools script to use correct compilers
            filter_file(r"^#FC\s*=.*", 'FC="{0}"'.format(fc), "maketools")
            filter_file(r"^#CC\s*=.*", 'CC="{0}"'.format(cc), "maketools")
            if fflags:
                filter_file(r"^#FFLAGS=.*", 'FFLAGS="{0}"'.format(fflags), "maketools")
            if cflags:
                filter_file(r"^#CFLAGS=.*", 'CFLAGS="{0}"'.format(cflags), "maketools")

            if self.compiler.name in ["xl", "xl_r"]:
                # Patch 'maketools' to use '-qextname' when checking for
                # underscore becasue 'xl'/'xl_r' use this option to enable the
                # addition of the underscore.
                filter_file(r"^\$FC -c ", "$FC -qextname -c ", "maketools")

            libx11_lib = find_libraries(
                "libX11", spec["libx11"].prefix.lib, shared=True, recursive=True
            )
            if not libx11_lib:
                libx11_lib = find_libraries(
                    "libX11", spec["libx11"].prefix.lib64, shared=True, recursive=True
                )
            if not libx11_lib:
                raise RuntimeError("libX11 not found in %s/{lib,lib64}" % spec["libx11"].prefix)
            # There is no other way to set the X11 library path except brute
            # force:
            filter_file(r"-L\$\(X\)", libx11_lib.search_flags, join_path("prenek", "makefile"))
            filter_file(r"-L\$\(X\)", libx11_lib.search_flags, join_path("postnek", "makefile"))

            if self.compiler.name in ["xl", "xl_r"]:
                # Use '-qextname' when compiling mxm.f
                filter_file(r"\$\(OLAGS\)", "-qextname $(OLAGS)", join_path("postnek", "makefile"))
            # Define 'rename_' function that calls 'rename'
            with open(join_path("postnek", "xdriver.c"), "a") as xdriver:
                xdriver.write(
                    "\nvoid rename_(char *from, char *to)\n{\n" "   rename(from, to);\n}\n"
                )

            maxnel = self.spec.variants["MAXNEL"].value
            filter_file(r"^#MAXNEL\s*=.*", "MAXNEL=" + maxnel, "maketools")

            maketools = Executable("./maketools")

            # Build the tools
            if "+genbox" in spec:
                maketools("genbox")
            if "+n2to3" in spec:
                maketools("n2to3")
            if "+postnek" in spec:
                maketools("postnek")
            if "+reatore2" in spec:
                maketools("reatore2")
            if "+genmap" in spec:
                maketools("genmap")
            if "+nekmerge" in spec:
                maketools("nekmerge")
            if "+prenek" in spec:
                maketools("prenek")

        # Install Nek5000/bin in prefix/bin
        install_tree(bin_dir, prefix.bin)
