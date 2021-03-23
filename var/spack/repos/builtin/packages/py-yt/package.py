# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class PyYt(PythonPackage):
    """Volumetric Data Analysis

       yt is a python package for analyzing and visualizing
       volumetric, multi-resolution data from astrophysical
       simulations, radio telescopes, and a burgeoning
       interdisciplinary community.
    """
    homepage = "http://yt-project.org"
    url      = "https://github.com/yt-project/yt/archive/yt-3.5.0.tar.gz"
    git      = "https://github.com/yt-project/yt.git"

    maintainers = ['qobilidop']

    version("develop", branch="master")
    version("develop-4.0", branch="yt-4.0")

    version('3.6.1', sha256='a1be3ea7e18729d3cd86e9234dc4731bf23200dff3344fa756fe173ea36cc747')
    version('3.6.0', sha256='4e3bab11766d5950477ba4d6c528a495e12cda1155227361b4579ac4ac0bf975')
    version('3.5.1', sha256='cdc0ecb153e737d74820581f311d1be7b6f1a7ee065ad69706470939db88b041')
    version('3.5.0', sha256='548598912adba72b782b7422d40d1d12a8c1a6cd064281a9a537fdb2a5af89fc')
    version('3.4.1', sha256='b9a73ade3726a8163fc992999c8c1010ca89473131901fe4d48b820ab2ced486')
    version('3.4.0', sha256='2120793a76864cf3165b2b7290ef719e358fa57501ee8721941e7cfc434cfb2b')
    version('3.3.5', sha256='2ebe4bbefd9f5367563ce4d7eb87d3f6ef0de1f97ed1c03106d9541e71b7e1ca')
    version('3.3.4', sha256='2842bab891cfbf3269a3c4bd8f22fef23c9a15a790ba48c6490730cb51ce9b0e')
    version('3.3.3', sha256='7b9244089e92b1d32cef791cd72760bb8c80b391eaec29672a5377c33f932d88')
    version('3.3.2', sha256='d323419ad3919e86d2af1738c846021fd7f5b5dc5c06059cdf3a2bc63226466a')
    version('3.3.1', sha256='7ac68d5e05e2b57fb3635f1027f3201094f3547d584e72ab55fedbfd3bc09a36')
    version('3.3.0', sha256='e6be799c0d9a83a06649f0d77a61ad9c23b94b34f94e16724e2b18f5c7513c33')
    version('3.2.3', sha256='96476d17e9ce35f0d4380b2ddb398fe729e39f1f3894602ff07e49844541e5ca')
    version('3.2.2', sha256='498ed77b3dae8c54929602d4931f3c3e0a3420a9b500cbd870f50b1e0efea8c3')

    variant("astropy", default=True, description="enable astropy support")
    variant("h5py", default=True, description="enable h5py support")
    variant("scipy", default=True, description="enable scipy support")
    variant("rockstar", default=False, description="enable rockstar support")

    depends_on("py-astropy@4.0.1:", type=('build', 'run'), when="+astropy")
    depends_on("py-cython@0.24:", type=('build', 'run'))
    depends_on("py-h5py@3.1:", type=('build', 'run'), when="+h5py")
    depends_on("py-ipython@1.0:", type=('build', 'run'))
    depends_on("py-ipython@:6.99", type=('build', 'run'), when="^python@:2.99")
    depends_on("py-matplotlib@1.5.3:", type=('build', 'run'))
    depends_on("py-matplotlib@:3.2.2", type=('build', 'run'), when="@:3.6.0")
    depends_on("py-numpy@1.10.4:", type=('build', 'run'))
    depends_on("py-scipy@1.5.0:", type=('build', 'run'), when="+scipy")
    depends_on("py-setuptools@19.6:", type=('build', 'run'))
    depends_on("py-sympy@1.0:", type=('build', 'run'))
    depends_on("rockstar@yt", type=('build', 'run'), when="+rockstar")
    depends_on("python@2.7.0:2.7.99,3.5:", type=('build', 'run'))

    @run_before('install')
    def prep_yt(self):
        if '+rockstar' in self.spec:
            with open('rockstar.cfg', 'w') as rockstar_cfg:
                rockstar_cfg.write(self.spec['rockstar'].prefix)

    @run_after('install')
    @on_package_attributes(run_tests=True)
    def check_install(self):
        # The Python interpreter path can be too long for this
        # yt = Executable(join_path(prefix.bin, "yt"))
        # yt("--help")
        python(join_path(self.prefix.bin, "yt"), "--help")
