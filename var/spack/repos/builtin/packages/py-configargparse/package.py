# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyConfigargparse(PythonPackage):
    """Applications with more than a handful of user-settable
    options are best configured through a combination of
    command line args, config files, hard-coded defaults, and
    in some cases, environment variables.

    Python's command line parsing modules such as argparse have
    very limited support for config files and environment
    variables, so this module extends argparse to add these
    features."""

    homepage = "https://github.com/bw2/ConfigArgParse"
    url      = "https://github.com/bw2/ConfigArgParse/archive/1.2.3.tar.gz"

    version('1.2.3', sha256='0f1144a204e3b896d6ac900e151c1d13bde3103d6b7d541e3bb57514a94083bf')

    depends_on('python@2.2:2.999,3.5:', type=('build', 'run'))
