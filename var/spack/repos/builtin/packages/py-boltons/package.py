# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBoltons(PythonPackage):
    """When they're not builtins, they're boltons.

    Functionality that should be in the standard library. Like builtins,
    but Boltons.

    Otherwise known as, "everyone's util.py," but cleaned up and tested.
    """
    homepage = "https://boltons.readthedocs.io/"
    url = "https://pypi.io/packages/source/b/boltons/boltons-16.5.1.tar.gz"

    version('16.5.1', sha256='fcded58596fa79bd1ada4488178e79fd11c7cb449f29ff9a6532411fb2db19b7')

    depends_on('py-setuptools', type='build')
