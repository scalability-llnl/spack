# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Tix(AutotoolsPackage):
    """Tix, the Tk Interface eXtension, is a powerful set of user interface components
    that expands the capabilities of your Tcl/Tk and Python applications. Using Tix
    together with Tk will greatly enhance the appearance and functionality of your
    application."""

    homepage = "https://sourceforge.net/projects/tix/"
    url = "https://sourceforge.net/projects/tix/files/tix/8.4.3/Tix8.4.3-src.tar.gz/download"

    license("TCL")

    version("8.4.3", sha256="562f040ff7657e10b5cffc2c41935f1a53c6402eb3d5f3189113d734fd6c03cb")

    depends_on("c", type="build")  # generated

    extends("tcl", type=("build", "link", "run"))
    depends_on("tk", type=("build", "link", "run"))

    patch(
        "https://raw.githubusercontent.com/macports/macports-ports/v2.7.0-archive/x11/tix/files/panic.patch",
        sha256="1be1a1c7453f6ab8771f90d7e7c0f8959490104752a16a8755bbb7287a841a96",
        level=0,
    )
    # This patch causes 'install' to fail on RHEL8 with at least gcc@10.3.1 with
    # "error: expected ')' before '->' token in expansion of macro 'Tcl_Panic'".
    #
    # TBD: Is the problem the platform, os, or compiler?
    patch(
        "https://raw.githubusercontent.com/macports/macports-ports/v2.7.0-archive/x11/tix/files/implicit.patch",
        sha256="8a2720368c7757896814684147029d8318b9aa3b0914b3f37dd5e8a8603a61d3",
        level=0,
        when="platform=darwin",
    )
    patch(
        "https://raw.githubusercontent.com/macports/macports-ports/v2.7.0-archive/x11/tix/files/patch-generic-tixGrSort.c.diff",
        sha256="99b33cc307f71bcf9cc6f5a44b588f22956884ce3f1e4c716ad64c79cf9c5f41",
        level=0,
    )
    patch(
        "https://raw.githubusercontent.com/macports/macports-ports/v2.7.0-archive/x11/tix/files/patch-missing-headers.diff",
        sha256="d9f789dcfe5f4c5ee4589a18f9f410cdf162e41d35d00648c1ef37831f4a2b2b",
        level=0,
    )
    patch(
        "https://raw.githubusercontent.com/macports/macports-ports/v2.7.0-archive/x11/tix/files/patch-tk_x11.diff",
        sha256="1e28d8eee1aaa956a00571cf495a4775e72a993958dff1cabfbc5f102e327a6f",
        level=0,
    )
    patch(
        "https://raw.githubusercontent.com/macports/macports-ports/v2.7.0-archive/x11/tix/files/patch-tk_aqua.diff",
        sha256="41a717f5d95f61b4b8196ca6f14ece8f4764d4ba58fb2e1ae15e3240ee5ac534",
        level=0,
        when="platform=darwin",
    )
    patch(
        "https://raw.githubusercontent.com/macports/macports-ports/v2.7.0-archive/x11/tix/files/patch-dyld_variable.diff",
        sha256="719eb2e4d8c5d6aae897e5f676cf5ed1a0005c1bd07fd9b18705d81a005f592b",
        level=0,
        when="platform=darwin",
    )

    def configure_args(self):
        spec = self.spec
        args = [
            "--with-tcl={0}".format(spec["tcl"].libs.directories[0]),
            "--with-tk={0}".format(spec["tk"].libs.directories[0]),
            "--exec-prefix={0}".format(self.prefix),
        ]
        return args

    @run_after("install")
    def darwin_fix(self):
        # The shared library is not installed correctly on Darwin; fix this
        if "platform=darwin" in self.spec:
            fix_darwin_install_name(self.prefix.lib.Tix + str(self.version))

    def test_tcl(self):
        """Test that tix can be loaded"""
        test_data_dir = self.test_suite.current_test_data_dir
        test_file = test_data_dir.join("test.tcl")
        tcl = self.spec["tcl"].command
        tcl(test_file)

    @property
    def libs(self):
        return find_libraries(["libTix{0}".format(self.version)], root=self.prefix, recursive=True)

    def setup_run_environment(self, env):
        """Set TIX_LIBRARY to the directory containing Tix.tcl.

        For further info, see:

        * http://tix.sourceforge.net/docs/pdf/TixUser.pdf
        """
        # When using tkinter.tix from within spack provided python+tkinter+tix,
        # python will not be able to find Tix unless TIX_LIBRARY is set.
        env.set("TIX_LIBRARY", os.path.dirname(find(self.prefix, "Tix.tcl")[0]))

    def setup_dependent_build_environment(self, env, dependent_spec):
        """Set TIX_LIBRARY to the directory containing Tix.tcl.

        For further info, see:

        * http://tix.sourceforge.net/docs/pdf/TixUser.pdf
        """
        env.set("TIX_LIBRARY", os.path.dirname(find(self.prefix, "Tix.tcl")[0]))
