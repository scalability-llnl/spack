# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class ImportResourcesMissingFile(Package):
    """Simple package that is used to test import_resources.
    """

    homepage = "http://www.example.com"
    url      = "http://www.example.com/a-1.0.tar.gz"

    version('2.0', 'hash2')
    version('1.0', 'hash1')

    import_resources("nonexistent.json")
