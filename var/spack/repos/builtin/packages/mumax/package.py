# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import shutil

from spack.package import *


class Mumax(MakefilePackage, CudaPackage):
    """GPU accelerated micromagnetic simulator."""

    homepage = "https://mumax.github.io"
    url = "https://github.com/mumax/3/archive/v3.10.tar.gz"

    license("CC-BY-3.0")

    version(
        "3.10",
        sha256="42c858661cec3896685ff4babea11e711f71fd6ea37d20c2bed7e4a918702caa",
        preferred=True,
    )
    version(
        "3.10beta",
        sha256="f20fbd90a4b531fe5a0d8acc3d4505a092a5e426f5f53218a22a87d445daf0e9",
        url="https://github.com/mumax/3/archive/3.10beta.tar.gz",
    )

    variant("cuda", default=True, description="Use CUDA; must be true")
    variant("gnuplot", default=False, description="Use gnuplot for graphs")

    depends_on("cuda")
    depends_on("go", type="build")
    depends_on("gnuplot", type="run", when="+gnuplot")

    conflicts("~cuda", msg="mumax requires cuda")

    patch(
        "https://github.com/mumax/3/commit/2cf5c9a6985c9eb16a124c6bd96aed75b4a30c24.patch?full_index=1",
        sha256="4bbb95aacdac7e2cbcb37ee8adcfb9464e69965f984c264ff094dc1cca10589b",
        when="@3.10beta",
    )

    @property
    def cuda_arch(self):
        cuda_arch = " ".join(self.spec.variants["cuda_arch"].value)
        if cuda_arch == "none":
            raise InstallError("Must select at least one value for cuda_arch")
        return cuda_arch

    @property
    def gopath(self):
        return self.stage.path

    @property
    def mumax_gopath_dir(self):
        return join_path(self.gopath, "src/github.com/mumax/3")

    def do_stage(self, mirror_only=False):
        super().do_stage(mirror_only)
        if not os.path.exists(self.mumax_gopath_dir):
            # Need to move source to $GOPATH and then symlink the original
            # stage directory
            shutil.move(self.stage.source_path, self.mumax_gopath_dir)
            force_symlink(self.mumax_gopath_dir, self.stage.source_path)

    # filter out targets that do not exist
    def edit(self, spec, prefix):
        filter_file(r"(^all: cudakernels) hooks$", r"\1", "Makefile")

    @when("@3.10beta")
    def edit(self, spec, prefix):
        filter_file(r"(^ln -sf .*)", r"#\1", "make.bash")
        filter_file(r"(^\(cd test)", r"#\1", "make.bash")
        filter_file(r"(for cc in ).*(; do)", r"\1{0}\2".format(self.cuda_arch), "cuda/make.bash")

    def setup_build_environment(self, env):
        env.prepend_path("GOPATH", self.gopath)
        env.set("CUDA_CC", self.cuda_arch)
        env.set("NVCC_CCBIN", spack_cc)

    def install(self, spec, prefix):
        go("mod init github.com/mumax/3")
        make()
        with working_dir(self.gopath):
            install_tree("bin", prefix.bin)
