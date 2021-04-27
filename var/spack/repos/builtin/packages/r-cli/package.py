# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RCli(RPackage):
    """Helpers for Developing Command Line Interfaces

    A suite of tools to build attractive command line interfaces ('CLIs'), from
    semantic elements: headings, lists, alerts, paragraphs, etc.  Supports
    custom themes via a 'CSS'-like language. It also contains a number of lower
    level 'CLI' elements: rules, boxes, trees, and 'Unicode' symbols with
    'ASCII' alternatives. It integrates with the 'crayon' package to support
    'ANSI' terminal colors."""

    homepage = "https://github.com/r-lib/cli#readme"
    url      = "https://cloud.r-project.org/src/contrib/cli_1.0.0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/cli"

    version('2.2.0', sha256='39a77af61724f8cc1f5117011e17bb2a488cbac61a7c112db078a675d3ac40b8')
    version('2.0.2', sha256='490834e5b80eb036befa0e150996bcab1c4d5d168c3d45209926e52d0d5413b6')
    version('1.1.0', sha256='4fc00fcdf4fdbdf9b5792faee8c7cf1ed5c4f45b1221d961332cda82dbe60d0a')
    version('1.0.1', sha256='ef80fbcde15760fd55abbf9413b306e3971b2a7034ab8c415fb52dc0088c5ee4')
    version('1.0.0', sha256='8fa3dbfc954ca61b8510f767ede9e8a365dac2ef95fe87c715a0f37d721b5a1d')

    depends_on('r@2.10:', type=('build', 'run'))
    depends_on('r-assertthat', type=('build', 'run'))
    depends_on('r-crayon@1.3.4:', type=('build', 'run'))
    depends_on('r-glue', when='@2:', type=('build', 'run'))
    depends_on('r-fansi', when='@2:', type=('build', 'run'))
