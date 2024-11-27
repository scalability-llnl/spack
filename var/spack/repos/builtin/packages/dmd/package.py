# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Dmd(MakefilePackage):
    """DMD is the reference compiler for the D programming language."""

    homepage = "https://github.com/dlang/dmd"
    url = "https://github.com/dlang/dmd/archive/v2.081.1.tar.gz"

    license("BSL-1.0")

    version("2.081.1", sha256="14f3aafe1c93c86646aaeb3ed7361a5fc5a24374cf25c8848c81942bfd9fae1a")
    version("2.081.0", sha256="29b9882ed424b744df83ac73182d4ae952251029ebd16117d18f9cc1e83542e2")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("openssl")
    depends_on("curl")

    # https://wiki.dlang.org/Building_under_Posix
    resource(
        name="druntime",
        url="https://github.com/dlang/druntime/archive/v2.081.1.tar.gz",
        sha256="8313af32dce71f767fb0072cae699cbfe7196cf01b0ce1c5dd416a71d94f5fee",
        placement="druntime",
    )
    resource(
        name="phobos",
        url="https://github.com/dlang/phobos/archive/v2.081.1.tar.gz",
        sha256="d945c6fd1be14dff5fcbf45c1e11302e12bebac56d55e4e97e48e150f2899e04",
        placement="phobos",
    )
    resource(
        name="tools",
        url="https://github.com/dlang/tools/archive/v2.081.1.tar.gz",
        sha256="71fa249dbfd278eec2b95ce577af32e623e44caf0d993905ddc189e3beec21d0",
        placement="tools",
    )

    def setup_run_environment(self, env):
        env.prepend_path("PATH", self.prefix.linux.bin64)
        env.prepend_path("LIBRARY_PATH", self.prefix.linux.lib64)
        env.prepend_path("LD_LIBRARY_PATH", self.prefix.linux.lib64)

    def edit(self, spec, prefix):
        # Move contents to dmd/
        mkdir = which("mkdir")
        mkdir("dmd")
        mv = which("mv")
        dmd_files = [
            f
            for f in os.listdir(".")
            if not f.startswith(("dmd", "druntime", "phobos", "tools", "spack-build"))
        ]
        for f in dmd_files:
            mv(f, "dmd")
        # Edit
        dmd_mak = FileFilter("dmd/posix.mak")
        dmd_mak.filter("$(PWD)/../install", prefix, string=True)
        dr_mak = FileFilter("druntime/posix.mak")
        dr_mak.filter("INSTALL_DIR=.*", "INSTALL_DIR={0}".format(prefix))
        pb_mak = FileFilter("phobos/posix.mak")
        pb_mak.filter("INSTALL_DIR = .*", "INSTALL_DIR = {0}".format(prefix))
        tl_mak = FileFilter("tools/posix.mak")
        tl_mak.filter("INSTALL_DIR = .*", "INSTALL_DIR = {0}".format(prefix))

    def build(self, spec, prefix):
        with working_dir("dmd"):
            make("-f", "posix.mak", "AUTO_BOOTSTRAP=1")
        with working_dir("phobos"):
            make("-f", "posix.mak")

    def install(self, spec, prefix):
        with working_dir("dmd"):
            make("-f", "posix.mak", "install", "AUTO_BOOTSTRAP=1")
        with working_dir("phobos"):
            make("-f", "posix.mak", "install")
        with working_dir("tools"):
            make("-f", "posix.mak", "install")
        with working_dir("druntime"):
            make("-f", "posix.mak", "install")
