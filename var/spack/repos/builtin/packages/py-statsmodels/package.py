# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import glob


class PyStatsmodels(PythonPackage):
    """Statistical computations and models for use with SciPy"""

    homepage = "http://www.statsmodels.org"
    pypi = "statsmodels/statsmodels-0.8.0.tar.gz"

    version('0.12.2', sha256='8ad7a7ae7cdd929095684118e3b05836c0ccb08b6a01fe984159475d174a1b10')
    version('0.12.1', sha256='a271b4ccec190148dccda25f0cbdcbf871f408fc1394a10a7dc1af4a62b91c8e')
    version('0.10.2', sha256='9cd2194c6642a8754e85f9a6e6912cdf996bebf6ff715d3cc67f65dadfd37cc9')
    version('0.10.1', sha256='320659a80f916c2edf9dfbe83512d9004bb562b72eedb7d9374562038697fa10')
    version('0.8.0', sha256='26431ab706fbae896db7870a0892743bfbb9f5c83231644692166a31d2d86048')

    variant('plotting', default=False, description='With matplotlib')

    depends_on('python@:3.6',         when='@:0.8.0',  type=('build', 'link', 'run'))
    depends_on('python@2.7:2.8,3.4:', when='@0.10.1:', type=('build', 'link', 'run'))
    depends_on('python@3.6:',         when='@0.12.1:', type=('build', 'link', 'run'))

    # according to http://www.statsmodels.org/dev/install.html earlier versions
    # might work.
    depends_on('py-setuptools@0.6c5:', type='build')
    depends_on('py-cython@0.29:', type='build')

    # patsy@0.5.1 works around a Python change
    #    https://github.com/statsmodels/statsmodels/issues/5343 and
    #    https://github.com/pydata/patsy/pull/131

    depends_on('py-numpy@1.7.0:',      type=('build', 'link', 'run'), when='@0.8.0:')
    depends_on('py-numpy@1.11.0:',     type=('build', 'link', 'run'), when='@0.10.1:')
    depends_on('py-numpy@1.15.0:',     type=('build', 'link', 'run'), when='@0.12.1:')
    depends_on('py-pandas@0.12:',      type=('build', 'run'), when='@0.8.0:')
    depends_on('py-pandas@0.19:',      type=('build', 'run'), when='@0.10.1:')
    depends_on('py-pandas@0.21:',      type=('build', 'run'), when='@0.12.1:')
    depends_on('py-patsy@0.2.1:',      type=('build', 'run'), when='@0.8.0:')
    depends_on('py-patsy@0.4.0:',      type=('build', 'run'), when='@0.10.1:')
    depends_on('py-patsy@0.5.0:',      type=('build', 'run'), when='@0.12.1:')
    depends_on('py-scipy@0.11:',       type=('build', 'run'), when='@0.8.0:')
    depends_on('py-scipy@0.18:',       type=('build', 'run'), when='@0.10.1:')
    depends_on('py-scipy@1.1:',        type=('build', 'run'), when='@0.12.1:')
    depends_on('py-matplotlib@1.3:',   type=('build', 'run'), when='@0.8.0 +plotting')

    depends_on('py-pytest', type='test')

    @run_after('build')
    @on_package_attributes(run_tests=True)
    def build_test(self):
        dirs = glob.glob("build/lib*")  # There can be only one...
        with working_dir(dirs[0]):
            pytest = which('pytest')
            pytest('statsmodels')
