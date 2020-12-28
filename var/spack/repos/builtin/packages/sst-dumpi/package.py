# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#
# Author: Samuel Knight <sknigh@sandia.gov>
# Date: Feb 3, 2017
#
from spack.package import *


class SstDumpi(AutotoolsPackage):
    """The DUMPI package provides libraries to collect and read traces of MPI
    applications. Traces are created by linking an application with a library
    that uses the PMPI interface to intercept MPI calls. DUMPI records
    signatures of all MPI-1 and MPI-2 subroutine calls, return values, request
    information, and PAPI counters.
    """

    homepage = "http://sst.sandia.gov/about_dumpi.html"
    url      = "https://github.com/sstsimulator/sst-dumpi/archive/6.1.0.tar.gz"
    git      = "https://github.com/sstsimulator/sst-dumpi.git"

    version('master', branch='master')
    version('6.1.0', sha256='d4f6afcff5ba67fcc3a29f461afbb59855053840f5f320552a77b4e14c687bb6')

    depends_on('autoconf@1.68:', type='build')
    depends_on('automake@1.11.1:', type='build')
    depends_on('libtool@1.2.4:', type='build')
    depends_on('m4', type='build')
