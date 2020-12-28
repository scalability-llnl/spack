# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Turnserver(AutotoolsPackage):
    """coturn TURN server project."""

    homepage = "https://coturn.net/turnserver"
    url      = "https://coturn.net/turnserver/v4.5.1.3/turnserver-4.5.1.3.tar.gz"

    version('4.5.1.3', sha256='408bf7fde455d641bb2a23ba2df992ea0ae87b328de74e66e167ef58d8e9713a')

    depends_on('libevent')
