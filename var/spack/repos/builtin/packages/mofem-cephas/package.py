# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class MofemCephas(CMakePackage):
    """MoFEM is finite element core library"""

    homepage = "http://mofem.eng.gla.ac.uk"
    git = "https://bitbucket.org/likask/mofem-cephas.git"

    maintainers = ['likask']

    version('develop', branch='develop')
    version('0.8.17', tag='v0.8.17')
    version('0.8.16', tag='v0.8.16')
    version('0.8.15', tag='v0.8.15')
    version('0.8.14', tag='v0.8.14')
    version('0.8.13', tag='v0.8.13')
    version('0.8.12', tag='v0.8.12')
    version('0.8.11', tag='v0.8.11')
    version('0.8.10', tag='v0.8.10')
    version('0.8.9', tag='v0.8.9')
    version('0.8.8', tag='v0.8.8')
    version('0.8.7', tag='v0.8.7')

    # This option can be only used for development of core lib
    variant('copy_user_modules', default=True,
            description='Copy user modules directory '
            'instead of linking to source')
    variant('adol-c', default=True, description='Compile with ADOL-C')
    variant('tetgen', default=True, description='Compile with Tetgen')
    variant('med', default=True, description='Compile with Med')
    variant('slepc', default=False, description='Compile with Slepc')

    depends_on("mpi")
    depends_on("boost@:1.68")
    depends_on("parmetis")
    # Fixed version of hdf5, to remove some problems with dependent
    # packages, f.e. MED format
    depends_on("hdf5@:1.8.19+hl+mpi+fortran")
    depends_on("petsc@:3.9.3+mumps+mpi")
    depends_on('slepc', when='+slepc')
    depends_on("moab")
    # Upper bound set to ADOL-C until issues with memory leaks
    # for versions 2.6: fully resolved
    depends_on("adol-c@2.5.2~examples", when="+adol-c")
    depends_on("tetgen", when="+tetgen")
    depends_on("med", when='+med')

    extendable = True

    root_cmakelists_dir = 'mofem'

    def cmake_args(self):
        spec = self.spec
        options = []

        # obligatory options
        options.extend([
            '-DWITH_SPACK=YES',
            '-DPETSC_DIR=%s' % spec['petsc'].prefix,
            '-DPETSC_ARCH=',
            '-DMOAB_DIR=%s' % spec['moab'].prefix,
            '-DBOOST_DIR=%s' % spec['boost'].prefix])

        # build tests
        options.append('-DMOFEM_BUILD_TESTS={0}'.format(
            'ON' if self.run_tests else 'OFF'))

        # variant packages
        if '+adol-c' in spec:
            options.append('-DADOL-C_DIR=%s' % spec['adol-c'].prefix)

        if '+tetgen' in spec:
            options.append('-DTETGEN_DIR=%s' % spec['tetgen'].prefix)

        if '+med' in spec:
            options.append('-DMED_DIR=%s' % spec['med'].prefix)

        if '+slepc' in spec:
            options.append('-DSLEPC_DIR=%s' % spec['slepc'].prefix)

        # copy users modules, i.e. stand alone vs linked users modules
        options.append(
            '-DSTAND_ALLONE_USERS_MODULES=%s' %
            ('YES' if '+copy_user_modules' in spec else 'NO'))
        return options
