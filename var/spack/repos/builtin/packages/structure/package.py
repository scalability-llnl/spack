# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Structure(MakefilePackage):
    """Structure is a free software package for using multi-locus genotype
    data to investigate population structure."""

    homepage = "https://web.stanford.edu/group/pritchardlab/structure.html"
    url = "https://web.stanford.edu/group/pritchardlab/structure_software/release_versions/v2.3.4/structure_kernel_source.tar.gz"

    version("2.3.4", sha256="f2b72b9189a514f53e921bbdc1aa3dbaca7ac34a8467af1f972c7e4fc9c0bb37")

    depends_on("c", type="build")  # generated

    def url_for_version(self, version):
        url = "http://web.stanford.edu/group/pritchardlab/structure_software/release_versions/v{0}/structure_kernel_source.tar.gz"
        return url.format(version)

    @when("%gcc@10:")
    def edit(self, spec, prefix):
        filter_file(r"(CFLAGS =.*$)", "\\1 -fcommon", "Makefile")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("structure", prefix.bin)
        install("mainparams", prefix.bin)
        install("extraparams", prefix.bin)
