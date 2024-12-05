# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Spaceranger(Package):
    """Space Ranger is a set of analysis pipelines that process Visium data with brightfield
    and fluorescence microscope images. Space Ranger allows users to map the whole
    transcriptome in formalin fixed paraffin embedded (FFPE) and fresh frozen (FF) tissues.

    This package requires the user to accept a license and to download the tarball manually.
    Once downloaded, the file should be placed within a manual mirror or within the current
    directory. For instructions on making a manual mirror, see
    https://spack.readthedocs.io/en/latest/mirrors.html"""

    homepage = "https://www.10xgenomics.com/support/software/space-ranger/latest"
    manual_download = True
    license_url = "support.10xgenomics.com/license"

    version("2.1.1", sha256="e3c2982ae91afc4031f7b29e4b27ea012243e1c61ca8fa246b8c1f6ef7c7c241")

    # spaceranger is distributed as precompiled binaries that are not compatible with
    # processors without the avx instruction set ...
    # https://www.10xgenomics.com/support/software/space-ranger/downloads/space-ranger-system-requirements
    conflicts("target=:k10")  # last AMD processor not to support avx
    conflicts("target=:westmere")  # last Intel processor not to support avx
    conflicts("target=:x86_64_v2")  # last generic architecture not to support avx

    def url_for_version(self, version):
        return "file://{0}/spaceranger-{1}.tar.gz".format(os.getcwd(), version)

    def install(self, spec, prefix):
        install_tree(".", prefix)
