# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Cellranger(Package):
    """Cellranger is a set of analysis pipelines that process Chromium single cell data to
    align reads, generate feature-barcode matrices, perform clustering and other secondary
    analysis, and more.

    This package requires the user to accept a license and to download the tarball manually.
    Once downloaded, the file should be placed within a manual mirror or within the current
    directory. For instructions on making a manual mirror, see
    https://spack.readthedocs.io/en/latest/mirrors.html"""

    homepage = "https://www.10xgenomics.com/support/software/cell-ranger/latest"
    manual_download = True
    license_url = "support.10xgenomics.com/license"

    version("7.2.0", sha256="b092bd4e3ab585ad051a231fbdd8f3f0f5cbcd10f657eeab86bec98cd594502c")
    version("7.1.0", sha256="5c4f9b142e3c30ad10ae15d25868df2b4fd05bdb3bbd47da0c83a7cc649b577e")

    # cellranger is distributed as precompiled binaries that are not compatible with
    # processors without the avx instruction set ...
    conflicts("target=:k10")  # last AMD processor not to support avx
    conflicts("target=:westmere")  # last Intel processor not to support avx
    conflicts("target=:x86_64_v2")  # last generic architecture not to support avx

    def url_for_version(self, version):
        return "file://{0}/cellranger-{1}.tar.gz".format(os.getcwd(), version)

    def install(self, spec, prefix):
        install_tree(".", prefix)
