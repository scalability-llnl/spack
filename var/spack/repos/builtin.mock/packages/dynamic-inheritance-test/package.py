# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class DynamicInheritanceTest(DynamicInheritancePackage):
    classes = {
        CMakePackage: '@1.0',
        AutotoolsPackage: '@2.0',
        PythonPackage: '@3.0'
    }

    homepage = 'http://www.example.com/'
    url      = 'http://www.example.com/example-1.0.tar.gz'

    version('1.0', 'aaaaaaaaaaaaaaaaaaaaaaaaaa')
    version('2.0', 'aaaaaaaaaaaaaaaaaaaaaaaaaa')
    version('3.0', 'aaaaaaaaaaaaaaaaaaaaaaaaaa')

    depends_on('cmake', when='@1.0', type='build')
    depends_on('python', when='@3.0', type=('build', 'run'))

    variant('build_type', default='RelWithDebInfo',
            description='CMake build type',
            values=('Debug', 'Release', 'RelWithDebInfo', 'MinSizeRel'))

    phases = DynamicInheritancePackage.phases + ['sdist']
    include_phases = ['sdist']

    @run_after('build')
    def after_build(self):
        return 'after_build'

    def set_build_system(self, spec, prefix):
        super(DynamicInheritanceTest, self).set_build_system(spec, prefix)
        active_phases = [phase for phase in self.phases
                         if getattr(self, '_InstallPhase_%s' % phase, None)]
        valid_phases = self.cls.phases
        if spec.satisfies('@3.0'):
            valid_phases += ['sdist']
        assert active_phases == valid_phases
