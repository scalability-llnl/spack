##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *
from distutils.dir_util import copy_tree


class Cudnn(Package):
    """NVIDIA cuDNN is a GPU-accelerated library of primitives for deep
    neural networks"""

    homepage = "https://developer.nvidia.com/cudnn"

    version('7.0', '6189e05077dbce0bd07059b20306a836',
            url='http://developer.download.nvidia.com/compute/redist/cudnn/v7.0.3/cudnn-9.0-linux-x64-v7.tgz',
            when='^cuda@9')
    version('7.0', '8548a35c8d51c3f8d44b46a79026d18b',
            url='http://developer.download.nvidia.com/compute/redist/cudnn/v7.0.3/cudnn-8.0-linux-x64-v7.tgz',
            when='^cuda@8')
    version('6.0', 'a08ca487f88774e39eb6b0ef6507451d',
            url='http://developer.download.nvidia.com/compute/redist/cudnn/v6.0/cudnn-8.0-linux-x64-v6.0.tgz',
            when='^cuda@8')
    version('6.0', '388b32257ad34a9d954e51ea920500e4',
            url='http://developer.download.nvidia.com/compute/redist/cudnn/v6.0/cudnn-7.5-linux-x64-v6.0.tgz',
            when='^cuda@7.5')
    version('5.1', '406f4ac7f7ee8aa9e41304c143461a69',
            url='http://developer.download.nvidia.com/compute/redist/cudnn/v5.1/cudnn-8.0-linux-x64-v5.1.tgz',
            when='^cuda@8')
    version('5.1', '114ae87d1b9e96fff5e1353907df7a14',
            url='http://developer.download.nvidia.com/compute/redist/cudnn/v5.1/cudnn-7.5-linux-x64-v5.1.tgz',
            when='^cuda@7.5')

    depends_on('cuda@7.5:', type='run')

    def install(self, spec, prefix):
        copy_tree('.', prefix)
