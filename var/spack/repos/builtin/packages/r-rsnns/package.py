# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class RRsnns(RPackage):
    """The Stuttgart Neural Network Simulator (SNNS) is a library containing
    many standard implementations of neural networks. This package wraps the
    SNNS functionality to make it available from within R. Using the RSNNS
    low-level interface, all of the algorithmic functionality and flexibility
    of SNNS can be accessed. Furthermore, the package contains a convenient
    high-level interface, so that the most common neural network topologies
    and learning algorithms integrate seamlessly into R."""

    homepage = "http://sci2s.ugr.es/dicits/software/RSNNS"
    url      = "https://cloud.r-project.org/src/contrib/RSNNS_0.4-7.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/RSNNS"

    version('0.4-11', sha256='87943126e98ae47f366e3025d0f3dc2f5eb0aa2924508fd9ee9a0685d7cb477c')
    version('0.4-10.1', sha256='38bb3d172390bd01219332ec834744274b87b01f94d23b29a9d818c2bca04071')
    version('0.4-7', sha256='ec941dddda55e4e29ed281bd8768a93d65e0d86d56ecab0f2013c64c8d1a4994')

    depends_on('r@2.10.0:', type=('build', 'run'))
    depends_on('r-rcpp@0.8.5:', type=('build', 'run'))
