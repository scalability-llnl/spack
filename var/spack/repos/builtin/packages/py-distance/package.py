# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDistance(PythonPackage):
    """This package provides helpers for computing similarities
    between arbitrary sequences. Included metrics are
    Levenshtein, Hamming, Jaccard, and Sorensen distance, plus
    some bonuses."""

    homepage = "https://github.com/doukremt/distance"
    pypi = "Distance/Distance-0.1.3.tar.gz"

    license("GPL-2.0-only")

    version("0.1.3", sha256="60807584f5b6003f5c521aa73f39f51f631de3be5cccc5a1d67166fcbf0d4551")

    depends_on("c", type="build")  # generated

    depends_on("py-setuptools", type="build")
