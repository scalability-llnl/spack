# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class GenerateNinja(Package):
    """
    A meta-build system that generates build files for Ninja.
    This is a fork of the Google GN package with some minor features and bug fixes
    """

    homepage = "https://github.com/o-lim/generate-ninja"
    url = "https://github.com/o-lim/generate-ninja/archive/refs/tags/v0.4.1.tar.gz"

    license("BSD", checked_by="teaguesterling")

    version("0.4.1", sha256="1b2bec9dd18602a4af9dc8782ca809e44305f1435d43c55f35ec9eec50ca7e9a")
    version("0.4.0", sha256="3575ed41eec49fe756dbd2c402f70cd80ba2952cc59ce2091d0a82b7bd3ce8a0")
    version("0.3.2", sha256="82e949c3970d77b28c9df7cf3f3df409798b65848e05ff415009e7e2118460a8")
    version("0.3.1", sha256="ed0112b434b80c322fcc9203646eaef17c306a804bf2ff5e5df91677c4e58678")
    version("0.3.0", sha256="e6091d34cfc6bc625bfad4bbdc001e10ed951651d0ae98785b509bdfadad6822")
    version("0.2.2", sha256="3146bdef1db9dfdc2d48bb5ee5e8e4ef9642ebea7cf39c432681685db8a11c86")
    version("0.2.1", sha256="bf27ddde69bd0791ce86bd3ab9ead51dcfb00d3f202168057b721fdc39d417c5")
    version("0.2.0", sha256="6cfd6f4a2f6d656e8d5f64d7f03a575a569b2c0f662d1d828ee790c9d9c2be25")
    version("0.1.0", sha256="eb94e0bb170416010d3efa296fce63e7fec19f1e3e9b5988b2418166ec068896")

    depends_on("ninja")
    depends_on("python", type="build")
    depends_on("llvm+clang", type="build")

    def setup_build_environment(self, env):
        env.set("DEPLOY", "1")
        env.set("CC", self.spec["llvm"].home.bin.clang)
        env.set("CXX", self.spec["llvm"].home.bin.join("clang++"))

    phases = ["configure", "build", "install"]
    #    build_targets = ["bootstrap", "gn"]
    out_dir = "out"

    def configure(self, spec, prefix):
        python("build/gen.py")

    def build(self, spec, prefix):
        ninja("-C", self.out_dir)

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install(join_path(self.out_dir, "gn"), prefix.bin.gn)
