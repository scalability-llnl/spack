# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Scs(MakefilePackage):
    """A C package that solves convex cone problems via operator splitting"""

    homepage = "https://github.com/cvxgrp/scs"
    url = "https://github.com/cvxgrp/scs/archive/2.1.1.tar.gz"

    license("MIT")

    version("2.1.1", sha256="0e20b91e8caf744b84aa985ba4e98cc7235ee33612b2bad2bf31ea5ad4e07d93")

    depends_on("c", type="build")  # generated

    variant("cuda", default=False, description="Build with Cuda support")

    depends_on("blas")
    depends_on("lapack")
    depends_on("cuda", when="+cuda")

    # make sure install_gpu target installs all libs not only the gpu ones
    patch("make_gpu.patch")

    def edit(self, spec, prefix):
        filter_file(r"-lblas", spec["blas"].libs.ld_flags, "scs.mk")
        filter_file(r"-llapack", spec["lapack"].libs.ld_flags, "scs.mk")

    def build(self, spec, prefix):
        if "+cuda" in spec:
            make("default", "gpu")
        else:
            make()

    def install(self, spec, prefix):
        if "+cuda" in spec:
            make("PREFIX=" + prefix, "install_gpu")
        else:
            make("PREFIX=" + prefix, "install")
