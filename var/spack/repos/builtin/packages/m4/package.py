# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re


class M4(AutotoolsPackage, GNUMirrorPackage):
    """GNU M4 is an implementation of the traditional Unix macro processor."""

    homepage = "https://www.gnu.org/software/m4/m4.html"
    gnu_mirror_path = "m4/m4-1.4.18.tar.gz"

    version('1.4.18', sha256='ab2633921a5cd38e48797bf5521ad259bdc4b979078034a3b790d7fec5493fab')
    version('1.4.17', sha256='3ce725133ee552b8b4baca7837fb772940b25e81b2a9dc92537aeaf733538c9e')

    patch('gnulib-pgi.patch', when='@1.4.18')
    patch('pgi.patch', when='@1.4.17')
    patch('nvhpc.patch', when='%nvhpc')
    patch('oneapi.patch', when='%oneapi')
    # from: https://github.com/Homebrew/homebrew-core/blob/master/Formula/m4.rb
    # Patch credit to Jeremy Huddleston Sequoia <jeremyhu@apple.com>
    patch('secure_snprintf.patch', when='os = highsierra')
    patch('secure_snprintf.patch', when='os = mojave')
    patch('secure_snprintf.patch', when='os = catalina')
    # https://bugzilla.redhat.com/show_bug.cgi?id=1573342
    patch('https://src.fedoraproject.org/rpms/m4/raw/5d147168d4b93f38a4833f5dd1d650ad88af5a8a/f/m4-1.4.18-glibc-change-work-around.patch', sha256='fc9b61654a3ba1a8d6cd78ce087e7c96366c290bc8d2c299f09828d793b853c8', when='@1.4.18')

    variant('sigsegv', default=True,
            description="Build the libsigsegv dependency")

    depends_on('libsigsegv', when='+sigsegv')

    build_directory = 'spack-build'

    tags = ['build-tools']

    executables = ['^g?m4$']

    @classmethod
    def determine_version(cls, exe):
        # Output on macOS:
        #   GNU M4 1.4.6
        # Output on Linux:
        #   m4 (GNU M4) 1.4.18
        output = Executable(exe)('--version', output=str, error=str)
        match = re.search(r'GNU M4\)?\s+(\S+)', output)
        return match.group(1) if match else None

    def configure_args(self):
        spec = self.spec
        args = ['--enable-c++']

        if spec.satisfies('%cce@9:'):
            args.append('LDFLAGS=-rtlib=compiler-rt')

        if (spec.satisfies('%clang') or
            spec.satisfies('%aocc') or
            spec.satisfies('%arm') or
            spec.satisfies('%fj')) and not spec.satisfies('platform=darwin'):
            args.append('LDFLAGS=-rtlib=compiler-rt')

        if spec.satisfies('%intel@:18.999'):
            args.append('CFLAGS=-no-gcc')

        if '+sigsegv' in spec:
            args.append('--with-libsigsegv-prefix={0}'.format(
                spec['libsigsegv'].prefix))
        else:
            args.append('--without-libsigsegv-prefix')

        # http://lists.gnu.org/archive/html/bug-m4/2016-09/msg00002.html
        arch = spec.architecture
        if (arch.platform == 'darwin' and arch.os == 'sierra' and
                '%gcc' in spec):
            args.append('ac_cv_type_struct_sched_param=yes')

        return args

    def test(self):
        spec_vers = str(self.spec.version)
        reason = 'test: ensuring m4 version is {0}'.format(spec_vers)
        self.run_test('m4', '--version', spec_vers, installed=True,
                      purpose=reason, skip_missing=False)

        reason = 'test: ensuring m4 example succeeds'
        test_data_dir = self.test_suite.current_test_data_dir
        hello_file = test_data_dir.join('hello.m4')
        expected = get_escaped_text_output(test_data_dir.join('hello.out'))
        self.run_test('m4', hello_file, expected, installed=True,
                      purpose=reason, skip_missing=False)
