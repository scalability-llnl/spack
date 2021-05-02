# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Indent(AutotoolsPackage):
    """A tool to make code easier to read."""

    homepage = "https://www.gnu.org/software/indent"
    url      = "https://ftp.gnu.org/gnu/indent/indent-2.2.11.tar.gz"

    version('2.2.12', sha256='e77d68c0211515459b8812118d606812e300097cfac0b4e9fb3472664263bb8b')
    version('2.2.11', sha256='aaff60ce4d255efb985f0eb78cca4d1ad766c6e051666073050656b6753a0893')
    version('2.2.10', sha256='8a9b41be5bfcab5d8c1be74204b10ae78789fc3deabea0775fdced8677292639')

    depends_on('texinfo')
