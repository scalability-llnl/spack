# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class Kicad(CMakePackage):
    """KiCad is an open source software suite for Electronic Design
    Automation (EDA). The programs handle Schematic Capture, and PCB
    Layout with Gerber output."""

    homepage = 'https://kicad.org'
    url = 'https://gitlab.com/kicad/code/kicad/-/archive/5.1.8/kicad-5.1.8.tar.gz'
    maintainers = ['aweits']

    version('5.1.9', sha256='841be864b9dc5c761193c3ee9cbdbed6729952d7b38451aa8e1977bdfdb6081b')
    version('5.1.8', sha256='bf24f8ef427b4a989479b8e4af0b8ae5c54766755f12748e2e88a922c5344ca4')

    depends_on('wxwidgets')
    depends_on('python@3:', type=('build', 'run'))
    # py-wxpython needs work
    # depends_on('py-wxpython', type=('build', 'run'))
    depends_on('glew')
    depends_on('gl')
    depends_on('glm')
    depends_on('boost@1.56:')
    depends_on('oce+X11')
    depends_on('swig', type='build')
    depends_on('curl')
    depends_on('pkgconfig')
    depends_on('git', type=('build', 'run'))
    depends_on('ngspice')
    depends_on('hicolor-icon-theme', type=('build', 'run'))
    depends_on('adwaita-icon-theme', type=('build', 'run'))
    depends_on('gsettings-desktop-schemas', type=('build', 'run'))

    extends('python')

    resource_list = [
        # version, resource, sha256sum
        ('5.1.8', 'footprints', '8937b5ba0f67844ffaca40632bebe9c2f4f17fba446137434aa72363c55d7dd9'),
        ('5.1.8', 'packages3D', '81e64939e922742431284bb19d1ec274d6dc10fd238e5583ead21dc08876c221'),
        ('5.1.8', 'symbols', '98cedcca4d7ad6e3be96ec5a41f8f9b3414eae276bac1efdfd3f8871f0f8bc7e'),
        ('5.1.8', 'templates', 'd64ca82854e9780413447a3fa82a528b264d39f57d467fddfc78f919e7ed15c5'),
        ('5.1.9', 'footprints', 'a86fbe00fccd6da2d29687ec0c56a9c3cb6b9748ee8fd35c1625839168f28edc'),
        ('5.1.9', 'packages3D', '35a4888dabd2dedb0d49c3e84b0eebc97b306200510e818dad90d4bb1c9e3296'),
        ('5.1.9', 'symbols', '6741a7b01f14f1f5aae3155a554816516cf02ce7790074ba8462dee8091f8c2f'),
        ('5.1.9', 'templates', 'bacf93567f8efe87314762448bb69698c8ed387058c13868c051c91740014aac'),
    ]

    for ver, lib, checksum in resource_list:
        resource(when='@{0}'.format(ver),
                 name=lib,
                 url='https://gitlab.com/kicad/libraries/kicad-{0}/-/archive/{1}/kicad-{0}-{1}.tar.bz2'.format(lib, ver),
                 sha256=checksum,
                 destination='',
                 )

    def setup_dependent_build_environment(self, env, dependent_spec):
        env.prepend_path('XDG_DATA_DIRS', self.prefix.share)

    def setup_dependent_run_environment(self, env, dependent_spec):
        env.prepend_path('XDG_DATA_DIRS', self.prefix.share)

    def setup_build_environment(self, env):
        env.prepend_path("XDG_DATA_DIRS", self.prefix.share)

    def setup_run_environment(self, env):
        env.prepend_path("XDG_DATA_DIRS", self.prefix.share)

    def cmake_args(self):
        args = []
        args.append('-DKICAD_SCRIPTING_PYTHON3=ON')
        args.append('-DKICAD_SCRIPTING_WXPYTHON=OFF')
        return args

    @run_after('install')
    def install_libraries(self):
        for ver, lib, checksum in self.resource_list:
            if self.spec.version == Version(ver):
                with working_dir('kicad-{0}-{1}'.format(lib, ver)):
                    args = std_cmake_args
                    cmake(*args)
                    make('install')
