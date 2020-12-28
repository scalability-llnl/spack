# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Htop(AutotoolsPackage):
    """htop is an interactive text-mode process viewer for Unix systems."""

    homepage = "https://github.com/hishamhm/htop"
    url      = "https://hisham.hm/htop/releases/2.0.2/htop-2.0.2.tar.gz"
    list_url = "https://hisham.hm/htop/releases"
    list_depth = 1

    version('2.2.0', sha256='d9d6826f10ce3887950d709b53ee1d8c1849a70fa38e91d5896ad8cbc6ba3c57')
    version('2.0.2', sha256='179be9dccb80cee0c5e1a1f58c8f72ce7b2328ede30fb71dcdf336539be2f487')

    depends_on('ncurses')
    depends_on('python+pythoncmd', type='build')

    def configure_args(self):
        return ['--enable-shared']
