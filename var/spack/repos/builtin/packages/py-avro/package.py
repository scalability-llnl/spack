# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAvro(PythonPackage):
    """Avro is a serialization and RPC framework."""

    homepage = "http://avro.apache.org/docs/current/"
    url      = "https://pypi.io/packages/source/a/avro/avro-1.8.2.tar.gz"

    version('1.8.2', sha256='8f9ee40830b70b5fb52a419711c9c4ad0336443a6fba7335060805f961b04b59')

    depends_on('py-setuptools', type='build')
