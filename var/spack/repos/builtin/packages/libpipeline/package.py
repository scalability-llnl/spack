# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libpipeline(AutotoolsPackage):
    """libpipeline is a C library for manipulating pipelines of subprocesses
    in a flexible and convenient way."""

    homepage = "http://libpipeline.nongnu.org/"
    url      = "http://git.savannah.nongnu.org/cgit/libpipeline.git/snapshot/libpipeline-1.4.2.tar.gz"

    version('1.4.2', sha256='ac8b103b281ff63129c4fa6a8cc40bb5863e3a4266343d6e3bb5788de1ede488')

    depends_on('pkgconfig', type='build')
    depends_on('check', type='test')
