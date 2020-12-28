# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyTorchaudio(PythonPackage):
    """The aim of torchaudio is to apply PyTorch to the audio
    domain. By supporting PyTorch, torchaudio follows the same
    philosophy of providing strong GPU acceleration, having a focus on
    trainable features through the autograd system, and having
    consistent style (tensor names and dimension names). Therefore, it
    is primarily a machine learning library and not a general signal
    processing library. The benefits of Pytorch is be seen in
    torchaudio through having all the computations be through Pytorch
    operations which makes it easy to use and feel like a natural
    extension."""

    homepage = "https://github.com/pytorch/audio"
    url      = "https://github.com/pytorch/audio/archive/v0.4.0.tar.gz"

    version('0.4.0', sha256='9361312319b1ab880fc348ea82b024053bca6faf477ef6a9232a5b805742dc66')

    depends_on('py-setuptools', type='build')
    depends_on('sox@14.3.2:')
    depends_on('py-torch@1.2.0:', type=('build', 'run'))
