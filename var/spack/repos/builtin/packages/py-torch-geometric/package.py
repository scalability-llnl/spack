# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PyTorchGeometric(PythonPackage):
    """PyTorch Geometric (PyG) is a geometric deep learning extension
    library for PyTorch.  It consists of various methods for deep
    learning on graphs and other irregular structures, also known as
    geometric deep learning, from a variety of published papers. In
    addition, it consists of an easy-to-use mini-batch loader for many
    small and single giant graphs, multi gpu-support, a large number
    of common benchmark datasets (based on simple interfaces to create
    your own), and helpful transforms, both for learning on arbitrary
    graphs as well as on 3D meshes or point clouds."""

    homepage = "https://github.com/rusty1s/pytorch_geometric"
    url      = "https://github.com/rusty1s/pytorch_geometric/archive/1.6.0.tar.gz"

    version('1.6.3', sha256='1907c0f5eb7ab8f6f79a7e43703579b39b514501dd956ed0fc3d33210bcbb4c2')
    version('1.6.0', sha256='7d5231cdcc2ebd4444f406cbf1537eb49bf90ab6f446eaf1b7af5cdbe105f3c9')

    variant('cuda', default=False, description="Enable CUDA support")

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-pytest-runner', type='build')
    depends_on('py-torch', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-tqdm', type=('build', 'run'))
    depends_on('py-scipy', type=('build', 'run'))
    depends_on('py-networkx', type=('build', 'run'))
    depends_on('py-scikit-learn', type=('build', 'run'))
    depends_on('py-numba', type=('build', 'run'))
    depends_on('py-python-louvain', type=('build', 'run'), when='@1.6.2:')
    depends_on('py-requests', type=('build', 'run'))
    depends_on('py-pandas', type=('build', 'run'))
    depends_on('py-rdflib', type=('build', 'run'))
    depends_on('py-googledrivedownloader', type=('build', 'run'))
    depends_on('py-h5py~mpi', type=('build', 'run'))
    depends_on('py-ase', type=('build', 'run'))
    depends_on('py-jinja2', type=('build', 'run'))
    depends_on('py-torch-sparse+cuda', when='+cuda', type=('build', 'run'))
    depends_on('py-torch-scatter+cuda', when='+cuda', type=('build', 'run'))
    depends_on('py-torch-cluster+cuda', when='+cuda', type=('build', 'run'))
    depends_on('py-torch-spline-conv+cuda', when='+cuda', type=('build', 'run'))
    depends_on('py-torch-sparse~cuda', when='~cuda', type=('build', 'run'))
    depends_on('py-torch-scatter~cuda', when='~cuda', type=('build', 'run'))
    depends_on('py-torch-cluster~cuda', when='~cuda', type=('build', 'run'))
    depends_on('py-torch-spline-conv~cuda', when='~cuda', type=('build', 'run'))

    def setup_build_environment(self, env):
        if '+cuda' in self.spec:
            cuda_arches = list(
                self.spec['py-torch'].variants['cuda_arch'].value)
            for i, x in enumerate(cuda_arches):
                cuda_arches[i] = '{0}.{1}'.format(x[0:-1], x[-1])
            env.set('TORCH_CUDA_ARCH_LIST', str.join(' ', cuda_arches))

            env.set('FORCE_CUDA', '1')
            env.set('CUDA_HOME', self.spec['cuda'].prefix)
        else:
            env.set('FORCE_CUDA', '0')
