# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RVgam(RPackage):
    """An implementation of about 6 major classes of statistical regression
    models."""

    homepage = "https://cloud.r-project.org/package=VGAM"
    url      = "https://cloud.r-project.org/src/contrib/VGAM_1.0-4.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/VGAM"

    version('1.1-1', sha256='de192bd65a7e8818728008de8e60e6dd3b61a13616c887a43e0ccc8147c7da52')
    version('1.0-6', sha256='121820a167411e847b41bdcb0028b55842d0ccc0c3471755c67449837e0fe3b9')
    version('1.0-4', sha256='e581985f78ef8b866d0e810b2727061bb9c9bc177b2c9090aebb3a35ae87a964')
    version('1.0-3', sha256='23bb6690ae15e9ede3198ef55d5d3236c279aa8fa6bd4f7350242379d9d72673')
    version('1.0-2', sha256='03561bf484f97b616b1979132c759c5faa69c5d5a4cfd7aea2ea6d3612ac0961')
    version('1.0-1', sha256='c066864e406fcee23f383a28299dba3cf83356e5b68df16324885afac87a05ea')
    version('1.0-0', sha256='6acdd7db49c0987c565870afe593160ceba72a6ca4a84e6da3cf6f74d1fa02e1')

    depends_on('r@3.0.0:', when='@:1.0-1', type=('build', 'run'))
    depends_on('r@3.1.0:', when='@1.0-2:1.0-3', type=('build', 'run'))
    depends_on('r@3.4.0:', when='@1.0-4:', type=('build', 'run'))
