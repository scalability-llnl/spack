# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RCli(RPackage):
    """A suite of tools designed to build attractive command line interfaces
       ('CLIs'). Includes tools for drawing rules, boxes, trees, and
       'Unicode' symbols with 'ASCII' alternatives."""

    homepage = "https://github.com/r-lib/cli#readme"
    url      = "https://cloud.r-project.org/src/contrib/cli_1.0.0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/cli"

    version('2.0.2', sha256='490834e5b80eb036befa0e150996bcab1c4d5d168c3d45209926e52d0d5413b6')
    version('1.1.0', sha256='4fc00fcdf4fdbdf9b5792faee8c7cf1ed5c4f45b1221d961332cda82dbe60d0a')
    version('1.0.1', sha256='ef80fbcde15760fd55abbf9413b306e3971b2a7034ab8c415fb52dc0088c5ee4')
    version('1.0.0', sha256='8fa3dbfc954ca61b8510f767ede9e8a365dac2ef95fe87c715a0f37d721b5a1d')

    depends_on('r@2.10:', type=('build', 'run'))
    depends_on('r-assertthat', type=('build', 'run'))
    depends_on('r-crayon@1.3.4:', type=('build', 'run'))
    depends_on('r-glue', when='@2:', type=('build', 'run'))
    depends_on('r-fansi', when='@2:', type=('build', 'run'))
