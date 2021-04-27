# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyMemprof(PythonPackage):
    """memprof logs and plots the memory usage of all the
    variables during the execution of the decorated methods."""

    homepage = "http://jmdana.github.io/memprof/"
    pypi = "memprof/memprof-0.3.6.tar.gz"

    version('0.3.6', sha256='a8376ce476bf82a5eb465d1a30b8ffc86cc55b0b6de7aa4cdeccb4c99586d967')

    depends_on('py-setuptools', type='build')
    depends_on('py-cython',     type='build')
    depends_on('py-argparse', when='^python@:2.6', type=('build', 'run'))
    depends_on('py-matplotlib', type=('build', 'run'))
