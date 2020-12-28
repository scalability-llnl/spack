# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from os.path import split

from spack.package import *


class Anaconda2(Package):
    """Anaconda is a free and open-source distribution of the Python and
       R programming languages for scientific computing, that aims to
       simplify package management and deployment. Package versions are
       managed by the package management system conda.
    """

    homepage = "https://www.anaconda.com"
    url      = "https://repo.anaconda.com/archive/Anaconda2-2019.10-Linux-x86_64.sh"

    maintainers = ['ajkotobi']

    version('2019.10', sha256='8b2e7dea2da7d8cc18e822e8ec1804052102f4eefb94c1b3d0e586e126e8cd2f', expand=False)
    version('2019.07', sha256='189e16e7adf9ba4b7b7d06ecdc10ce4ad4153e5e3505b9331f3d142243e18e97', expand=False)
    version('2019.03', sha256='cedfee5b5a3f62fcdac0a1d2d12396d0f232d2213d24d6dc893df5d8e64b8773', expand=False)
    version('2018.12', sha256='1821d4b623ed449e0acb6df3ecbabd3944cffa98f96a5234b7a102a7c0853dc6', expand=False)
    version('5.3.1',   sha256='f0650ad2f9ca4ae3f3162d7204a32950bc794f37f322eb47b5ad9412454f998c', expand=False)
    version('5.3.0',   sha256='50eeaab24bfa2472bc6485fe8f0e612ed67e561eda1ff9fbf07b62c96443c1be', expand=False)
    version('5.2.0',   sha256='cb0d7a08b0e2cec4372033d3269979b4e72e2353ffd1444f57cb38bc9621219f', expand=False)
    version('5.1.0',   sha256='5f26ee92860d1dffdcd20910ff2cf75572c39d2892d365f4e867a611cca2af5b', expand=False)
    version('5.0.1',   sha256='23c676510bc87c95184ecaeb327c0b2c88007278e0d698622e2dd8fb14d9faa4', expand=False)
    version('5.0.0.1', sha256='18730808d863a5c194ab3f59dd395c1a63cbd769c9bfb1df65efe61ee62fc6d6', expand=False)
    version('5.0.0',   sha256='58a7117f89c40275114bf7e824a613a963da2b0fe63f2ec3c1175fea785b468e', expand=False)
    version('4.4.0',   sha256='2d30b91ed4d215b6b4a15162a3389e9057b15445a0c02da71bd7bd272e7b824e', expand=False)
    version('4.3.1',   sha256='e9b8f2645df6b1527ba56d61343162e0794acc3ee8dde2a6bba353719e2d878d', expand=False)
    version('4.3.0',   sha256='7c52e6e99aabb24a49880130615a48e685da444c3c14eb48d6a65f3313bf745c', expand=False)
    version('4.2.0',   sha256='beee286d24fb37dd6555281bba39b3deb5804baec509a9dc5c69185098cf661a', expand=False)
    version('4.1.1',   sha256='9413b1d3ca9498ba6f53913df9c43d685dd973440ff10b7fe0c45b1cbdcb582e', expand=False)
    version('4.1.0',   sha256='3b7e504ca0132fb555d1f10e174cae07007f1bc6898cad0f7d416a68aca01f45', expand=False)
    version('4.0.0',   sha256='ae312143952ca00e061a656c2080e0e4fd3532721282ba8e2978177cad71a5f0', expand=False)
    version('2.5.0',   sha256='e10abf459cde4a838bd6fc5ca03023c3401b81ad470627acde5a298d56715321', expand=False)
    version('2.4.1',   sha256='2de682c96edf8cca2852071a84ff860025fbe8c502218e1995acd5ab47e8c9ac', expand=False)
    version('2.4.0',   sha256='49d19834da06b1b82b6fa85bc647d2e78fa5957d0cbae3ccd6c695a541befa6b', expand=False)

    def install(self, spec, prefix):
        dir, anaconda_script = split(self.stage.archive_file)
        bash = which('bash')
        bash(anaconda_script, '-b', '-f', '-p', self.prefix)
