# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RSelectr(RPackage):
    """Translates a CSS3 selector into an equivalent XPath expression. This
       allows us to use CSS selectors when working with the XML package as it
       can only evaluate XPath expressions. Also provided are convenience
       functions useful for using CSS selectors on XML nodes. This package
       is a port of the Python package 'cssselect'
       (<https://pythonhosted.org/cssselect/>)."""

    homepage = "https://sjp.co.nz/projects/selectr"
    url      = "https://cloud.r-project.org/src/contrib/selectr_0.3-1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/selectr"

    version('0.4-1', sha256='8bd42f167629344e485e586f9b05fed342746132489079084d82133d7b3ee2ca')
    version('0.4-0', sha256='40cd51bfe499954b300742c49f92167a68964b974268a7f47ca8864f32020ece')
    version('0.3-1', sha256='db4f7ceea4b522a54c3ae7709787b0b7fcf389c5d945c5a278e3625388218949')

    depends_on('r@3.0:', type=('build', 'run'))
    depends_on('r-stringr', type=('build', 'run'))
    depends_on('r-r6', when='@0.4-0:', type=('build', 'run'))
