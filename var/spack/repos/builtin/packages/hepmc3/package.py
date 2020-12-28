# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Hepmc3(CMakePackage):
    """The HepMC package is an object oriented, C++ event record for
       High Energy Physics Monte Carlo generators and simulation."""

    homepage = "https://cern.ch/hepmc"
    url      = "https://gitlab.cern.ch/hepmc/HepMC3/-/archive/3.2.1/HepMC3-3.2.1.tar.gz"
    git      = "https://gitlab.cern.ch/hepmc/HepMC3.git"

    tags = ['hep']

    maintainers = ['vvolkl']

    version('3.2.2', sha256='0e8cb4f78f804e38f7d29875db66f65e4c77896749d723548cc70fb7965e2d41')
    version('3.2.1', sha256='6e4e4bb5708af105d4bf74efc2745e6efe704e942d46a8042f7dcae37a4739fe')
    version('3.2.0', sha256='f132387763d170f25a7cc9f0bd586b83373c09acf0c3daa5504063ba460f89fc')
    version('3.1.2', sha256='4133074b3928252877982f3d4b4c6c750bb7a324eb6c7bb2afc6fa256da3ecc7')
    version('3.1.1', sha256='2fcbc9964d6f9f7776289d65f9c73033f85c15bf5f0df00c429a6a1d8b8248bb')
    version('3.1.0', sha256='cd37eed619d58369041018b8627274ad790020a4714b54ac05ad1ebc1a6e7f8a')
    # note that version 3.0.0 is not supported
    # conflicts with cmake configuration

    variant('python', default=False, description='Enable Python bindings')
    variant('rootio', default=False, description='Enable ROOT I/O')
    variant('interfaces', default=False, description='Install interfaces for some Monte-Carlo Event Gens')

    depends_on('cmake@2.8.9:', type='build')
    depends_on('root', when='+rootio')
    depends_on('python', when="+python")

    conflicts('%gcc@9.3.0', when="@:3.1.1")
    patch('ba38f14d8f56c16cc4105d98f6d4540c928c6150.patch', when="@3.1.2:3.2.1 %gcc@9.3.0")

    def cmake_args(self):
        spec = self.spec
        args = [
            '-Dmomentum:STRING=GEV',
            '-Dlength:STRING=MM',
            '-DHEPMC3_ENABLE_PYTHON={0}'.format(spec.satisfies('+python')),
            '-DHEPMC3_ENABLE_ROOTIO={0}'.format(spec.satisfies('+rootio')),
            '-DHEPMC3_INSTALL_INTERFACES={0}'.format(
                spec.satisfies('+interfaces')),
        ]

        if self.spec.satisfies('+python'):
            py_ver = spec['python'].version.up_to(2)
            py_sitepkg = join_path(self.prefix, site_packages_dir)
            args.extend([
                '-DHEPMC3_PYTHON_VERSIONS={0}'.format(py_ver),
                '-DHEPMC3_Python_SITEARCH{0}={1}'.format(
                    py_ver.joined, py_sitepkg)
            ])

        if self.spec.satisfies('+rootio'):
            args.append('-DROOT_DIR={0}'.format(self.spec['root'].prefix))
        return args
