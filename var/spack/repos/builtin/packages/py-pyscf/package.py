# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPyscf(PythonPackage):
    """PySCF is a collection of electronic structure programs powered
    by Python."""

    homepage = "https://sunqm.github.io/pyscf/"
    git      = "https://github.com/pyscf/pyscf"

    maintainers = ['naromero77']

    version('1.7.5', tag='v1.7.5')
    version('1.7.3', tag='v1.7.3')

    # dependencies
    depends_on('cmake@2.8:', type='build')
    depends_on('python@2.6:', type=('build', 'run'))
    depends_on('py-numpy@1.8.0:', type=('build', 'run'))
    depends_on('py-scipy@0.12:', type=('build', 'run'))
    depends_on('py-h5py@2.3.0:', type=('build', 'run'))
    depends_on('blas')
    depends_on('libcint+coulomb_erf+f12')
    depends_on('libxc')
    depends_on('xcfun')
    depends_on('xcfun@2.0.0a2', when='@:1.7.4')

    def setup_build_environment(self, env):
        # Tell PSCF where supporting libraries are located."
        spec = self.spec

        pyscf_search_dir = []
        pyscf_search_dir.append(spec['blas'].prefix)
        pyscf_search_dir.append(spec['libcint'].prefix)
        pyscf_search_dir.append(spec['libcint'].prefix.lib64)
        pyscf_search_dir.append(spec['libxc'].prefix)
        pyscf_search_dir.append(spec['xcfun'].prefix)
        pyscf_search_dir.append(spec['xcfun'].prefix.include.XCFun)

        env.set('PYSCF_INC_DIR', ":".join(pyscf_search_dir))
