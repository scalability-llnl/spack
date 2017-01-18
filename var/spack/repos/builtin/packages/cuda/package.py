##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
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
from glob import glob
import os


class Cuda(Package):
    """CUDA is a parallel computing platform and programming model invented
    by NVIDIA. It enables dramatic increases in computing performance by
    harnessing the power of the graphics processing unit (GPU).

    Note: NVIDIA does not provide a download URL for CUDA so you will
    need to download it yourself. Go to
    https://developer.nvidia.com/cuda-downloads and select your Operating
    System, Architecture, Distribution, and Version.  For the Installer
    Type, select runfile and click Download. Spack will search your
    current directory for this file. Alternatively, add this file to a
    mirror so that Spack can find it. For instructions on how to set up a
    mirror, see http://spack.readthedocs.io/en/latest/mirrors.html.

    Note: This package does not currently install the drivers necessary
    to run CUDA. These will need to be installed manually. See:
    http://docs.nvidia.com/cuda/cuda-getting-started-guide-for-linux for
    details.

    """

    homepage = "http://www.nvidia.com/object/cuda_home_new.html"

    version('8.0.44', '6dca912f9b7e2b7569b0074a41713640', expand=False,
            url="file://%s/cuda_8.0.44_linux.run"    % os.getcwd())
    version('7.5.18', '4b3bcecf0dfc35928a0898793cf3e4c6', expand=False,
            url="file://%s/cuda_7.5.18_linux.run"    % os.getcwd())
    version('6.5.14', '90b1b8f77313600cc294d9271741f4da', expand=False,
            url="file://%s/cuda_6.5.14_linux_64.run" % os.getcwd())

    def install(self, spec, prefix):
        runfile = glob(os.path.join(self.stage.path, 'cuda*.run'))[0]
        chmod = which('chmod')
        chmod('+x', runfile)
        runfile = which(runfile)

        # Note: NVIDIA does not officially support many newer versions of
        # compilers.  For example, on CentOS 6, you must use GCC 4.4.7 or
        # older. See:
        # http://docs.nvidia.com/cuda/cuda-installation-guide-linux/#system-requirements
        # for details.

        runfile(
            '--silent',   # disable interactive prompts
            '--verbose',  # create verbose log file
            '--toolkit',  # install CUDA Toolkit
            '--toolkitpath=%s' % prefix
        )
