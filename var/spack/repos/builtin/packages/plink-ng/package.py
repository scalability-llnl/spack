# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PlinkNg(Package):
    """A comprehensive update to the PLINK association analysis toolset."""

    homepage = "https://www.cog-genomics.org/plink/2.0/"
    url = "https://www.cog-genomics.org/static/bin/plink2_src_200511.zip"

    version("200511", sha256="00cff19bece88acb7a21ba098501cb677b78d22c9f3ca5bcdc869139a40db816")

    depends_on("zlib-api")
    depends_on("zstd@1.4.4:")
    depends_on("cblas")
    depends_on("blas")
    depends_on("lapack")

    conflicts("%gcc@:4")

    def url_for_version(self, ver):
        template = "https://www.cog-genomics.org/static/bin/plink2_src_{0}.zip"
        return template.format(ver)

    def setup_build_environment(self, env):
        zlib = join_path(self.spec["zlib-api"].prefix.lib, "libz.a")
        env.set("ZLIB", zlib)

    def install(self, spec, prefix):
        ld_flags = [spec["lapack"].libs.ld_flags, spec["blas"].libs.ld_flags]
        filter_file("-llapack -lcblas -lblas", " ".join(ld_flags), "build.sh", string=True)
        which("sh")("build.sh")
        install_tree(".", prefix)
