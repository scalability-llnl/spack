# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Motioncor2(Package):
    """MotionCor2 is a multi-GPU program that corrects beam-induced sample
    motion recorded on dose fractionated movie stacks. It implements a robust
    iterative alignment algorithm that delivers precise measurement and
    correction of both global and non-uniform local motions at
    single pixel level, suitable for both single-particle and
    tomographic images. MotionCor2 is sufficiently fast
    to keep up with automated data collection."""

    homepage = "http://msg.ucsf.edu/em/software"
    url      = "http://msg.ucsf.edu/MotionCor2/MotionCor2-1.1.0.zip"

    version('1.1.0',
            '6e37e7ed63a9f0aab5d794b2604d5ba79333960bb9440a1a218630b03dbeaeac')
    version('1.0.5',
            '4efa55af25644bcff1ca7882419267b8c094c9cc6155b37d2c204b154c56f5a8',
            url='http://msg.ucsf.edu/MotionCor2/MotionCor2-1.0.5.tar.gz')
    version('1.0.4',
            'c75738160ac18d3f27c33677e78e63313d8ec2b023b5a46173428c3fa0451a94',
            url='http://msg.ucsf.edu/MotionCor2/MotionCor2-1.0.4.tar.gz')

    depends_on('cuda@8.0:8.99', type='run')
    # libtiff.so.3 is required
    depends_on('libtiff@3.0:3.99', type='run')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('MotionCor2_*', prefix.bin)
        with working_dir(prefix.bin):
            symlink('MotionCor2_{0}'.format(spec.version), 'MotionCor2')
