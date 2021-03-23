# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""
This test checks that the Spack cc compiler wrapper is parsing
arguments correctly.
"""
import os
import pytest

from spack.paths import build_env_path
from spack.util.environment import system_dirs, set_env
from spack.util.executable import Executable

#
# Complicated compiler test command
#
test_args = [
    '-I/test/include', '-L/test/lib', '-L/other/lib', '-I/other/include',
    'arg1',
    '-Wl,--start-group',
    'arg2',
    '-Wl,-rpath,/first/rpath', 'arg3', '-Wl,-rpath', '-Wl,/second/rpath',
    '-llib1', '-llib2',
    'arg4',
    '-Wl,--end-group',
    '-Xlinker', '-rpath', '-Xlinker', '/third/rpath',
    '-Xlinker', '-rpath', '-Xlinker', '/fourth/rpath',
    '-Wl,--rpath,/fifth/rpath', '-Wl,--rpath', '-Wl,/sixth/rpath',
    '-llib3', '-llib4',
    'arg5', 'arg6']

#
# Pieces of the test command above, as they should be parsed out.
#
# `_wl_rpaths` are for the compiler (with -Wl,), and `_rpaths` are raw
# -rpath arguments for the linker.
#
test_include_paths = [
    '-I/test/include', '-I/other/include']

test_library_paths = [
    '-L/test/lib', '-L/other/lib']

test_wl_rpaths = [
    '-Wl,-rpath,/first/rpath', '-Wl,-rpath,/second/rpath',
    '-Wl,-rpath,/third/rpath', '-Wl,-rpath,/fourth/rpath',
    '-Wl,-rpath,/fifth/rpath', '-Wl,-rpath,/sixth/rpath']

test_rpaths = [
    '-rpath', '/first/rpath', '-rpath', '/second/rpath',
    '-rpath', '/third/rpath', '-rpath', '/fourth/rpath',
    '-rpath', '/fifth/rpath', '-rpath', '/sixth/rpath']

test_args_without_paths = [
    'arg1',
    '-Wl,--start-group',
    'arg2', 'arg3', '-llib1', '-llib2', 'arg4',
    '-Wl,--end-group',
    '-llib3', '-llib4', 'arg5', 'arg6']

#: The prefix of the package being mock installed
pkg_prefix = '/spack-test-prefix'

# Compilers to use during tests
cc = Executable(os.path.join(build_env_path, "cc"))
ld = Executable(os.path.join(build_env_path, "ld"))
cpp = Executable(os.path.join(build_env_path, "cpp"))
cxx = Executable(os.path.join(build_env_path, "c++"))
fc = Executable(os.path.join(build_env_path, "fc"))

#: the "real" compiler the wrapper is expected to invoke
real_cc = '/bin/mycc'

# mock flags to use in the wrapper environment
spack_cppflags = ['-g', '-O1', '-DVAR=VALUE']
spack_cflags   = ['-Wall']
spack_cxxflags = ['-Werror']
spack_fflags   = ['-w']
spack_ldflags  = ['-L', 'foo']
spack_ldlibs   = ['-lfoo']

lheaderpad = ['-Wl,-headerpad_max_install_names']
headerpad = ['-headerpad_max_install_names']


@pytest.fixture(scope='session')
def wrapper_environment():
    with set_env(
            SPACK_CC=real_cc,
            SPACK_CXX=real_cc,
            SPACK_FC=real_cc,
            SPACK_PREFIX=pkg_prefix,
            SPACK_ENV_PATH='test',
            SPACK_DEBUG_LOG_DIR='.',
            SPACK_DEBUG_LOG_ID='foo-hashabc',
            SPACK_COMPILER_SPEC='gcc@4.4.7',
            SPACK_SHORT_SPEC='foo@1.2 arch=linux-rhel6-x86_64 /hashabc',
            SPACK_SYSTEM_DIRS=':'.join(system_dirs),
            SPACK_CC_RPATH_ARG='-Wl,-rpath,',
            SPACK_CXX_RPATH_ARG='-Wl,-rpath,',
            SPACK_F77_RPATH_ARG='-Wl,-rpath,',
            SPACK_FC_RPATH_ARG='-Wl,-rpath,',
            SPACK_LINK_DIRS=None,
            SPACK_INCLUDE_DIRS=None,
            SPACK_RPATH_DIRS=None,
            SPACK_TARGET_ARGS='',
            SPACK_LINKER_ARG='-Wl,',
            SPACK_DTAGS_TO_ADD='--disable-new-dtags',
            SPACK_DTAGS_TO_STRIP='--enable-new-dtags'):
        yield


@pytest.fixture()
def wrapper_flags():
    with set_env(
            SPACK_CPPFLAGS=' '.join(spack_cppflags),
            SPACK_CFLAGS=' '.join(spack_cflags),
            SPACK_CXXFLAGS=' '.join(spack_cxxflags),
            SPACK_FFLAGS=' '.join(spack_fflags),
            SPACK_LDFLAGS=' '.join(spack_ldflags),
            SPACK_LDLIBS=' '.join(spack_ldlibs)):
        yield


pytestmark = pytest.mark.usefixtures('wrapper_environment')


def check_args(cc, args, expected):
    """Check output arguments that cc produces when called with args.

    This assumes that cc will print debug command output with one element
    per line, so that we see whether arguments that should (or shouldn't)
    contain spaces are parsed correctly.
    """
    with set_env(SPACK_TEST_COMMAND='dump-args'):
        cc_modified_args = cc(*args, output=str).strip().split('\n')
        assert expected == cc_modified_args


def dump_mode(cc, args):
    """Make cc dump the mode it detects, and return it."""
    with set_env(SPACK_TEST_COMMAND='dump-mode'):
        return cc(*args, output=str).strip()


def test_vcheck_mode():
    assert dump_mode(cc, ['-I/include', '--version']) == 'vcheck'
    assert dump_mode(cc, ['-I/include', '-V']) == 'vcheck'
    assert dump_mode(cc, ['-I/include', '-v']) == 'vcheck'
    assert dump_mode(cc, ['-I/include', '-dumpversion']) == 'vcheck'
    assert dump_mode(cc, ['-I/include', '--version', '-c']) == 'vcheck'
    assert dump_mode(cc, ['-I/include', '-V', '-o', 'output']) == 'vcheck'


def test_cpp_mode():
    assert dump_mode(cc, ['-E']) == 'cpp'
    assert dump_mode(cxx, ['-E']) == 'cpp'
    assert dump_mode(cpp, []) == 'cpp'


def test_as_mode():
    assert dump_mode(cc, ['-S']) == 'as'


def test_ccld_mode():
    assert dump_mode(cc, []) == 'ccld'
    assert dump_mode(cc, ['foo.c', '-o', 'foo']) == 'ccld'
    assert dump_mode(cc, ['foo.c', '-o', 'foo', '-Wl,-rpath,foo']) == 'ccld'
    assert dump_mode(cc, [
        'foo.o', 'bar.o', 'baz.o', '-o', 'foo', '-Wl,-rpath,foo']) == 'ccld'


def test_ld_mode():
    assert dump_mode(ld, []) == 'ld'
    assert dump_mode(ld, [
        'foo.o', 'bar.o', 'baz.o', '-o', 'foo', '-Wl,-rpath,foo']) == 'ld'


def test_ld_flags(wrapper_flags):
    check_args(
        ld, test_args,
        ['ld'] +
        spack_ldflags +
        test_include_paths +
        test_library_paths +
        ['--disable-new-dtags'] +
        test_rpaths +
        test_args_without_paths +
        spack_ldlibs)


def test_cpp_flags(wrapper_flags):
    check_args(
        cpp, test_args,
        ['cpp'] +
        spack_cppflags +
        test_include_paths +
        test_library_paths +
        test_args_without_paths)


def test_cc_flags(wrapper_flags):
    check_args(
        cc, test_args,
        [real_cc] +
        spack_cppflags +
        spack_cflags +
        spack_ldflags +
        test_include_paths +
        test_library_paths +
        ['-Wl,--disable-new-dtags'] +
        test_wl_rpaths +
        test_args_without_paths +
        spack_ldlibs)


def test_cxx_flags(wrapper_flags):
    check_args(
        cxx, test_args,
        [real_cc] +
        spack_cppflags +
        spack_cxxflags +
        spack_ldflags +
        test_include_paths +
        test_library_paths +
        ['-Wl,--disable-new-dtags'] +
        test_wl_rpaths +
        test_args_without_paths +
        spack_ldlibs)


def test_fc_flags(wrapper_flags):
    check_args(
        fc, test_args,
        [real_cc] +
        spack_fflags +
        spack_cppflags +
        spack_ldflags +
        test_include_paths +
        test_library_paths +
        ['-Wl,--disable-new-dtags'] +
        test_wl_rpaths +
        test_args_without_paths +
        spack_ldlibs)


def test_dep_rpath():
    """Ensure RPATHs for root package are added."""
    check_args(
        cc, test_args,
        [real_cc] +
        test_include_paths +
        test_library_paths +
        ['-Wl,--disable-new-dtags'] +
        test_wl_rpaths +
        test_args_without_paths)


def test_dep_include():
    """Ensure a single dependency include directory is added."""
    with set_env(SPACK_INCLUDE_DIRS='x'):
        check_args(
            cc, test_args,
            [real_cc] +
            test_include_paths +
            ['-Ix'] +
            test_library_paths +
            ['-Wl,--disable-new-dtags'] +
            test_wl_rpaths +
            test_args_without_paths)


def test_dep_lib():
    """Ensure a single dependency RPATH is added."""
    with set_env(SPACK_LINK_DIRS='x',
                 SPACK_RPATH_DIRS='x'):
        check_args(
            cc, test_args,
            [real_cc] +
            test_include_paths +
            test_library_paths +
            ['-Lx'] +
            ['-Wl,--disable-new-dtags'] +
            test_wl_rpaths +
            ['-Wl,-rpath,x'] +
            test_args_without_paths)


def test_dep_lib_no_rpath():
    """Ensure a single dependency link flag is added with no dep RPATH."""
    with set_env(SPACK_LINK_DIRS='x'):
        check_args(
            cc, test_args,
            [real_cc] +
            test_include_paths +
            test_library_paths +
            ['-Lx'] +
            ['-Wl,--disable-new-dtags'] +
            test_wl_rpaths +
            test_args_without_paths)


def test_dep_lib_no_lib():
    """Ensure a single dependency RPATH is added with no -L."""
    with set_env(SPACK_RPATH_DIRS='x'):
        check_args(
            cc, test_args,
            [real_cc] +
            test_include_paths +
            test_library_paths +
            ['-Wl,--disable-new-dtags'] +
            test_wl_rpaths +
            ['-Wl,-rpath,x'] +
            test_args_without_paths)


def test_ccld_deps():
    """Ensure all flags are added in ccld mode."""
    with set_env(SPACK_INCLUDE_DIRS='xinc:yinc:zinc',
                 SPACK_RPATH_DIRS='xlib:ylib:zlib',
                 SPACK_LINK_DIRS='xlib:ylib:zlib'):
        check_args(
            cc, test_args,
            [real_cc] +
            test_include_paths +
            ['-Ixinc',
             '-Iyinc',
             '-Izinc'] +
            test_library_paths +
            ['-Lxlib',
             '-Lylib',
             '-Lzlib'] +
            ['-Wl,--disable-new-dtags'] +
            test_wl_rpaths +
            ['-Wl,-rpath,xlib',
             '-Wl,-rpath,ylib',
             '-Wl,-rpath,zlib'] +
            test_args_without_paths)


def test_ccld_deps_isystem():
    """Ensure all flags are added in ccld mode.
       When a build uses -isystem, Spack should inject it's
       include paths using -isystem. Spack will insert these
       after any provided -isystem includes, but before any
       system directories included using -isystem"""
    with set_env(SPACK_INCLUDE_DIRS='xinc:yinc:zinc',
                 SPACK_RPATH_DIRS='xlib:ylib:zlib',
                 SPACK_LINK_DIRS='xlib:ylib:zlib'):
        mytest_args = test_args + ['-isystem', 'fooinc']
        check_args(
            cc, mytest_args,
            [real_cc] +
            test_include_paths +
            ['-isystem', 'fooinc',
             '-isystem', 'xinc',
             '-isystem', 'yinc',
             '-isystem', 'zinc'] +
            test_library_paths +
            ['-Lxlib',
             '-Lylib',
             '-Lzlib'] +
            ['-Wl,--disable-new-dtags'] +
            test_wl_rpaths +
            ['-Wl,-rpath,xlib',
             '-Wl,-rpath,ylib',
             '-Wl,-rpath,zlib'] +
            test_args_without_paths)


def test_cc_deps():
    """Ensure -L and RPATHs are not added in cc mode."""
    with set_env(SPACK_INCLUDE_DIRS='xinc:yinc:zinc',
                 SPACK_RPATH_DIRS='xlib:ylib:zlib',
                 SPACK_LINK_DIRS='xlib:ylib:zlib'):
        check_args(
            cc, ['-c'] + test_args,
            [real_cc] +
            test_include_paths +
            ['-Ixinc',
             '-Iyinc',
             '-Izinc'] +
            test_library_paths +
            ['-c'] +
            test_args_without_paths)


def test_ccld_with_system_dirs():
    """Ensure all flags are added in ccld mode."""
    with set_env(SPACK_INCLUDE_DIRS='xinc:yinc:zinc',
                 SPACK_RPATH_DIRS='xlib:ylib:zlib',
                 SPACK_LINK_DIRS='xlib:ylib:zlib'):

        sys_path_args = ['-I/usr/include',
                         '-L/usr/local/lib',
                         '-Wl,-rpath,/usr/lib64',
                         '-I/usr/local/include',
                         '-L/lib64/']
        check_args(
            cc, sys_path_args + test_args,
            [real_cc] +
            test_include_paths +
            ['-Ixinc',
             '-Iyinc',
             '-Izinc'] +
            ['-I/usr/include',
             '-I/usr/local/include'] +
            test_library_paths +
            ['-Lxlib',
             '-Lylib',
             '-Lzlib'] +
            ['-L/usr/local/lib',
             '-L/lib64/'] +
            ['-Wl,--disable-new-dtags'] +
            test_wl_rpaths +
            ['-Wl,-rpath,xlib',
             '-Wl,-rpath,ylib',
             '-Wl,-rpath,zlib'] +
            ['-Wl,-rpath,/usr/lib64'] +
            test_args_without_paths)


def test_ccld_with_system_dirs_isystem():
    """Ensure all flags are added in ccld mode.
       Ensure that includes are in the proper
       place when a build uses -isystem, and uses
       system directories in the include paths"""
    with set_env(SPACK_INCLUDE_DIRS='xinc:yinc:zinc',
                 SPACK_RPATH_DIRS='xlib:ylib:zlib',
                 SPACK_LINK_DIRS='xlib:ylib:zlib'):

        sys_path_args = ['-isystem', '/usr/include',
                         '-L/usr/local/lib',
                         '-Wl,-rpath,/usr/lib64',
                         '-isystem', '/usr/local/include',
                         '-L/lib64/']
        check_args(
            cc, sys_path_args + test_args,
            [real_cc] +
            test_include_paths +
            ['-isystem', 'xinc',
             '-isystem', 'yinc',
             '-isystem', 'zinc'] +
            ['-isystem', '/usr/include',
             '-isystem', '/usr/local/include'] +
            test_library_paths +
            ['-Lxlib',
             '-Lylib',
             '-Lzlib'] +
            ['-L/usr/local/lib',
             '-L/lib64/'] +
            ['-Wl,--disable-new-dtags'] +
            test_wl_rpaths +
            ['-Wl,-rpath,xlib',
             '-Wl,-rpath,ylib',
             '-Wl,-rpath,zlib'] +
            ['-Wl,-rpath,/usr/lib64'] +
            test_args_without_paths)


def test_ld_deps():
    """Ensure no (extra) -I args or -Wl, are passed in ld mode."""
    with set_env(SPACK_INCLUDE_DIRS='xinc:yinc:zinc',
                 SPACK_RPATH_DIRS='xlib:ylib:zlib',
                 SPACK_LINK_DIRS='xlib:ylib:zlib'):
        check_args(
            ld, test_args,
            ['ld'] +
            test_include_paths +
            test_library_paths +
            ['-Lxlib',
             '-Lylib',
             '-Lzlib'] +
            ['--disable-new-dtags'] +
            test_rpaths +
            ['-rpath', 'xlib',
             '-rpath', 'ylib',
             '-rpath', 'zlib'] +
            test_args_without_paths)


def test_ld_deps_no_rpath():
    """Ensure SPACK_LINK_DEPS controls -L for ld."""
    with set_env(SPACK_INCLUDE_DIRS='xinc:yinc:zinc',
                 SPACK_LINK_DIRS='xlib:ylib:zlib'):
        check_args(
            ld, test_args,
            ['ld'] +
            test_include_paths +
            test_library_paths +
            ['-Lxlib',
             '-Lylib',
             '-Lzlib'] +
            ['--disable-new-dtags'] +
            test_rpaths +
            test_args_without_paths)


def test_ld_deps_no_link():
    """Ensure SPACK_RPATH_DEPS controls -rpath for ld."""
    with set_env(SPACK_INCLUDE_DIRS='xinc:yinc:zinc',
                 SPACK_RPATH_DIRS='xlib:ylib:zlib'):
        check_args(
            ld, test_args,
            ['ld'] +
            test_include_paths +
            test_library_paths +
            ['--disable-new-dtags'] +
            test_rpaths +
            ['-rpath', 'xlib',
             '-rpath', 'ylib',
             '-rpath', 'zlib'] +
            test_args_without_paths)


def test_ld_deps_partial():
    """Make sure ld -r (partial link) is handled correctly on OS's where it
       doesn't accept rpaths.
    """
    with set_env(SPACK_INCLUDE_DIRS='xinc',
                 SPACK_RPATH_DIRS='xlib',
                 SPACK_LINK_DIRS='xlib'):
        # TODO: do we need to add RPATHs on other platforms like Linux?
        # TODO: Can't we treat them the same?
        os.environ['SPACK_SHORT_SPEC'] = "foo@1.2=linux-x86_64"
        check_args(
            ld, ['-r'] + test_args,
            ['ld'] +
            test_include_paths +
            test_library_paths +
            ['-Lxlib'] +
            ['--disable-new-dtags'] +
            test_rpaths +
            ['-rpath', 'xlib'] +
            ['-r'] +
            test_args_without_paths)

        # rpaths from the underlying command will still appear
        # Spack will not add its own rpaths.
        os.environ['SPACK_SHORT_SPEC'] = "foo@1.2=darwin-x86_64"
        check_args(
            ld, ['-r'] + test_args,
            ['ld'] +
            headerpad +
            test_include_paths +
            test_library_paths +
            ['-Lxlib'] +
            ['--disable-new-dtags'] +
            test_rpaths +
            ['-r'] +
            test_args_without_paths)


def test_ccache_prepend_for_cc():
    with set_env(SPACK_CCACHE_BINARY='ccache'):
        os.environ['SPACK_SHORT_SPEC'] = "foo@1.2=linux-x86_64"
        check_args(
            cc, test_args,
            ['ccache'] +  # ccache prepended in cc mode
            [real_cc] +
            test_include_paths +
            test_library_paths +
            ['-Wl,--disable-new-dtags'] +
            test_wl_rpaths +
            test_args_without_paths)
        os.environ['SPACK_SHORT_SPEC'] = "foo@1.2=darwin-x86_64"
        check_args(
            cc, test_args,
            ['ccache'] +  # ccache prepended in cc mode
            [real_cc] +
            lheaderpad +
            test_include_paths +
            test_library_paths +
            ['-Wl,--disable-new-dtags'] +
            test_wl_rpaths +
            test_args_without_paths)


def test_no_ccache_prepend_for_fc():
    os.environ['SPACK_SHORT_SPEC'] = "foo@1.2=linux-x86_64"
    check_args(
        fc, test_args,
        # no ccache for Fortran
        [real_cc] +
        test_include_paths +
        test_library_paths +
        ['-Wl,--disable-new-dtags'] +
        test_wl_rpaths +
        test_args_without_paths)
    os.environ['SPACK_SHORT_SPEC'] = "foo@1.2=darwin-x86_64"
    check_args(
        fc, test_args,
        # no ccache for Fortran
        [real_cc] +
        lheaderpad +
        test_include_paths +
        test_library_paths +
        ['-Wl,--disable-new-dtags'] +
        test_wl_rpaths +
        test_args_without_paths)


@pytest.mark.regression('9160')
def test_disable_new_dtags(wrapper_flags):
    with set_env(SPACK_TEST_COMMAND='dump-args'):
        result = ld(*test_args, output=str).strip().split('\n')
        assert '--disable-new-dtags' in result
        result = cc(*test_args, output=str).strip().split('\n')
        assert '-Wl,--disable-new-dtags' in result


@pytest.mark.regression('9160')
def test_filter_enable_new_dtags(wrapper_flags):
    with set_env(SPACK_TEST_COMMAND='dump-args'):
        result = ld(*(test_args + ['--enable-new-dtags']), output=str)
        result = result.strip().split('\n')
        assert '--enable-new-dtags' not in result

        result = cc(*(test_args + ['-Wl,--enable-new-dtags']), output=str)
        result = result.strip().split('\n')
        assert '-Wl,--enable-new-dtags' not in result
