# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RBiocmanager(RPackage):
    """Access the Bioconductor Project Package Repository.

    A convenient tool to install and update Bioconductor packages."""

    cran = "BiocManager"

    version("1.30.24", sha256="645c423bb144dbd476cb308678bd36e06c1a3494115f157166dd3f59955ec7d1")
    version("1.30.20", sha256="b9e72d7687abbd785a69fecb530ec86ad92257a6be95b8e15953b193a516d5ea")
    version("1.30.19", sha256="6897ab1c58ab2fa3108e22d70bc4150c683bb4ac29355ba7886b88acc30c18e2")
    version("1.30.18", sha256="f763126b45614e1b83260da5311923eac50db24002f3c22fa5f667434a5b5c35")
    version("1.30.16", sha256="75a754a55192ef6aa6ac9b054fd5381ff03fe6bb8b2e033eb8143da930ef3855")
    version("1.30.10", sha256="f3b7a412b42be0ab8df5fcd9bf981876ba9e5c55bc5faaca7af7ede3b6d0c90e")
