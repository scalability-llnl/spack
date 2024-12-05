# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from llnl.util.filesystem import find_first

from spack.package import *


class Tk(AutotoolsPackage, SourceforgePackage):
    """Tk is a graphical user interface toolkit that takes developing desktop
    applications to a higher level than conventional approaches. Tk is the standard GUI
    not only for Tcl, but for many other dynamic languages, and can produce rich, native
    applications that run unchanged across Windows, Mac OS X, Linux and more."""

    homepage = "https://www.tcl.tk"
    sourceforge_mirror_path = "tcl/tk8.6.5-src.tar.gz"

    license("TCL")

    version("8.6.11", sha256="5228a8187a7f70fa0791ef0f975270f068ba9557f57456f51eb02d9d4ea31282")
    version("8.6.10", sha256="63df418a859d0a463347f95ded5cd88a3dd3aaa1ceecaeee362194bc30f3e386")
    version("8.6.8", sha256="49e7bca08dde95195a27f594f7c850b088be357a7c7096e44e1158c7a5fd7b33")
    version("8.6.6", sha256="d62c371a71b4744ed830e3c21d27968c31dba74dd2c45f36b9b071e6d88eb19d")
    version("8.6.5", sha256="fbbd93541b4cd467841208643b4014c4543a54c3597586727f0ab128220d7946")
    version("8.6.3", sha256="ba15d56ac27d8c0a7b1a983915a47e0f635199b9473cf6e10fbce1fc73fd8333")
    version("8.5.19", sha256="407af1de167477d598bd6166d84459a3bdccc2fb349360706154e646a9620ffa")

    variant("xft", default=True, description="Enable X FreeType")
    variant("xss", default=True, description="Enable X Screen Saver")

    extends("tcl", type=("build", "link", "run"))

    depends_on("tcl@8.6:", type=("build", "link", "run"), when="@8.6:")
    depends_on("libx11")
    depends_on("libxft", when="+xft")
    depends_on("libxscrnsaver", when="+xss")

    configure_directory = "unix"

    # https://core.tcl-lang.org/tk/tktview/3598664fffffffffffff
    # https://core.tcl-lang.org/tk/info/8b679f597b1d17ad
    # https://core.tcl-lang.org/tk/info/997b17c343444e48
    patch(
        "https://raw.githubusercontent.com/macports/macports-ports/v2.7.0-archive/x11/tk/files/patch-unix-Makefile.in.diff",
        sha256="54bba3d2b3550b7e2c636881c1a3acaf6e1eb743f314449a132864ff47fd0010",
        level=0,
        when="@:8.6.11 platform=darwin",
    )
    patch(
        "https://raw.githubusercontent.com/macports/macports-ports/v2.7.0-archive/x11/tk/files/patch-dyld_fallback_library_path.diff",
        sha256="9ce6512f1928db9987986f4d3540207c39429395d5234bd6489ba9d86a6d9c31",
        level=0,
        when="platform=darwin",
    )

    def configure_args(self):
        spec = self.spec
        config_args = [
            "--with-tcl={0}".format(spec["tcl"].libs.directories[0]),
            "--x-includes={0}".format(spec["libx11"].headers.directories[0]),
            "--x-libraries={0}".format(spec["libx11"].libs.directories[0]),
        ]
        config_args += self.enable_or_disable("xft")
        config_args += self.enable_or_disable("xss")

        return config_args

    def install(self, spec, prefix):
        with working_dir(self.build_directory):
            make("install")

            # Some applications like Expect require private Tk headers.
            make("install-private-headers")

            # Copy source to install tree
            installed_src = join_path(self.spec.prefix, "share", self.name, "src")
            stage_src = os.path.realpath(self.stage.source_path)
            install_tree(stage_src, installed_src)

            # Replace stage dir -> installed src dir in tkConfig
            filter_file(
                stage_src,
                installed_src,
                join_path(self.spec["tk"].libs.directories[0], "tkConfig.sh"),
            )

    @run_after("install")
    def symlink_wish(self):
        with working_dir(self.prefix.bin):
            symlink("wish{0}".format(self.version.up_to(2)), "wish")

    def test_tk_help(self):
        """run tk help"""
        tk = self.spec["tk"].command
        tk("-h")

    def test_tk_load(self):
        """check that tk can be loaded"""
        test_data_dir = self.test_suite.current_test_data_dir
        test_file = test_data_dir.join("test.tcl")
        tcl = self.spec["tcl"].command
        tcl(test_file)

    @property
    def command(self):
        """Returns the wish command.

        Returns:
            Executable: the wish command
        """
        # Although we symlink wishX.Y to wish, we also need to support external
        # installations that may not have this symlink, or may have multiple versions
        # of Tk installed in the same directory.
        return Executable(
            os.path.realpath(self.prefix.bin.join("wish{0}".format(self.version.up_to(2))))
        )

    @property
    def libs(self):
        return find_libraries(
            ["libtk{0}".format(self.version.up_to(2))], root=self.prefix, recursive=True
        )

    def _find_script_dir(self):
        # Put more-specific prefixes first
        check_prefixes = [
            join_path(self.prefix, "share", "tk{0}".format(self.version.up_to(2))),
            self.prefix,
        ]
        for prefix in check_prefixes:
            result = find_first(prefix, "tk.tcl")
            if result:
                return os.path.dirname(result)
        raise RuntimeError("Cannot locate tk.tcl")

    def setup_run_environment(self, env):
        """Set TK_LIBRARY to the directory containing tk.tcl.

        For further info, see:

        * https://www.tcl-lang.org/man/tcl/TkCmd/tkvars.htm
        """
        # When using tkinter from within spack provided python+tkinter,
        # python will not be able to find Tk unless TK_LIBRARY is set.
        env.set("TK_LIBRARY", self._find_script_dir())

    def setup_dependent_build_environment(self, env, dependent_spec):
        """Set TK_LIBRARY to the directory containing tk.tcl.

        For further info, see:

        * https://www.tcl-lang.org/man/tcl/TkCmd/tkvars.htm
        """
        env.set("TK_LIBRARY", self._find_script_dir())
