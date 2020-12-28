# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMaestrowf(PythonPackage):
    """A general purpose workflow conductor for running multi-step
       simulation studies."""

    homepage = "https://github.com/LLNL/maestrowf/"
    url      = "https://pypi.io/packages/source/m/maestrowf/maestrowf-1.1.8.tar.gz"
    git      = "https://github.com/LLNL/maestrowf/"

    maintainers = ['FrankD412']

    # git branches
    version('develop', branch='develop')
    version('master',  branch='master')

    # Pre-release candidates
    version('1.1.7dev0', sha256='bcef838f13da396dd33cc7f503655de7a8f16ee5fe7b1e2a553044334a03f1f0')

    # pypi releases
    version('1.1.8', sha256='fa8f8eb8dd3adfb9646d7b0dfd498a00423d2131adbc8dbc8016c4159b2ec1d5', preferred=True)
    version('1.1.7', sha256='ff1b6696f30254b105fcadd297ad437c0c666ebc70124b231a713b89f47f4e94')
    version('1.1.7dev0', sha256='bcef838f13da396dd33cc7f503655de7a8f16ee5fe7b1e2a553044334a03f1f0', url="https://pypi.io/packages/source/m/maestrowf/maestrowf-1.1.7.dev0.tar.gz")
    version('1.1.6', sha256='9812e67d9bd83c452cc99d82fbceb3017b5e36dafdf52eda939748bad4a88756')
    version('1.1.4', sha256='6603b93494e8e9d939a4ab40ecdfe7923a85960a8a8bddea4734e230d8144016')
    version('1.1.3', sha256='9812e67d9bd83c452cc99d82fbceb3017b5e36dafdf52eda939748bad4a88756')
    version('1.1.2', sha256='6998ba2c6ee4ef205c6d47d98cf35d5eaa184e1e859cc41b4120e2aa12c06df3')
    version('1.1.1', sha256='689ed42ba1fb214db0594756ff6015e466470103f726a5e5bf4d21c1086ad2b1')
    version('1.1.0', sha256='1bfec546831f2ef577d7823bb50dcd12622644dad0d3d761998eafd0905b6977')
    version('1.0.1', sha256='dd42ffeac1f0492a576c630b37e5d3593273e59664407f2ebf78d49322d37146')

    depends_on('python@2.7:2.8,3.5:',  type=('build', 'run'))
    depends_on('py-setuptools',        type='build')
    depends_on('py-pyyaml@4.2b1:',     type=('build', 'run'))
    depends_on('py-six',               type=('build', 'run'))
    depends_on('py-enum34',            type=('build', 'run'), when='^python@:3.3')
    depends_on('py-enum34',            type=('build', 'run'), when='@:1.1.3')
    depends_on('py-tabulate',          type=('build', 'run'), when='@1.1.0:')
    depends_on('py-filelock',          type=('build', 'run'), when='@1.1.0:')
    depends_on('py-coloredlogs',       type=('build', 'run'), when='@1.1.7:')
    depends_on('py-chainmap',          type=('build', 'run'), when='@1.1.7: ^python@:2')
    depends_on('py-dill',              type=('build', 'run'), when='@1.1.7:')
    depends_on('py-jsonschema@3.2.0:', type=('build', 'run'), when='@1.1.7:')
