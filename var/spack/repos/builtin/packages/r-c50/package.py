# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class RC50(RPackage):
    """C5.0 decision trees and rule-based models for pattern recognition."""

    homepage = "https://cloud.r-project.org/package=C50"
    url      = "https://cloud.r-project.org/src/contrib/C50_0.1.0-24.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/C50"

    version('0.1.2', sha256='8f459856e0309274bee24462b7145db4eba1d71031c236db39000a5375bdfaba')
    version('0.1.1', sha256='03bc1fc2f64bcd5c680568a24902deafab1965074a66f8802bc4cd0335bd01df')
    version('0.1.0-24', sha256='617ee8ae617a075213414c07739ce92d9e6927783d01588fd0e2315157065e9d')

    depends_on('r@2.10.0:', type=('build', 'run'))
    depends_on('r-partykit', type=('build', 'run'))
    depends_on('r-cubist@0.2.1:', type=('build', 'run'))
