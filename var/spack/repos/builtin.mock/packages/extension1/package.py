# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os.path

from spack.package import *


class Extension1(Package):
    """A package which extends another package"""

    homepage = "http://www.example.com"
    url      = "http://www.example.com/extension1-1.0.tar.gz"

    extends('extendee')

    version('1.0', 'hash-extension1-1.0')
    version('2.0', 'hash-extension1-2.0')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        with open(os.path.join(prefix.bin, 'extension1'), 'w+') as fout:
            fout.write(str(spec.version))
