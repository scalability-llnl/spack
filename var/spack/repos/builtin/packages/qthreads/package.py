# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


def is_integer(x):
    """Any integer value"""

    try:
        return float(x).is_integer()
    except ValueError:
        return False


class Qthreads(AutotoolsPackage):
    """The qthreads API is designed to make using large numbers of
       threads convenient and easy, and to allow portable access to
       threading constructs used in massively parallel shared memory
       environments. The API maps well to both MTA-style threading and
       PIM-style threading, and we provide an implementation of this
       interface in both a standard SMP context as well as the SST
       context. The qthreads API provides access to full/empty-bit
       (FEB) semantics, where every word of memory can be marked
       either full or empty, and a thread can wait for any word to
       attain either state."""
    homepage = "http://www.cs.sandia.gov/qthreads/"

    url = "https://github.com/Qthreads/qthreads/releases/download/1.10/qthread-1.10.tar.bz2"
    test_requires_compiler = True
    test_base_path = 'test/basics/'
    test_list = ['hello_world_multi', 'hello_world']

    version("1.14", sha256="16f15e5b2e35b6329a857d24c283a1e43cd49921ee49a1446d4f31bf9c6f5cf9")
    version("1.12", sha256="2c13a5f6f45bc2f22038d272be2e748e027649d3343a9f824da9e86a88b594c9")
    version("1.11", sha256="dbde6c7cb7de7e89921e47363d09cecaebf775c9d090496c2be8350355055571")
    version("1.10", sha256="29fbc2e54bcbc814c1be13049790ee98c505f22f22ccee34b7c29a4295475656")

    patch("restrict.patch", when="@:1.10")
    patch("trap.patch", when="@:1.10")

    variant(
        'hwloc',
        default=True,
        description='hwloc support'
    )
    variant('spawn_cache',
            default=False,
            description='enables worker specific cache of spawns')
    variant('scheduler', default='nemesis',
            values=('nemesis', 'lifo', 'mutexfifo', 'mtsfifo',
                    'sherwood', 'distrib', 'nottingham'),
            multi=False,
            description='Specify which scheduler policy to use')
    variant('static', default=True, description='Build static library')
    variant('stack_size',
            default=4096,
            description='Specify number of bytes to use in a stack',
            values=is_integer)

    depends_on("hwloc@1.0:1.99", when="+hwloc")

    def configure_args(self):
        spec = self.spec
        if "+hwloc" in self.spec:
            args = [
                "--enable-guard-pages",
                "--with-topology=hwloc",
                "--with-hwloc=%s" % spec["hwloc"].prefix]
        else:
            args = ["--with-topology=no"]

        if '+spawn_cache' in self.spec:
            args.append('--enable-spawn-cache')
        else:
            args.append('--disable-spawn-cache')

        if '+static' in self.spec:
            args.append('--enable-static=yes')
        else:
            args.append('--enable-static=no')

        args.append('--with-default-stack-size=%s'
                    % self.spec.variants['stack_size'].value)

        args.append('--with-scheduler=%s'
                    % self.spec.variants['scheduler'].value)
        return args

    @run_after('install')
    def setup_build_tests(self):
        """Copy the build test files after the package is installed to an
        install test subdirectory for use during `spack test run`."""
        tests = self.test_list
        relative_test_dir = self.test_base_path
        files_to_cpy = []
        header = 'test/argparsing.h'
        for test in tests:
            test_path = join_path(relative_test_dir, test + '.c')
            files_to_cpy.append(test_path)
        files_to_cpy.append(header)
        self.cache_extra_test_sources(files_to_cpy)

    def build_tests(self):
        """Build and run the added smoke (install) test."""
        tests = self.test_list
        relative_test_dir = self.test_base_path

        for test in tests:
            options = [
                '-I{0}'.format(self.prefix.include),
                '-I{0}'.format(self.install_test_root + '/test'),
                join_path(self.install_test_root, relative_test_dir,
                          test + '.c'),
                '-o',
                test,
                '-L{0}'.format(self.prefix.lib),
                '-lqthread',
                '{0}{1}'.format(self.compiler.cc_rpath_arg,
                                self.prefix.lib)]
            reason = 'test:{0}: Checking ability to link to the library.'\
                     .format(test)
            self.run_test('cc', options, [], installed=False, purpose=reason)

    def run_tests(self):
        tests = self.test_list
        # Now run the program
        for test in tests:
            reason = 'test:{0}: Checking ability to execute.'.format(test)
            self.run_test(test, [], purpose=reason)

    def test(self):
        # Build
        self.build_tests()
        # Run test programs pulled from the build
        self.run_tests()
