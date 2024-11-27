# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Xeniumranger(Package):
    """The Xenium In Situ software suite is a set of software applications for analyzing and
    visualizing in situ gene expression data produced by the Xenium Analyzer. Xenium Ranger
    provides flexible off-instrument reanalysis of Xenium In Situ data.

    This package requires the user to accept a license and to download the tarball manually.
    Once downloaded, the file should be placed within a manual mirror or within the current
    directory. For instructions on making a manual mirror, see
    https://spack.readthedocs.io/en/latest/mirrors.html"""

    homepage = "https://www.10xgenomics.com/support/software/xenium-ranger/latest"
    manual_download = True
    license_url = "support.10xgenomics.com/license"

    version("1.7.1", sha256="3bfa85de75ef473b54a5a6d853649999e446f2f00cc202750bb22af5078965a1")

    # xeniumranger is distributed as precompiled binaries that are not compatible with
    # processors without the avx instruction set ...
    # https://www.10xgenomics.com/support/software/xenium-ranger/downloads/XR-system-requirements
    conflicts("target=:k10")  # last AMD processor not to support avx
    conflicts("target=:westmere")  # last Intel processor not to support avx
    conflicts("target=:x86_64_v2")  # last generic architecture not to support avx

    def url_for_version(self, version):
        return "file://{0}/xeniumranger-{1}.tar.gz".format(os.getcwd(), version)

    def install(self, spec, prefix):
        install_tree(".", prefix)
