# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Lordec(MakefilePackage):
    """LoRDEC is a program to correct sequencing errors in long reads from
    3rd generation sequencing with high error rate, and is especially
    intended for PacBio reads."""

    homepage = "http://www.atgc-montpellier.fr/lordec/"
    url      = "https://gite.lirmm.fr/lordec/lordec-releases/uploads/e3116a5f251e46e47f7a3b7ddb2bd7f6/lordec-src_0.8.tar.gz"

    version('0.8', sha256='3894a7c57649a3545b598f92a48d55eda66d729ab51606b00470c50611b12823')

    depends_on('boost')
    depends_on('cmake@3.1.0:', type='build')

    build_targets = ['clean', 'all']

    def install(self, spec, prefix):
        install_tree('.', prefix.bin)
