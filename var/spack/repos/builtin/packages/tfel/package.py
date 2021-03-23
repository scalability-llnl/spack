# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# Maintainer comments:
# 18/12/2018: fix python detection

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
    url      = "https://github.com/thelfer/tfel/archive/TFEL-3.4.0.tar.gz"
    git      = "https://github.com/thelfer/tfel.git"
    maintainers = ['thelfer']

    # development branches
    version("master", branch="master")
    version("rliv-3.4", branch="rliv-3.4")
    version("rliv-3.3", branch="rliv-3.3")
    version("rliv-3.2", branch="rliv-3.2")
    version("rliv-3.1", branch="rliv-3.1")
    version("rliv-3.0", branch="rliv-3.0")
    version("rliv-2.0", branch="rliv-2.0")
    version("rliv-1.2", branch="rliv-1.2")

    # released version
    version('3.4.0', sha256='176feb4c1726d0f21f4c656b20620dce6f99ab7f5f09a66905aeb643a316bbc1')
    version('3.3.1', sha256='ad07329c25874832fbacc999b5f88d9b9ab84415bc897a6f3cae5b4afcd7661f')
    version('3.3.0', sha256='884ad68b0fbbededc3a602d559433c24114ae4534dc9f0a759d31ca3589dace0')
    version('3.2.2', sha256='69b01ae0d1f9140b619aaa9135948284ff40d4654672c335e55ab4934c02eb43')
    version('3.2.1', sha256='12786480524a7fe86889120fb334fa00211dfd44ad5ec71e2279e7adf1ddc807')
    version('3.2.0', sha256='089d79745e9f267a2bd03dcd8841d484e668bd27f5cc2ff7453634cb39016848')
    version('3.1.5', sha256='e22cf2110f19666f004b8acda32e87beae74721f82e7f83fd0c4fafb86812763')
    version('3.1.4', sha256='8dc2904fc930636976baaf7e91ac89c0377afb1629c336343dfad8ab651cf87d')
    version('3.1.3', sha256='2022fa183d2c2902ada982ec6550ebe15befafcb748fd988fc9accdde7976a42')
    version('3.1.2', sha256='2eaa191f0699031786d8845ac769320a42c7e035991d82b3738289886006bfba')
    version('3.1.1', sha256='a4c0c21c6c22752cc90c82295a6bafe637b3395736c66fcdfcfe4aeccb5be7af')
    version('3.1.0', sha256='dd67b400b5f157aef503aa3615b9bf6b52333876a29e75966f94ee3f79ab37ad')
    version('3.0.5', sha256='abf58f87962cf98b6129e873a841819a2a751f2ebd4e08490eb89fb933cd7887')
    version('3.0.4', sha256='e832d421a0dc9f315c60c5ea23f958dcaa299913c50a4eb73bde0e053067a3cc')
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
    variant('java', default=False,
            description='Enables java interface')

    # only since TFEL-3.3, no effect on version below
    variant('comsol', default=True,
            description='Enables comsol interface')
    variant('diana-fea', default=True,
            description='Enables DIANA-FEA interface')

    variant('build_type', default='Release',
            description='The build type to build',
            values=('Debug', 'Release'))

    depends_on('java', when='+java')
    depends_on('python', when='+python',
               type=('build', 'link', 'run'))
    depends_on('python', when='+python_bindings',
               type=('build', 'link', 'run'))
    depends_on('boost+python+numpy', when='+python_bindings')

    extends('python', when='+python_bindings')

    def cmake_args(self):

        args = []

        args.append("-DUSE_EXTERNAL_COMPILER_FLAGS=ON")

        for i in ['fortran', 'java', 'aster', 'abaqus', 'calculix',
                  'ansys', 'europlexus', 'cyrano', 'lsdyna', 'python',
                  'comsol', 'diana-fea']:
            if '+' + i in self.spec:
                args.append("-Denable-{0}=ON".format(i))
            else:
                args.append("-Denable-{0}=OFF".format(i))

        if '+castem' in self.spec:
            args.append("-Dlocal-castem-header=ON")
        else:
            args.append("-Dlocal-castem-header=OFF")

        if '+python_bindings' in self.spec:
            args.append("-Denable-python-bindings=ON")
        else:
            args.append("-Denable-python-bindings=OFF")

        if(('+python' in self.spec) or
           ('+python_bindings' in self.spec)):
            python = self.spec['python']
            args.append('-DPYTHON_LIBRARY={0}'.
                        format(python.libs[0]))
            args.append('-DPYTHON_INCLUDE_DIR={0}'.
                        format(python.headers.directories[0]))
            args.append('-DPython_ADDITIONAL_VERSIONS={0}'.
                        format(python.version.up_to(2)))

        if '+python_bindings' in self.spec:
            args.append('-DBOOST_ROOT={0}'.
                        format(self.spec['boost'].prefix))
            args.append('-DBoost_NO_SYSTEM_PATHS=ON')
            args.append('-DBoost_NO_BOOST_CMAKE=ON')

        return args
