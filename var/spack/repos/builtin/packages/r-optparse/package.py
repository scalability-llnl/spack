# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class ROptparse(RPackage):
    """A command line parser inspired by Python's 'optparse' library to be used
       with Rscript to write "#!" shebang scripts that accept short and long
       flag/options"""

    homepage = "https://cloud.r-project.org/package=optparse"
    url      = "https://cloud.r-project.org/src/contrib/optparse_1.6.0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/optparse"

    version('1.6.2', sha256='b5a5a49ae05005f20359868329b73daac83d50f5e088981dcf5c41399534377f')
    version('1.6.1', sha256='819be3eff54cb7f3f18703eed9714fc655290ab8e169f87605433d069b597e13')
    version('1.6.0', sha256='10e816bb8f5b08d52cfd3a0028903a8c62ef9cf7bfd85f9dae8af442e82bfbb4')

    depends_on('r@2.9.0:', type=('build', 'run'))
    depends_on('r-getopt@1.20.2:', type=('build', 'run'))
