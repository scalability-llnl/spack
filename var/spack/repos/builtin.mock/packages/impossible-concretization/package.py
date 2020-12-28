# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class ImpossibleConcretization(Package):
    """Package that should be impossible to concretize due to a conflict
    with target ranges. See Issue 19981.
    """

    homepage = "http://www.example.com"
    url = "http://www.example.com/example-1.0.tar.gz"

    version(1.0, 'foobarbaz')

    conflicts('target=x86_64:')
