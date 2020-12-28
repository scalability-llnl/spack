# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Chapel(AutotoolsPackage):
    """Chapel is a modern programming language that is parallel, productive,
       portable, scalable and open-source."""

    homepage = "https://chapel-lang.org/"
    url      = "https://github.com/chapel-lang/chapel/releases/download/1.20.0/chapel-1.20.0.tar.gz"

    version('1.20.0', sha256='08bc86df13e4ad56d0447f52628b0f8e36b0476db4e19a90eeb2bd5f260baece')
    version('1.19.0', sha256='c2b68a20d87cc382c2f73dd1ecc6a4f42fb2f590b0b10fbc577382dd35c9e9bd')
    version('1.18.0', sha256='68471e1f398b074edcc28cae0be26a481078adc3edea4df663f01c6bd3b6ae0d')
