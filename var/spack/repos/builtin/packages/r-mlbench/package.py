# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RMlbench(RPackage):
    """A collection of artificial and real-world machine learning benchmark
    problems, including, e.g., several data sets from the UCI repository."""

    homepage = "https://cloud.r-project.org/package=mlbench"
    url      = "https://cloud.r-project.org/src/contrib/mlbench_2.1-1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/mlbench"

    version('2.1-1', sha256='748141d56531a39dc4d37cf0a5165a40b653a04c507e916854053ed77119e0e6')

    depends_on('r@2.10:', type=('build', 'run'))
