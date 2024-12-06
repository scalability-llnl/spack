# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import stat
from pathlib import Path

from spack.package import *


class IntelXed(Package):
    """The Intel X86 Encoder Decoder library for encoding and decoding x86
    machine instructions (64- and 32-bit).  Also includes libxed-ild,
    a lightweight library for decoding the length of an instruction."""

    homepage = "https://intelxed.github.io/"
    git = "https://github.com/intelxed/xed.git"
    maintainers("mwkrentel")

    mbuild_git = "https://github.com/intelxed/mbuild.git"

    # Current versions now have actual releases and tags.
    version("main", branch="main")
    version("2024.05.20", tag="v2024.05.20", commit="7e88c3e00274a10daa6b9d053decc057f65aa0ec")
    version("2024.04.01", tag="v2024.04.01", commit="6d87b5481aa53b5ab1fc2b5a5622759c46746bf9")
    version("2024.02.22", tag="v2024.02.22", commit="d08a6f66f780a685f26322960cd3ae297dbad931")
    version("2023.10.11", tag="v2023.10.11", commit="d7d46c73fb04a1742e99c9382a4acb4ed07ae272")
    version("2023.08.21", tag="v2023.08.21", commit="01a6da8090af84cd52f6c1070377ae6e885b078f")
    version("2023.07.09", tag="v2023.07.09", commit="539a6a349cf7538a182ed3ee1f48bb9317eb185f")
    version("2023.06.07", tag="v2023.06.07", commit="4dc77137f651def2ece4ac0416607b215c18e6e4")
    version("2023.04.16", tag="v2023.04.16", commit="a3055cd0209f5c63c88e280bbff9579b1e2942e2")
    version("2022.10.11", tag="v2022.10.11", commit="9fc12ab6c0ba7a9eaadb20135369b4b4107fa670")
    version("2022.08.11", tag="v2022.08.11", commit="1ce1036aa4ab280f9a498136b37421ab390e42db")
    version("2022.04.17", tag="v2022.04.17", commit="ef19f00de14a9c2c253c1c9b1119e1617280e3f2")
    version("12.0.1", tag="12.0.1", commit="5976632eeaaaad7890c2109d0cfaf4012eaca3b8")
    version("11.2.0", tag="11.2.0", commit="40125558530137444b4ee6fd26b445bfa105b543")

    # The old 2019.03.01 version (before there were tags).
    version("10.2019.03", commit="b7231de4c808db821d64f4018d15412640c34113", deprecated=True)

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    # XED wants the mbuild directory adjacent to xed in the same directory.
    mdir = join_path("..", "mbuild")

    resource(name="mbuild", placement=mdir, git=mbuild_git, branch="main", when="@main")

    # Match xed more closely with the version of mbuild at the time.
    resource(
        name="mbuild",
        placement=mdir,
        git=mbuild_git,
        tag="v2022.07.28",
        commit="75cb46e6536758f1a3cdb3d6bd83a4a9fd0338bb",
        when="@2022.07:9999",
    )

    resource(
        name="mbuild",
        placement=mdir,
        git=mbuild_git,
        tag="v2022.04.17",
        commit="b41485956bf65d51b8c2379768de7eaaa7a4245b",
        when="@:2022.06",
    )

    variant("optimize", default=True, description="Build with -O2")
    variant("debug", default=False, description="Enable debug symbols")
    variant("pic", default=False, description="Compile with position independent code.")
    variant("examples", default=False, description="Build and install the examples")

    # Previous versions of this recipe used a different install layout than upstream Xed.
    # This has since been fixed, but some packages were written on the older install layout and
    # will not build on the upstream Xed layout.
    # Enabling this variant adds compatibility headers for such software to build successfully.
    variant(
        "deprecated-includes",
        default=False,
        sticky=True,
        description="Add compatibility headers for software written on the old include layout",
    )

    # The current mfile uses python3 by name.
    depends_on("python@3.7:", type="build")

    patch("1201-segv.patch", when="@12.0.1")
    patch("2019-python3.patch", when="@10.2019.03")
    patch("libxed-ild.patch", when="@12.0:2022.12")

    requires("target=x86_64:,aarch64:", msg="intel-xed only builds on x86-64 or aarch64")

    @when("@2023.04.16")
    def patch(self):
        # In 2023.04.16, the xed source directory must be exactly 'xed',
        # so add a symlink, but don't fail if the link already exists.
        # See: https://github.com/intelxed/xed/issues/300
        try:
            lname = join_path(self.stage.source_path, "..", "xed")
            os.symlink("spack-src", lname)
        except OSError:
            pass

    def setup_build_environment(self, env):
        # XED needs PYTHONPATH to find the mbuild directory.
        env.prepend_path("PYTHONPATH", self.mdir)

    @staticmethod
    def _make_writable(root) -> None:
        for dirpath, _, filenames in os.walk(root):
            for fn in filenames:
                path = Path(dirpath) / fn
                if not path.is_symlink():
                    path.chmod(path.stat().st_mode | stat.S_IWUSR)

    def install(self, spec, prefix):
        mfile = Executable(join_path(".", "mfile.py"))
        mfile.add_default_arg(
            f"--jobs={make_jobs}",
            f"--cc={spack_cc}",
            f"--cxx={spack_cxx}",
            "--no-werror",
            f"--prefix={prefix}",
        )
        if spec.satisfies("+optimize"):
            mfile.add_default_arg("--opt=2")
        if spec.satisfies("+debug"):
            mfile.add_default_arg("--debug")
        if spec.satisfies("+pic"):
            mfile.add_default_arg(
                f"--extra-ccflags={self.compiler.cc_pic_flag}",
                f"--extra-cxxflags={self.compiler.cxx_pic_flag}",
            )

        # Build and install first as static (the default).
        mfile("--install-dir=" + join_path("kits", "static"), "install")
        self._make_writable(prefix)

        # Rebuild and reinstall as shared. This overwrites anything installed as static before.
        shared_kit = join_path("kits", "shared")
        mfile("--clean")
        mfile(
            f"--install-dir={shared_kit}",
            "--shared",
            *(["examples"] if spec.satisfies("+examples") else []),
            "install",
        )

        if self.spec.satisfies("+examples"):
            # Install the example binaries to share/xed/examples
            install_tree(join_path(shared_kit, "bin"), prefix.share.xed.examples)

            # Add a convenience symlink for the xed example/CLI to bin/xed
            mkdirp(prefix.bin)
            symlink(prefix.share.xed.examples.xed, prefix.bin.xed)

    @run_after("install", when="+deprecated-includes")
    def install_deprecated_include_compat(self):
        """Install compatibility headers in <prefix>/include for old code"""
        for hdr in Path(self.prefix.include).glob("xed/*.h"):
            (Path(self.prefix.include) / hdr.name).write_text(
                f"""\
#warning This is a Spack compatibilty header, please update your #includes!
#include "xed/{hdr.name}"
"""
            )
