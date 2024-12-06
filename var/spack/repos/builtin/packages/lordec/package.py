# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.pkg.builtin.boost import Boost


class Lordec(MakefilePackage):
    """LoRDEC is a program to correct sequencing errors in long reads from
    3rd generation sequencing with high error rate, and is especially
    intended for PacBio reads."""

    homepage = "http://www.atgc-montpellier.fr/lordec/"
    url = "https://gite.lirmm.fr/lordec/lordec-releases/uploads/e3116a5f251e46e47f7a3b7ddb2bd7f6/lordec-src_0.8.tar.gz"

    license("CECILL-2.1")

    version("0.9", sha256="8108b82a8404fbf44c7e300d3abb43358ccc28993f90546168a20ca82536923b")
    version("0.8", sha256="3894a7c57649a3545b598f92a48d55eda66d729ab51606b00470c50611b12823")

    depends_on("cxx", type="build")  # generated

    def url_for_version(self, version):
        if version == Version("0.8"):
            return "https://gite.lirmm.fr/lordec/lordec-releases/uploads/e3116a5f251e46e47f7a3b7ddb2bd7f6/lordec-src_0.8.tar.gz"
        if version == Version("0.9"):
            return "https://gite.lirmm.fr/lordec/lordec-releases/uploads/800a96d81b3348e368a0ff3a260a88e1/lordec-src_0.9.tar.bz2"

    depends_on("boost@1.48.0:1.64.0", type=["build", "link"])
    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants)
    depends_on("gatb-core@1.4.1:", type=["build", "link", "run"])
    depends_on("zlib-api", type=["build", "link"])

    build_targets = ["clean", "all"]

    def edit(self, spec, prefix):
        lbstr = "AUTOMATIC_LIBBOOST_LOCAL_INSTALL=no"
        filter_file("^AUTOMATIC_LIBBOOST_LOCAL_INSTALL.*$", lbstr, "Makefile")
        filter_file("gatb_v.*gatb_core.hpp", "", "Makefile")

    def install(self, spec, prefix):
        mkdir(prefix.include)
        install("*.h", prefix.include)
        mkdir(prefix.bin)
        binaries = [
            "lordec-correct",
            "lordec-stat",
            "lordec-trim",
            "lordec-trim-split",
            "lordec-build-SR-graph",
        ]
        for binary in binaries:
            install(binary, prefix.bin)
        mkdir(prefix.tools)
        install("lordec_sge_slurm_wrapper.sh", prefix.tools)
