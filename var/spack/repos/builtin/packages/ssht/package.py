# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Ssht(CMakePackage):
    """ssht: Spin spherical harmonic transforms

    The SSHT code provides functionality to perform fast and exact
    spin spherical harmonic transforms based on the sampling theorem
    on the sphere derived in our paper: A novel sampling theorem on
    the sphere <http://dx.doi.org/10.1109/TSP.2011.2166394>.
    """

    homepage = "https://astro-informatics.github.io/ssht/"
    url      = "https://github.com/astro-informatics/ssht/archive/v1.3.4.tar.gz"
    git      = "https://github.com/astro-informatics/ssht.git"

    maintainers = ['eschnett']

    version('1.3.7', sha256='947c11b104734acb124171ff5115d14279b4d09bc297ac989204633919df422e')
    version('1.3.6', sha256='db652e0f550229a630643bbf4bdb270def25c158be5ccdcf594a24fd8054430d')
    version('1.3.5', sha256='2f71690cbd00f4969d7377e586022397bfb8efb107f7b13bf849a65e61362350')
    version('1.3.4', sha256='dfcceca9a4ffe8973a45e213e8d5331dcee6a504a42601f50fdfa4fd022cce7b')
    version('1.3.3', sha256='1f3b89e29d89fa79170b9979046a55c81b588d9dd563fd36f37887495b71dd28')
    version('1.3.2', sha256='6cb3b6f94fb90dff45ba59da30a8ccd9667d8e319bed437f19d2287f59e35dd1')
    version('1.3.0', sha256='9e2c220a70d662714ff601a121b674c8423866058279e000cbbee532d31dd3c9')
    # version('1.2b1', commit='7378ce8853897cbd1b08adebf7ec088c1e40f860')

    depends_on('fftw @3.0.0:')
