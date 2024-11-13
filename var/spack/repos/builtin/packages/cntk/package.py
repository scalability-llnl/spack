# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *
from spack.pkg.builtin.boost import Boost


class Cntk(Package):
    """The Microsoft Cognitive Toolkit is a unified deep-learning toolkit
    that describes neural networks as a series of computational steps
    via a directed graph."""

    homepage = "https://www.microsoft.com/en-us/research/product/cognitive-toolkit"
    url = "https://github.com/Microsoft/CNTK/archive/v2.0.tar.gz"
    git = "https://github.com/Microsoft/CNTK.git"

    # CNTK is not an active project since April 2019.
    version("master", branch="master")
    version("2.0", sha256="3adee17f166e2a682dfb551ca017ae5c3836ca9772c0af14215a7e76254f201c")

    depends_on("cxx", type="build")  # generated

    variant("opencv", default=False, description="Enable OpenCV support.")
    variant("kaldi", default=False, description="Enable Kaldi support.")
    variant("asgd", default=True, description="Enable DataParallelASGD powered by Multiverso.")
    variant("1bitsgd", default=False, description="Enable 1bitsgd support.")
    variant("cuda", default=False, description="Enable CUDA support.")
    variant("debug", default=False, description="Debug build.")

    depends_on("libzip")
    depends_on("openblas")
    depends_on("mpi")
    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants)
    depends_on("protobuf@3.10")
    # CNTK depends on kaldi@c02e8.
    # See https://github.com/Microsoft/CNTK/blob/master/Tools/docker/CNTK-CPUOnly-Image/Dockerfile#L105-L125
    depends_on("kaldi@2015-10-07", when="+kaldi")
    depends_on("opencv@:3+imgcodecs+imgproc", when="+opencv")
    depends_on("cuda", when="+cuda")
    depends_on("cub@1.4.1", when="+cuda")
    depends_on("cudnn@5.1", when="+cuda")
    depends_on("nccl", when="+cuda")
    depends_on("cntk1bitsgd@c8b77d", when="+1bitsgd")
    depends_on("multiverso@143187", when="+asgd")

    # Patch CNTN's build process to use libs installed outside CNTK source tree
    # multiverso, kaldi, openfst
    patch("build.patch")
    # Patch to fix BLAS inconsistency between CNTK and KaldiReader
    patch("kaldireader-openblas.patch")
    # Patch to change behaviour of lock file - https://github.com/Microsoft/CNTK/issues/62
    patch("lock-file.patch")

    # It seems that cntk, at least version 2.0, can not be built with GCC
    # beyond 4.8.5.
    conflicts("%gcc@5:")

    def patch(self):
        protobuf_path = os.path.split(self.spec["protobuf"].libs[0])
        protobuf_ld_flags = self.spec["protobuf"].libs.ld_flags

        filter_file(
            r"(protobuf_check=)lib/libprotobuf\.a",
            r"\1{0}/{1}".format(os.path.basename(protobuf_path[0]), protobuf_path[1]),
            "configure",
        )
        filter_file(r"\$\(PROTOBUF_PATH\)/lib/libprotobuf.a", protobuf_ld_flags, "Makefile")

    def install(self, spec, prefix):
        args = []

        args.append("--with-mpi=" + spec["mpi"].prefix)
        args.append("--with-openblas=" + spec["openblas"].prefix)
        args.append("--with-libzip=" + spec["libzip"].prefix)
        args.append("--with-boost=" + spec["boost"].prefix)
        args.append("--with-protobuf=" + spec["protobuf"].prefix)

        if spec.satisfies("+debug"):
            args.append("--with-buildtype=debug")
        else:
            args.append("--with-buildtype=release")

        if spec.satisfies("+1bitsgd"):
            args.append("--1bitsgd=yes")
            args.append("--with-1bitsgd={0}/include".format(spec["cntk1bitsgd"].prefix))

        if spec.satisfies("+asgd"):
            args.append("--asgd=yes")
            args.append("--with-multiverso={0}".format(spec["multiverso"].prefix))
        else:
            args.append("--asgd=no")

        if spec.satisfies("+opencv"):
            args.append("--with-opencv=" + spec["opencv"].prefix)

        if spec.satisfies("+kaldi"):
            args.append("--with-kaldi=" + spec["kaldi"].prefix)
            args.append("--with-openfst=" + spec["openfst"].prefix)

        if spec.satisfies("+cuda"):
            args.append("--cuda=yes")
            args.append("--with-cuda={0}".format(spec["cuda"].prefix))
            args.append("--with-cub={0}".format(spec["cub"].prefix.include))
            args.append("--with-cudnn={0}".format(spec["cudnn"].prefix))
            args.append("--with-nccl={0}".format(spec["nccl"].prefix))
            args.append("--with-gdk-include={0}".format(spec["cuda"].prefix.include))
            args.append("--with-gdk-nvml-lib={0}/stubs".format(spec["cuda"].prefix.lib64))

        configure(*args)

        make()

        install_tree("bin", prefix.bin)
        install_tree("lib", prefix.lib)
        install_tree("Examples", join_path(prefix, "Examples"))
        install_tree("Tutorials", join_path(prefix, "Tutorials"))
