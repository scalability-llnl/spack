# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Simgrid(CMakePackage):
    """To study the behavior of large-scale distributed systems such as Grids,
    Clouds, HPC or P2P systems."""

    homepage = "http://simgrid.org/"
    url      = "https://gforge.inria.fr/frs/download.php/file/37758/SimGrid-3.21.tar.gz"
    git      = 'https://scm.gforge.inria.fr/anonscm/git/simgrid/simgrid.git'

    version('3.21', sha256='d2a6e9021016dd39a2b6f8d5d18c8223f6885746c5269550d19ba29c47c0c6a0',
            url='https://gforge.inria.fr/frs/download.php/file/37758/SimGrid-3.21.tar.gz')
    version('3.20', sha256='4d4757eb45d87cf18d990d589c31d223b0ea8cf6fcd8c94fca4d38162193cef6',
            url='https://gforge.inria.fr/frs/download.php/file/37602/SimGrid-3.20.tar.gz')
    version('3.19', sha256='64a3b82fdf0a65bb8b7c8e9feb01694360edaf38070097bf28aa181eccb86ea7',
            url='https://gforge.inria.fr/frs/download.php/file/37452/SimGrid-3.19.tar.gz')
    version('3.18', sha256='dc8f6223d89326b6a21c99eabc90598fa153d6b0818a63ff5c3ec8726e2257b2',
            url='https://gforge.inria.fr/frs/download.php/file/37294/SimGrid-3.18.tar.gz')
    version('3.17', sha256='f5e44f41983e83f65261598ab0de1909d3a8a3feb77f28e37d38f04631dbb908',
            url='https://gforge.inria.fr/frs/download.php/file/37148/SimGrid-3.17.tar.gz')
    version('3.16', sha256='51782534fec87eed9da345319ead699b13d7dad4be7ac89984a0446cb385d3fa',
            url='https://gforge.inria.fr/frs/download.php/file/36900/SimGrid-3.16.tar.gz')
    version('3.15', sha256='d1e411cdbfa953c018411b842727339ede6b82efcd5d3f6adc13a24f182fa9e8',
            url='https://gforge.inria.fr/frs/download.php/file/36621/SimGrid-3.15.tar.gz')
    version('3.14.159', sha256='2d93db245c6ec8039ffe332a77531b836ad093d57f18ec3f7920fe98e3719f48',
            url='http://gforge.inria.fr/frs/download.php/file/36384/SimGrid-3.14.159.tar.gz')
    version('3.13', sha256='7bcedd19492f9a32cc431840ad2688d0d6e4121982d6d26e0174b5c92b086121',
            url='http://gforge.inria.fr/frs/download.php/file/35817/SimGrid-3.13.tar.gz')
    version('3.12', sha256='d397ee0273395dc687fbcd2601515e7142559801a3db387454d77e0e18cd7878',
            url='http://gforge.inria.fr/frs/download.php/file/35215/SimGrid-3.12.tar.gz')
    version('3.11', sha256='6efb006e028e37f74a34fc37d585a8cb296720020cabad361d65662533f1600b',
            url='http://gforge.inria.fr/frs/download.php/file/33683/SimGrid-3.11.tar.gz')
    version('git', branch='master')

    variant('doc', default=False, description='Build documentation')
    variant('smpi', default=True, description='SMPI provides MPI')
    variant('examples', default=False, description='Install examples')
    variant('mc', default=False, description='Model checker')

    # does not build correctly with some old compilers -> rely on packages
    depends_on('boost')

    def setup_dependent_package(self, module, dep_spec):

        if self.spec.satisfies('+smpi'):
            self.spec.smpicc  = join_path(self.prefix.bin, 'smpicc')
            self.spec.smpicxx = join_path(self.prefix.bin,
                                          'smpicxx -std=c++11')
            self.spec.smpifc  = join_path(self.prefix.bin, 'smpif90')
            self.spec.smpif77 = join_path(self.prefix.bin, 'smpiff')

    def cmake_args(self):

        spec = self.spec
        args = []

        if not spec.satisfies('+doc'):
            args.append("-Denable_documentation=OFF")
        if spec.satisfies('+mc'):
            args.append("-Denable_model-checking=ON")

        return args

    def install(self, spec, prefix):
        """Make the install targets"""
        with working_dir(self.build_directory):
            make("install")
            if spec.satisfies('+examples'):
                install_tree(join_path(self.build_directory, 'examples'),
                             prefix.examples)
