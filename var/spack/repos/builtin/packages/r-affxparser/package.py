# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RAffxparser(RPackage):
    """Affymetrix File Parsing SDK.

       Package for parsing Affymetrix files (CDF, CEL, CHP, BPMAP, BAR). It
       provides methods for fast and memory efficient parsing of Affymetrix
       files using the Affymetrix' Fusion SDK. Both ASCII- and binary-based
       files are supported. Currently, there are methods for reading chip
       definition file (CDF) and a cell intensity file (CEL). These files can
       be read either in full or in part. For example, probe signals from a few
       probesets can be extracted very quickly from a set of CEL files into a
       convenient list structure."""

    homepage = "https://bioconductor.org/packages/affxparser"
    git      = "https://git.bioconductor.org/packages/affxparser.git"

    version('1.56.0', commit='20d27701ad2bdfacf34d857bb8ecb4f505b4d056')
    version('1.54.0', commit='dce83d23599a964086a84ced4afd13fc43e7cd4f')
    version('1.52.0', commit='8e0c4b89ee1cb4ff95f58a5dd947249dc718bc58')
    version('1.50.0', commit='01ef641727eadc2cc17b5dbb0b1432364436e3d5')
    version('1.48.0', commit='2461ea88f310b59c4a9a997a4b3dadedbd65a4aa')

    depends_on('r@2.14.0:', type=('build', 'run'))
