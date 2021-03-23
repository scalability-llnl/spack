# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PyTorchvision(PythonPackage):
    """The torchvision package consists of popular datasets, model
    architectures, and common image transformations for computer vision."""

    homepage = "https://github.com/pytorch/vision"
    url      = "https://github.com/pytorch/vision/archive/v0.8.2.tar.gz"
    git      = "https://github.com/pytorch/vision.git"

    maintainers = ['adamjstewart']

    version('master', branch='master')
    version('0.9.0', sha256='9351ed92aded632f8c7f59dfadac13c191a834babe682f5785ea47e6fcf6b472')
    version('0.8.2', sha256='9a866c3c8feb23b3221ce261e6153fc65a98ce9ceaa71ccad017016945c178bf')
    version('0.8.1', sha256='c46734c679c99f93e5c06654f4295a05a6afe6c00a35ebd26a2cce507ae1ccbd')
    version('0.8.0', sha256='b5f040faffbfc7bac8d4687d8665bd1196937334589b3fb5fcf15bb69ca25391')
    version('0.7.0', sha256='fa0a6f44a50451115d1499b3f2aa597e0092a07afce1068750260fa7dd2c85cb')
    version('0.6.1', sha256='8173680a976c833640ecbd0d7e6f0a11047bf8833433e2147180efc905e48656')
    version('0.6.0', sha256='02de11b3abe6882de4032ce86dab9c7794cbc84369b44d04e667486580f0f1f7')
    version('0.5.0', sha256='eb9afc93df3d174d975ee0914057a9522f5272310b4d56c150b955c287a4d74d')
    version('0.4.2', sha256='1184a27eab85c9e784bacc6f9d6fec99e168ab4eda6047ef9f709e7fdb22d8f9')
    version('0.4.1', sha256='053689351272b3bd2ac3e6ba51efd284de0e4ca4a301f54674b949f1e62b7176')
    version('0.4.0', sha256='c270d74e568bad4559fed4544f6dd1e22e2eb1c60b088e04a5bd5787c4150589')
    version('0.3.0', sha256='c205f0618c268c6ed2f8abb869ef6eb83e5339c1336c243ad321a2f2a85195f0')

    # https://github.com/pytorch/vision#image-backend
    variant('backend', default='pil', description='Image backend',
            values=('pil', 'accimage', 'png', 'jpeg'), multi=False)

    # https://github.com/pytorch/vision#installation
    depends_on('python@3.6:', when='@0.7:', type=('build', 'link', 'run'))
    depends_on('python@3.5:', when='@0.6.0:0.6.999', type=('build', 'link', 'run'))
    depends_on('python@2.7:2.8,3.5:3.8', when='@0.5.0', type=('build', 'link', 'run'))
    depends_on('python@2.7:2.8,3.5:3.7', when='@:0.4', type=('build', 'link', 'run'))

    depends_on('py-setuptools', type='build')
    depends_on('ninja', type='build')
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-six', when='@:0.5', type=('build', 'run'))

    # https://github.com/pytorch/vision#installation
    depends_on('py-torch@master', when='@master', type=('build', 'link', 'run'))
    depends_on('py-torch@1.8.0', when='@0.9.0', type=('build', 'link', 'run'))
    depends_on('py-torch@1.7.1', when='@0.8.2', type=('build', 'link', 'run'))
    depends_on('py-torch@1.7.0', when='@0.8.1', type=('build', 'link', 'run'))
    depends_on('py-torch@1.7.0', when='@0.8.0', type=('build', 'link', 'run'))
    depends_on('py-torch@1.6.0', when='@0.7.0', type=('build', 'link', 'run'))
    depends_on('py-torch@1.5.1', when='@0.6.1', type=('build', 'link', 'run'))
    depends_on('py-torch@1.5.0', when='@0.6.0', type=('build', 'link', 'run'))
    depends_on('py-torch@1.4.1', when='@0.5.0', type=('build', 'link', 'run'))
    depends_on('py-torch@1.3.1', when='@0.4.2', type=('build', 'link', 'run'))
    depends_on('py-torch@1.3.0', when='@0.4.1', type=('build', 'link', 'run'))
    depends_on('py-torch@1.2.0', when='@0.4.0', type=('build', 'link', 'run'))
    depends_on('py-torch@1.1.0', when='@0.3.0', type=('build', 'link', 'run'))
    depends_on('py-torch@:1.0.1', when='@0.2.2', type=('build', 'link', 'run'))

    # https://github.com/pytorch/vision/issues/1712
    depends_on('pil@4.1.1:6', when='@:0.4 backend=pil', type=('build', 'run'))
    depends_on('pil@4.1.1:',  when='@0.5: backend=pil', type=('build', 'run'))
    depends_on('py-accimage', when='backend=accimage', type=('build', 'run'))
    depends_on('libpng', when='backend=png')
    depends_on('jpeg', when='backend=jpeg')

    # Many of the datasets require additional dependencies to use.
    # These can be installed after the fact.

    depends_on('ffmpeg@3.1:', when='@0.4.2:')

    conflicts('backend=png', when='@:0.7')
    conflicts('backend=jpeg', when='@:0.7')

    def setup_build_environment(self, env):
        include = []
        library = []
        for dep in self.spec.dependencies(deptype='link'):
            query = self.spec[dep.name]
            include.extend(query.headers.directories)
            library.extend(query.libs.directories)

        # README says to use TORCHVISION_INCLUDE and TORCHVISION_LIBRARY,
        # but these do not work for older releases. Build uses a mix of
        # Spack's compiler wrapper and the actual compiler, so this is
        # needed to get parts of the build working.
        # See https://github.com/pytorch/vision/issues/2591
        env.set('TORCHVISION_INCLUDE', ':'.join(include))
        env.set('TORCHVISION_LIBRARY', ':'.join(library))
        env.set('CPATH', ':'.join(include))
        env.set('LIBRARY_PATH', ':'.join(library))

        if '+cuda' in self.spec['py-torch']:
            env.set('FORCE_CUDA', 1)
            env.set('CUDA_HOME', self.spec['cuda'].prefix)
            pytorch_cuda_arch = ';'.join(
                '{0:.1f}'.format(float(i) / 10.0) for i in
                self.spec['py-torch'].variants['cuda_arch'].value
            )
            env.set('TORCH_CUDA_ARCH_LIST', pytorch_cuda_arch)
        else:
            env.set('FORCE_CUDA', 0)
