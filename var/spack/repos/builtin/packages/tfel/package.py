# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Tfel(CMakePackage):
    """
    The TFEL project is a collaborative development of CEA
    (French Alternative Energies and Atomic Energy Commission) and
    EDF (Electricite de France).

    It mostly contains the MFront code generator which translates
    a set of closely related domain specific languages into plain C++
    on top of the TFEL libraries. MFront handles material properties,
    mechanical behaviours and simple point-wise models. Interfaces
    are provided for several finite element solvers, such as:
    Abaqus/Standard, Abaqus/Explicit, Ansys APDL, Cast3M,
    Europlexus, Code_Aster, CalculiX and a few others.

    MFront comes with an handy easy-to-use tool called MTest that can
    test the local behaviour of a material, by imposing independent
    constraints on each component of the strain or the stress.
    """

    homepage = "http://tfel.sourceforge.net"
    url      = "https://github.com/thelfer/tfel/archive/TFEL-3.2.0.tar.gz"
    git      = "https://github.com/thelfer/tfel.git"

    # development branches
    version("master", branch="master")
    version("rliv-3.2", branch="rliv-3.2")
    version("rliv-3.1", branch="rliv-3.1")
    version("rliv-3.0", branch="rliv-3.0")
    version("rliv-2.0", branch="rliv-2.0")
    version("rliv-1.2", branch="rliv-1.2")

    # released version
    version('3.2.0', sha256='089d79745e9f267a2bd03dcd8841d484e668bd27f5cc2ff7453634cb39016848')
    version('3.1.3', sha256='2022fa183d2c2902ada982ec6550ebe15befafcb748fd988fc9accdde7976a42')
    version('3.1.2', sha256='2eaa191f0699031786d8845ac769320a42c7e035991d82b3738289886006bfba')
    version('3.1.1', sha256='a4c0c21c6c22752cc90c82295a6bafe637b3395736c66fcdfcfe4aeccb5be7af')
    version('3.1.0', sha256='dd67b400b5f157aef503aa3615b9bf6b52333876a29e75966f94ee3f79ab37ad')
    version('3.0.3', sha256='3ff1c14bcc27e9b615aab5748eaf3afac349050b27b55a2b57648aba28b801ac')
    version('3.0.2', sha256='edd54ac652e99621410137ea2f7f90f133067615a17840440690365e2c3906f5')
    version('3.0.1', sha256='fa239ddd353431954f2ab7443cf85d86c862433e72f7685c1b933ae12dbde435')
    version('3.0.0', sha256='b2cfaa3d7900b4f32f327565448bf9cb8e4242763f651bff8f231f378a278f9e')
    version('2.0.4', sha256='cac078435aad73d9a795516f161b320d204d2099d6a286e786359f484355a43a')

    # solvers interfaces
    variant('castem', default=True,
            description='Enables Cast3M interface')
    variant('aster', default=True,
            description='Enables Code_Aster interface')
    variant('abaqus', default=True,
            description='Enables Abaqus/Standard and ' +
            'Abaqus/Explicit interfaces')
    variant('ansys', default=True,
            description='Enables Ansys APDL interface')
    variant('europlexus', default=True,
            description='Enables Europlexus interface')
    variant('cyrano', default=True,
            description='Enables Cyrano interface')
    variant('lsdyna', default=True,
            description='Enables LS-DYNA interface')
    variant('fortran', default=True,
            description='Enables fortran interface')
    variant('python', default=True,
            description='Enables python interface')
    variant('python_bindings', default=True,
            description='Enables python bindings')

    depends_on('python', when='+python')
    depends_on('python', when='+python_bindings')
    depends_on('boost+python', when='+python_bindings')

    def cmake_args(self):

        args = []

        if '+fortran' in self.spec:
            args.append("-Denable-fortran=ON")
        if '+castem' in self.spec:
            args.append("-Denable-castem=ON")
        if '+aster' in self.spec:
            args.append("-Denable-aster=ON")
        if '+abaqus' in self.spec:
            args.append("-Denable-abaqus=ON")
        if '+calculix' in self.spec:
            args.append("-Denable-calculix=ON")
        if '+ansys' in self.spec:
            args.append("-Denable-ansys=ON")
        if '+europlexus' in self.spec:
            args.append("-Denable-europlexus=ON")
        if '+cyrano' in self.spec:
            args.append("-Denable-cyrano=ON")
        if '+lsdyna' in self.spec:
            args.append("-Denable-lsdyna=ON")
        if '+python' in self.spec:
            args.append("-Denable-python=ON")
        if '+python_bindings' in self.spec:
            args.append("-Denable-python-bindings=ON")

        return args
