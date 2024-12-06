# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Anicalculator(Package):
    """This tool will calculate the bidirectional average nucleotide identity
    (gANI) and Alignment Fraction (AF) between two genomes.

    Note: A manual download is required for ANIcalculator.
    Spack will search your current directory for the download file.
    Alternatively, add this file to a mirror so that Spack can find it.
    For instructions on how to set up a mirror, see
    https://spack.readthedocs.io/en/latest/mirrors.html"""

    homepage = "https://ani.jgi.doe.gov/html/download.php?"
    url = f"file://{os.getcwd()}/ANIcalculator_v1.tgz"
    manual_download = True

    version("1", sha256="236596a9a204cbcad162fc66be3506b2530b1f48f4f84d9647ccec3ca7483a43")

    depends_on("perl@5:", type="run")

    conflicts("platform=darwin", msg="ANIcalculator requires Linux")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("ANIcalculator", prefix.bin)
        install("nsimscan", prefix.bin)
        install_tree("Log", prefix.bin.Log)
