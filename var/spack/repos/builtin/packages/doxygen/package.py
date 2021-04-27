# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import re


class Doxygen(CMakePackage):
    """Doxygen is the de facto standard tool for generating documentation
    from annotated C++ sources, but it also supports other popular programming
    languages such as C, Objective-C, C#, PHP, Java, Python, IDL (Corba,
    Microsoft, and UNO/OpenOffice flavors), Fortran, VHDL, Tcl, and to some
    extent D.."""

    homepage  = "https://github.com/doxygen/doxygen/"
    git       = "https://github.com/doxygen/doxygen.git"

    # Doxygen versions on GitHub
    version('1.9.1',  commit='ef9b20ac7f8a8621fcfc299f8bd0b80422390f4b')
    version('1.9.0',  commit='71777ff3973331bd9453870593a762e184ba9f78')
    version('1.8.20', commit='f246dd2f1c58eea39ea3f50c108019e4d4137bd5')
    version('1.8.17', commit='b5fa3cd1c6e6240e20d3b80a70e3f04040b32021')
    version('1.8.16', commit='cfd73d5c4d1a66c620a3b7c08b72a3f3c3f94255')
    version('1.8.15', commit='dc89ac01407c24142698c1374610f2cee1fbf200')
    version('1.8.14', commit='2f4139de014bf03898320a45fe52c92872c1e0f4')
    version('1.8.12', commit='4951df8d0d0acf843b4147136f945504b96536e7')
    version('1.8.11', commit='a6d4f4df45febe588c38de37641513fd576b998f')
    version('1.8.10', commit='fdae7519a2e29f94e65c0e718513343f07302ddb')

    # graphviz appears to be a run-time optional dependency
    variant('graphviz', default=False,
            description='Build with dot command support from Graphviz.')

    variant('mscgen', default=False,
            description='Build with support for code graphs from mscgen.')

    executables = ['doxygen']

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)('-v', output=str, error=str)
        match = re.search(r"^([\d\.]+)$", output)
        return match.group(1) if match else None

    @classmethod
    def determine_variants(cls, exes, version_str):
        variants = ''
        if which('dot'):
            variants += "+graphviz"
        else:
            variants += "~graphviz"

        if which('mscgen'):
            variants += "+mscgen"
        else:
            variants += "~mscgen"

        return variants

    depends_on("cmake@2.8.12:", type='build')
    depends_on("python", type='build')  # 2 or 3 OK; used in CMake build
    depends_on("iconv")
    depends_on("flex", type='build')
    depends_on("bison", type='build')
    # code.l just checks subminor version <=2.5.4 or >=2.5.33
    # but does not recognize 2.6.x as newer...could be patched if needed
    depends_on("flex@2.5.39", type='build', when='@1.8.10')
    depends_on("bison@2.7:", type='build', when='@1.8.10:')

    # optional dependencies
    depends_on("graphviz", when="+graphviz", type='run')
    depends_on("mscgen", when="+mscgen", type='run')

    # Support C++14's std::shared_ptr. For details about this patch, see
    # https://github.com/Sleepyowl/doxygen/commit/6c380ba91ae41c6d5c409a5163119318932ae2a3?diff=unified
    # Also - https://github.com/doxygen/doxygen/pull/6588
    patch('shared_ptr.patch', when='@1.8.14')

    # Workaround for gcc getting stuck in an infinite loop
    patch('gcc-partial-inlining-bug.patch', when='@1.8.20: %gcc@7')

    def patch(self):
        if self.spec['iconv'].name == 'libc':
            return
        # On Linux systems, iconv is provided by libc. Since CMake finds the
        # symbol in libc, it does not look for libiconv, which leads to linker
        # errors. This makes sure that CMake always looks for the external
        # libconv instead.
        filter_file('check_function_exists(iconv_open ICONV_IN_GLIBC)',
                    'set(ICONV_IN_GLIBC FALSE)',
                    join_path('cmake', 'FindIconv.cmake'),
                    string=True)
