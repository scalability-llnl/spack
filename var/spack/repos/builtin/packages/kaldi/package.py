# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
from fnmatch import fnmatch
from os.path import join

from llnl.util.symlink import readlink

from spack.package import *


class Kaldi(Package):  # Does not use Autotools
    """Kaldi is a toolkit for speech recognition written
    in C++ and licensed under the Apache License v2.0.
    Kaldi is intended for use by speech recognition researchers."""

    homepage = "https://github.com/kaldi-asr/kaldi"
    git = "https://github.com/kaldi-asr/kaldi.git"

    license("Apache-2.0")

    version("master")
    version("2021-11-16", commit="6e03a3f5f99d6d8c22494d90b7e7f9ceb0117ac8")
    version("2019-09-29", commit="6ffde4b41c58de778245149690927d592cd5956a")
    version("2019-07-29", commit="7637de77e0a77bf280bef9bf484e4f37c4eb9475")
    version("2018-07-11", commit="6f2140b032b0108bc313eefdca65151289642773")
    version("2015-10-07", commit="c024e8aa0a727bf76c91a318f76a1f8b0b59249e")

    depends_on("cxx", type="build")  # generated

    variant("shared", default=True, description="build shared libraries")
    variant("double", default=False, description="build with double precision floats")
    variant("cuda", default=False, description="build with CUDA")

    depends_on("blas")
    depends_on("cuda", when="+cuda")
    depends_on("sph2pipe", type="run")
    depends_on("sctk", type="run")
    depends_on("speex", type="run")
    depends_on("openfst@1.4.1-patch", when="@2015-10-07")
    depends_on("openfst@1.6.0:", when="@2018-07-11")
    depends_on("openfst@1.6.0:", when="@2019-07-29")
    depends_on("openfst@1.6.7:1.7.3", when="@2019-09-29:")
    depends_on("cub", when="@2019-07-29:^cuda@:10")

    patch("openfst-1.4.1.patch", when="@2015-10-07")
    patch("0001_CMakeLists_txt.patch", when="+cuda@11:")

    # Change process of version analysis when using Fujitsu compiler.
    patch("fujitsu_fix_version_analysis.patch", when="@2018-07-11:%fj")

    def install(self, spec, prefix):
        configure_args = ["--fst-root=" + spec["openfst"].prefix]
        configure_args.append("--fst-version=" + str(spec["openfst"].version))
        configure_args.append("--speex-root=" + spec["speex"].prefix)
        configure_args.append("--cub-root=" + spec["cuda"].prefix.include)

        if spec.satisfies("~shared"):
            configure_args.append("--static")
        else:
            configure_args.append("--shared")

        if spec.satisfies("^[virtuals=blas] openblas"):
            configure_args.append("--mathlib=OPENBLAS")
            configure_args.append("--openblas-root=" + spec["blas"].prefix)
            if "+openmp" in spec["blas"].variants:
                configure_args.append("--threaded-math=yes")
        elif spec.satisfies("^[virtuals=blas] atlas"):
            configure_args.append("--mathlib=ATLAS")
            configure_args.append("--atlas-root=" + spec["blas"].prefix)
            if "+pthread" in spec["blas"].variants:
                configure_args.append("--threaded-atlas")
        elif spec.satisfies("^[virtuals=blas] intel-parallel-studio") or spec.satisfies(
            "^[virtuals=blas] intel-mkl"
        ):
            configure_args.append("--mathlib=MKL")
            configure_args.append("--mkl-root=" + spec["blas"].prefix.mkl)
            if "+openmp" in spec["blas"].variants:
                configure_args.append("--mkl-threading=iomp")

        if spec.satisfies("+cuda"):
            configure_args.append("--use-cuda=yes")
            configure_args.append("--cudatk-dir=" + spec["cuda"].prefix)

        if spec.satisfies("@2019-07-29: ^cuda@:10"):
            configure_args.append("--cub-root=" + spec["cub"].prefix.include)

        with working_dir("src"):
            configure(*configure_args)
            make()

            mkdirp(prefix.bin)
            for root, dirs, files in os.walk("."):
                for name in files:
                    if (
                        name.endswith("." + dso_suffix)
                        or name.endswith(".cc")
                        or name.endswith(".pptx")
                    ):
                        continue
                    if "configure" == name:
                        continue
                    if os.access(join(root, name), os.X_OK):
                        install(join(root, name), prefix.bin)

            mkdir(prefix.lib)
            for root, dirs, files in os.walk("lib"):
                for name in files:
                    if name.endswith("." + dso_suffix):
                        fpath = join(root, name)
                        src = readlink(fpath)
                        install(src, prefix.lib)

            for root, dirs, files in os.walk("."):
                for name in files:
                    if fnmatch(name, "*.h"):
                        mkdirp(join(prefix.include, root.strip("./")))
                        install(join(root, name), join(prefix.include, root.strip("./")))
        egs_dir = join(prefix, "egs")
        install_tree("egs", egs_dir)
