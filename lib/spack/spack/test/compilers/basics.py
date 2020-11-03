# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Test basic behavior of compilers in Spack"""
import pytest

import sys
import os
import shutil

from copy import copy
from six import iteritems

import llnl.util.filesystem as fs

import spack.spec
import spack.compiler
import spack.compilers as compilers
import spack.spec
import spack.util.environment

from spack.compiler import Compiler
from spack.util.executable import ProcessError


@pytest.fixture()
def make_args_for_version(monkeypatch):

    def _factory(version, path='/usr/bin/gcc'):
        class MockOs(object):
            pass

        compiler_name = 'gcc'
        compiler_cls = compilers.class_for_compiler_name(compiler_name)
        monkeypatch.setattr(compiler_cls, 'cc_version', lambda x: version)

        compiler_id = compilers.CompilerID(
            os=MockOs, compiler_name=compiler_name, version=None
        )
        variation = compilers.NameVariation(prefix='', suffix='')
        return compilers.DetectVersionArgs(
            id=compiler_id, variation=variation, language='cc', path=path
        )

    return _factory


def test_multiple_conflicting_compiler_definitions(mutable_config):
    compiler_def = {
        'compiler': {
            'flags': {},
            'modules': [],
            'paths': {
                'cc': 'cc',
                'cxx': 'cxx',
                'f77': 'null',
                'fc': 'null'},
            'extra_rpaths': [],
            'operating_system': 'test',
            'target': 'test',
            'environment': {},
            'spec': 'clang@0.0.0'}}

    compiler_config = [compiler_def, compiler_def]
    compiler_config[0]['compiler']['paths']['f77'] = 'f77'
    mutable_config.update_config('compilers', compiler_config)

    arch_spec = spack.spec.ArchSpec(('test', 'test', 'test'))
    cspec = compiler_config[0]['compiler']['spec']
    cmp = compilers.compiler_for_spec(cspec, arch_spec)
    assert cmp.f77 == 'f77'


def test_get_compiler_duplicates(config):
    # In this case there is only one instance of the specified compiler in
    # the test configuration (so it is not actually a duplicate), but the
    # method behaves the same.
    cfg_file_to_duplicates = compilers.get_compiler_duplicates(
        'gcc@4.5.0', spack.spec.ArchSpec('cray-CNL-xeon'))

    assert len(cfg_file_to_duplicates) == 1
    cfg_file, duplicates = next(iteritems(cfg_file_to_duplicates))
    assert len(duplicates) == 1


def test_all_compilers(config):
    all_compilers = compilers.all_compilers()
    filtered = [x for x in all_compilers if str(x.spec) == 'clang@3.3']
    filtered = [x for x in filtered if x.operating_system == 'SuSE11']
    assert len(filtered) == 1


@pytest.mark.skipif(
    sys.version_info[0] == 2, reason='make_args_for_version requires python 3'
)
@pytest.mark.parametrize('input_version,expected_version,expected_error', [
    (None, None,  "Couldn't get version for compiler /usr/bin/gcc"),
    ('4.9', '4.9', None)
])
def test_version_detection_is_empty(
        make_args_for_version, input_version, expected_version, expected_error
):
    args = make_args_for_version(version=input_version)
    result, error = compilers.detect_version(args)
    if not error:
        assert result.id.version == expected_version

    assert error == expected_error


def test_compiler_flags_from_config_are_grouped():
    compiler_entry = {
        'spec': 'intel@17.0.2',
        'operating_system': 'foo-os',
        'paths': {
            'cc': 'cc-path',
            'cxx': 'cxx-path',
            'fc': None,
            'f77': None
        },
        'flags': {
            'cflags': '-O0 -foo-flag foo-val'
        },
        'modules': None
    }

    compiler = compilers.compiler_from_dict(compiler_entry)
    assert any(x == '-foo-flag foo-val' for x in compiler.flags['cflags'])


# Test behavior of flags and UnsupportedCompilerFlag.

# Utility function to test most flags.
default_compiler_entry = {
    'spec': 'apple-clang@2.0.0',
    'operating_system': 'foo-os',
    'paths': {
        'cc': 'cc-path',
        'cxx': 'cxx-path',
        'fc': 'fc-path',
        'f77': 'f77-path'
    },
    'flags': {},
    'modules': None
}


# Fake up a mock compiler where everything is defaulted.
class MockCompiler(Compiler):
    def __init__(self):
        super(MockCompiler, self).__init__(
            cspec="badcompiler@1.0.0",
            operating_system=default_compiler_entry['operating_system'],
            target=None,
            paths=[default_compiler_entry['paths']['cc'],
                   default_compiler_entry['paths']['cxx'],
                   default_compiler_entry['paths']['fc'],
                   default_compiler_entry['paths']['f77']],
            environment={})

    def _get_compiler_link_paths(self, paths):
        # Mock os.path.isdir so the link paths don't have to exist
        old_isdir = os.path.isdir
        os.path.isdir = lambda x: True
        ret = super(MockCompiler, self)._get_compiler_link_paths(paths)
        os.path.isdir = old_isdir
        return ret

    @property
    def name(self):
        return "mockcompiler"

    @property
    def version(self):
        return "1.0.0"

    _verbose_flag = "--verbose"

    @property
    def verbose_flag(self):
        return self._verbose_flag

    required_libs = ['libgfortran']


def test_implicit_rpaths(dirs_with_libfiles, monkeypatch):
    lib_to_dirs, all_dirs = dirs_with_libfiles

    def try_all_dirs(*args):
        return all_dirs

    monkeypatch.setattr(MockCompiler, '_get_compiler_link_paths', try_all_dirs)

    expected_rpaths = set(lib_to_dirs['libstdc++'] +
                          lib_to_dirs['libgfortran'])

    compiler = MockCompiler()
    retrieved_rpaths = compiler.implicit_rpaths()
    assert set(retrieved_rpaths) == expected_rpaths


no_flag_dirs = ['/path/to/first/lib', '/path/to/second/lib64']
no_flag_output = 'ld -L%s -L%s' % tuple(no_flag_dirs)

flag_dirs = ['/path/to/first/with/flag/lib', '/path/to/second/lib64']
flag_output = 'ld -L%s -L%s' % tuple(flag_dirs)


def call_compiler(exe, *args, **kwargs):
    # This method can replace Executable.__call__ to emulate a compiler that
    # changes libraries depending on a flag.
    if '--correct-flag' in exe.exe:
        return flag_output
    return no_flag_output


@pytest.mark.parametrize('exe,flagname', [
    ('cxx', ''),
    ('cxx', 'cxxflags'),
    ('cxx', 'cppflags'),
    ('cxx', 'ldflags'),
    ('cc', ''),
    ('cc', 'cflags'),
    ('cc', 'cppflags'),
    ('fc', ''),
    ('fc', 'fflags'),
    ('f77', 'fflags'),
    ('f77', 'cppflags'),
])
@pytest.mark.enable_compiler_link_paths
def test_get_compiler_link_paths(monkeypatch, exe, flagname):
    # create fake compiler that emits mock verbose output
    compiler = MockCompiler()
    monkeypatch.setattr(
        spack.util.executable.Executable, '__call__', call_compiler)

    # Grab executable path to test
    paths = [getattr(compiler, exe)]

    # Test without flags
    dirs = compiler._get_compiler_link_paths(paths)
    assert dirs == no_flag_dirs

    if flagname:
        # set flags and test
        setattr(compiler, 'flags', {flagname: ['--correct-flag']})
        dirs = compiler._get_compiler_link_paths(paths)
        assert dirs == flag_dirs


def test_get_compiler_link_paths_no_path():
    compiler = MockCompiler()
    compiler.cc = None
    compiler.cxx = None
    compiler.f77 = None
    compiler.fc = None

    dirs = compiler._get_compiler_link_paths([compiler.cxx])
    assert dirs == []


def test_get_compiler_link_paths_no_verbose_flag():
    compiler = MockCompiler()
    compiler._verbose_flag = None

    dirs = compiler._get_compiler_link_paths([compiler.cxx])
    assert dirs == []


@pytest.mark.enable_compiler_link_paths
def test_get_compiler_link_paths_load_env(working_env, monkeypatch, tmpdir):
    gcc = str(tmpdir.join('gcc'))
    with open(gcc, 'w') as f:
        f.write("""#!/bin/bash
if [[ $ENV_SET == "1" && $MODULE_LOADED == "1" ]]; then
  echo '""" + no_flag_output + """'
fi
""")
    fs.set_executable(gcc)

    # Set module load to turn compiler on
    def module(*args):
        if args[0] == 'show':
            return ''
        elif args[0] == 'load':
            os.environ['MODULE_LOADED'] = "1"
    monkeypatch.setattr(spack.util.module_cmd, 'module', module)

    compiler = MockCompiler()
    compiler.environment = {'set': {'ENV_SET': '1'}}
    compiler.modules = ['turn_on']

    dirs = compiler._get_compiler_link_paths([gcc])
    assert dirs == no_flag_dirs


# Get the desired flag from the specified compiler spec.
def flag_value(flag, spec):
    compiler = None
    if spec is None:
        compiler = MockCompiler()
    else:
        compiler_entry = copy(default_compiler_entry)
        compiler_entry['spec'] = spec
        compiler = compilers.compiler_from_dict(compiler_entry)

    return getattr(compiler, flag)


# Utility function to verify that the expected exception is thrown for
# an unsupported flag.
def unsupported_flag_test(flag, spec=None):
    caught_exception = None
    try:
        flag_value(flag, spec)
    except spack.compiler.UnsupportedCompilerFlag:
        caught_exception = True

    assert(caught_exception and "Expected exception not thrown.")


# Verify the expected flag value for the give compiler spec.
def supported_flag_test(flag, flag_value_ref, spec=None):
    assert(flag_value(flag, spec) == flag_value_ref)


# Tests for UnsupportedCompilerFlag exceptions from default
# implementations of flags.
def test_default_flags():
    supported_flag_test("cc_rpath_arg",  "-Wl,-rpath,")
    supported_flag_test("cxx_rpath_arg", "-Wl,-rpath,")
    supported_flag_test("f77_rpath_arg", "-Wl,-rpath,")
    supported_flag_test("fc_rpath_arg",  "-Wl,-rpath,")
    supported_flag_test("linker_arg", "-Wl,")
    unsupported_flag_test("openmp_flag")
    unsupported_flag_test("cxx11_flag")
    unsupported_flag_test("cxx14_flag")
    unsupported_flag_test("cxx17_flag")
    supported_flag_test("cxx98_flag", "")
    unsupported_flag_test("c99_flag")
    unsupported_flag_test("c11_flag")
    supported_flag_test("cc_pic_flag",  "-fPIC")
    supported_flag_test("cxx_pic_flag", "-fPIC")
    supported_flag_test("f77_pic_flag", "-fPIC")
    supported_flag_test("fc_pic_flag",  "-fPIC")
    supported_flag_test("debug_flags", ["-g"])
    supported_flag_test("opt_flags", ["-O", "-O0", "-O1", "-O2", "-O3"])


# Verify behavior of particular compiler definitions.
def test_arm_flags():
    supported_flag_test("openmp_flag", "-fopenmp", "arm@1.0")
    supported_flag_test("cxx11_flag", "-std=c++11", "arm@1.0")
    supported_flag_test("cxx14_flag", "-std=c++14", "arm@1.0")
    supported_flag_test("cxx17_flag", "-std=c++1z", "arm@1.0")
    supported_flag_test("c99_flag", "-std=c99", "arm@1.0")
    supported_flag_test("c11_flag", "-std=c11", "arm@1.0")
    supported_flag_test("cc_pic_flag",  "-fPIC", "arm@1.0")
    supported_flag_test("cxx_pic_flag", "-fPIC", "arm@1.0")
    supported_flag_test("f77_pic_flag", "-fPIC", "arm@1.0")
    supported_flag_test("fc_pic_flag",  "-fPIC", "arm@1.0")
    supported_flag_test("opt_flags",
                        ['-O', '-O0', '-O1', '-O2', '-O3', '-Ofast'],
                        'arm@1.0')


def test_cce_flags():
    supported_flag_test("version_argument", "--version", "cce@9.0.1")
    supported_flag_test("version_argument", "-V", "cce@9.0.1-classic")
    supported_flag_test("openmp_flag", "-fopenmp", "cce@9.0.1")
    supported_flag_test("openmp_flag", "-h omp", "cce@9.0.1-classic")
    supported_flag_test("openmp_flag", "-h omp", "cce@1.0")
    supported_flag_test("cxx11_flag", "-std=c++11", "cce@9.0.1")
    supported_flag_test("cxx11_flag", "-h std=c++11", "cce@9.0.1-classic")
    supported_flag_test("cxx11_flag", "-h std=c++11", "cce@1.0")
    unsupported_flag_test("c99_flag", "cce@8.0")
    supported_flag_test("c99_flag", "-std=c99", "cce@9.0.1")
    supported_flag_test("c99_flag", "-h c99,noconform,gnu", "cce@8.1")
    supported_flag_test("c99_flag", "-h std=c99,noconform,gnu", "cce@8.4")
    unsupported_flag_test("c11_flag", "cce@8.4")
    supported_flag_test("c11_flag", "-std=c11", "cce@9.0.1")
    supported_flag_test("c11_flag", "-h std=c11,noconform,gnu", "cce@8.5")
    supported_flag_test("cc_pic_flag",  "-h PIC", "cce@1.0")
    supported_flag_test("cxx_pic_flag", "-h PIC", "cce@1.0")
    supported_flag_test("f77_pic_flag", "-h PIC", "cce@1.0")
    supported_flag_test("fc_pic_flag",  "-h PIC", "cce@1.0")
    supported_flag_test("cc_pic_flag",  "-fPIC", "cce@9.1.0")
    supported_flag_test("cxx_pic_flag", "-fPIC", "cce@9.1.0")
    supported_flag_test("f77_pic_flag", "-fPIC", "cce@9.1.0")
    supported_flag_test("fc_pic_flag",  "-fPIC", "cce@9.1.0")
    supported_flag_test("debug_flags", ['-g', '-G0', '-G1', '-G2', '-Gfast'],
                        'cce@1.0')


def test_apple_clang_flags():
    supported_flag_test(
        "openmp_flag", "-Xpreprocessor -fopenmp", "apple-clang@2.0.0"
    )
    unsupported_flag_test("cxx11_flag", "apple-clang@2.0.0")
    supported_flag_test("cxx11_flag", "-std=c++11", "apple-clang@4.0.0")
    unsupported_flag_test("cxx14_flag", "apple-clang@5.0.0")
    supported_flag_test("cxx14_flag", "-std=c++1y", "apple-clang@5.1.0")
    supported_flag_test("cxx14_flag", "-std=c++14", "apple-clang@6.1.0")
    unsupported_flag_test("cxx17_flag", "apple-clang@6.0.0")
    supported_flag_test("cxx17_flag", "-std=c++1z", "apple-clang@6.1.0")
    supported_flag_test("c99_flag", "-std=c99", "apple-clang@6.1.0")
    unsupported_flag_test("c11_flag", "apple-clang@6.0.0")
    supported_flag_test("c11_flag", "-std=c11", "apple-clang@6.1.0")
    supported_flag_test("cc_pic_flag", "-fPIC", "apple-clang@2.0.0")
    supported_flag_test("cxx_pic_flag", "-fPIC", "apple-clang@2.0.0")
    supported_flag_test("f77_pic_flag", "-fPIC", "apple-clang@2.0.0")
    supported_flag_test("fc_pic_flag", "-fPIC", "apple-clang@2.0.0")


def test_clang_flags():
    supported_flag_test("version_argument", "--version", "clang@foo.bar")
    supported_flag_test("openmp_flag", "-fopenmp", "clang@3.3")
    unsupported_flag_test("cxx11_flag", "clang@3.2")
    supported_flag_test("cxx11_flag", "-std=c++11", "clang@3.3")
    unsupported_flag_test("cxx14_flag", "clang@3.3")
    supported_flag_test("cxx14_flag", "-std=c++1y", "clang@3.4")
    supported_flag_test("cxx14_flag", "-std=c++14", "clang@3.5")
    unsupported_flag_test("cxx17_flag", "clang@3.4")
    supported_flag_test("cxx17_flag", "-std=c++1z", "clang@3.5")
    supported_flag_test("cxx17_flag", "-std=c++17", "clang@5.0")
    supported_flag_test("c99_flag", "-std=c99", "clang@3.3")
    unsupported_flag_test("c11_flag", "clang@6.0.0")
    supported_flag_test("c11_flag", "-std=c11", "clang@6.1.0")
    supported_flag_test("cc_pic_flag",  "-fPIC", "clang@3.3")
    supported_flag_test("cxx_pic_flag", "-fPIC", "clang@3.3")
    supported_flag_test("f77_pic_flag", "-fPIC", "clang@3.3")
    supported_flag_test("fc_pic_flag",  "-fPIC", "clang@3.3")
    supported_flag_test("debug_flags",
                        ['-gcodeview', '-gdwarf-2', '-gdwarf-3', '-gdwarf-4',
                         '-gdwarf-5', '-gline-tables-only', '-gmodules', '-gz',
                         '-g'],
                        'clang@3.3')
    supported_flag_test("opt_flags",
                        ['-O0', '-O1', '-O2', '-O3', '-Ofast', '-Os', '-Oz',
                         '-Og', '-O', '-O4'],
                        'clang@3.3')


def test_aocc_flags():
    supported_flag_test("debug_flags",
                        ['-gcodeview', '-gdwarf-2', '-gdwarf-3',
                         '-gdwarf-4', '-gdwarf-5', '-gline-tables-only',
                         '-gmodules', '-gz', '-g'],
                        'aocc@2.2.0')
    supported_flag_test("opt_flags",
                        ['-O0', '-O1', '-O2', '-O3', '-Ofast',
                         '-Os', '-Oz', '-Og',
                         '-O', '-O4'],
                        'aocc@2.2.0')
    supported_flag_test("openmp_flag", "-fopenmp", "aocc@2.2.0")
    supported_flag_test("cxx11_flag", "-std=c++11", "aocc@2.2.0")
    supported_flag_test("cxx14_flag", "-std=c++14", "aocc@2.2.0")
    supported_flag_test("cxx17_flag", "-std=c++17", "aocc@2.2.0")
    supported_flag_test("c99_flag", "-std=c99", "aocc@2.2.0")
    supported_flag_test("c11_flag", "-std=c11", "aocc@2.2.0")
    supported_flag_test("cc_pic_flag", "-fPIC", "aocc@2.2.0")
    supported_flag_test("cxx_pic_flag", "-fPIC", "aocc@2.2.0")
    supported_flag_test("f77_pic_flag", "-fPIC", "aocc@2.2.0")
    supported_flag_test("fc_pic_flag", "-fPIC", "aocc@2.2.0")
    supported_flag_test("version_argument", "--version", "aocc@2.2.0")


def test_fj_flags():
    supported_flag_test("openmp_flag", "-Kopenmp", "fj@4.0.0")
    supported_flag_test("cxx98_flag", "-std=c++98", "fj@4.0.0")
    supported_flag_test("cxx11_flag", "-std=c++11", "fj@4.0.0")
    supported_flag_test("cxx14_flag", "-std=c++14", "fj@4.0.0")
    supported_flag_test("c99_flag", "-std=c99", "fj@4.0.0")
    supported_flag_test("c11_flag", "-std=c11", "fj@4.0.0")
    supported_flag_test("cc_pic_flag",  "-KPIC", "fj@4.0.0")
    supported_flag_test("cxx_pic_flag", "-KPIC", "fj@4.0.0")
    supported_flag_test("f77_pic_flag", "-KPIC", "fj@4.0.0")
    supported_flag_test("fc_pic_flag",  "-KPIC", "fj@4.0.0")
    supported_flag_test("opt_flags", ['-O', '-O0', '-O1', '-O2', '-O3', '-O4'],
                        'fj@4.0.0')


def test_gcc_flags():
    supported_flag_test("openmp_flag", "-fopenmp", "gcc@4.1")
    supported_flag_test("cxx98_flag", "", "gcc@5.2")
    supported_flag_test("cxx98_flag", "-std=c++98", "gcc@6.0")
    unsupported_flag_test("cxx11_flag", "gcc@4.2")
    supported_flag_test("cxx11_flag", "-std=c++0x", "gcc@4.3")
    supported_flag_test("cxx11_flag", "-std=c++11", "gcc@4.7")
    unsupported_flag_test("cxx14_flag", "gcc@4.7")
    supported_flag_test("cxx14_flag", "-std=c++1y", "gcc@4.8")
    supported_flag_test("cxx14_flag", "-std=c++14", "gcc@4.9")
    supported_flag_test("cxx14_flag", "", "gcc@6.0")
    unsupported_flag_test("cxx17_flag", "gcc@4.9")
    supported_flag_test("cxx17_flag", "-std=c++1z", "gcc@5.0")
    supported_flag_test("cxx17_flag", "-std=c++17", "gcc@6.0")
    unsupported_flag_test("c99_flag", "gcc@4.4")
    supported_flag_test("c99_flag", "-std=c99", "gcc@4.5")
    unsupported_flag_test("c11_flag", "gcc@4.6")
    supported_flag_test("c11_flag", "-std=c11", "gcc@4.7")
    supported_flag_test("cc_pic_flag",  "-fPIC", "gcc@4.0")
    supported_flag_test("cxx_pic_flag", "-fPIC", "gcc@4.0")
    supported_flag_test("f77_pic_flag", "-fPIC", "gcc@4.0")
    supported_flag_test("fc_pic_flag",  "-fPIC", "gcc@4.0")
    supported_flag_test("stdcxx_libs", ("-lstdc++",), "gcc@4.1")
    supported_flag_test("debug_flags",
                        ['-g', '-gstabs+', '-gstabs', '-gxcoff+', '-gxcoff',
                         '-gvms'],
                        'gcc@4.0')
    supported_flag_test("opt_flags",
                        ['-O', '-O0', '-O1', '-O2', '-O3', '-Os', '-Ofast',
                         '-Og'],
                        'gcc@4.0')


def test_intel_flags():
    supported_flag_test("openmp_flag", "-openmp", "intel@15.0")
    supported_flag_test("openmp_flag", "-qopenmp", "intel@16.0")
    unsupported_flag_test("cxx11_flag", "intel@11.0")
    supported_flag_test("cxx11_flag", "-std=c++0x", "intel@12.0")
    supported_flag_test("cxx11_flag", "-std=c++11", "intel@13")
    unsupported_flag_test("cxx14_flag", "intel@14.0")
    supported_flag_test("cxx14_flag", "-std=c++1y", "intel@15.0")
    supported_flag_test("cxx14_flag", "-std=c++14", "intel@15.0.2")
    unsupported_flag_test("c99_flag", "intel@11.0")
    supported_flag_test("c99_flag", "-std=c99", "intel@12.0")
    unsupported_flag_test("c11_flag", "intel@15.0")
    supported_flag_test("c11_flag", "-std=c1x", "intel@16.0")
    supported_flag_test("cc_pic_flag",  "-fPIC", "intel@1.0")
    supported_flag_test("cxx_pic_flag", "-fPIC", "intel@1.0")
    supported_flag_test("f77_pic_flag", "-fPIC", "intel@1.0")
    supported_flag_test("fc_pic_flag",  "-fPIC", "intel@1.0")
    supported_flag_test("stdcxx_libs", ("-cxxlib",), "intel@1.0")
    supported_flag_test("debug_flags",
                        ['-debug', '-g', '-g0', '-g1', '-g2', '-g3'],
                        'intel@1.0')
    supported_flag_test("opt_flags",
                        ['-O', '-O0', '-O1', '-O2', '-O3', '-Ofast', '-Os'],
                        'intel@1.0')


def test_oneapi_flags():
    supported_flag_test("openmp_flag", "-qopenmp", "oneapi@2020.8.0.0827")
    supported_flag_test("cxx11_flag", "-std=c++11", "oneapi@2020.8.0.0827")
    supported_flag_test("cxx14_flag", "-std=c++14", "oneapi@2020.8.0.0827")
    supported_flag_test("c99_flag", "-std=c99", "oneapi@2020.8.0.0827")
    supported_flag_test("c11_flag", "-std=c1x", "oneapi@2020.8.0.0827")
    supported_flag_test("cc_pic_flag",  "-fPIC", "oneapi@2020.8.0.0827")
    supported_flag_test("cxx_pic_flag", "-fPIC", "oneapi@2020.8.0.0827")
    supported_flag_test("f77_pic_flag", "-fPIC", "oneapi@2020.8.0.0827")
    supported_flag_test("fc_pic_flag",  "-fPIC", "oneapi@2020.8.0.0827")
    supported_flag_test("stdcxx_libs", ("-cxxlib",), "oneapi@2020.8.0.0827")
    supported_flag_test("debug_flags",
                        ['-debug', '-g', '-g0', '-g1', '-g2', '-g3'],
                        'oneapi@2020.8.0.0827')
    supported_flag_test("opt_flags",
                        ['-O', '-O0', '-O1', '-O2', '-O3', '-Ofast', '-Os'],
                        'oneapi@2020.8.0.0827')


def test_nag_flags():
    supported_flag_test("openmp_flag", "-openmp", "nag@1.0")
    supported_flag_test("cxx11_flag", "-std=c++11", "nag@1.0")
    supported_flag_test("cc_pic_flag",  "-fPIC", "nag@1.0")
    supported_flag_test("cxx_pic_flag", "-fPIC", "nag@1.0")
    supported_flag_test("f77_pic_flag", "-PIC",  "nag@1.0")
    supported_flag_test("fc_pic_flag",  "-PIC",  "nag@1.0")
    supported_flag_test("cc_rpath_arg",  "-Wl,-rpath,", "nag@1.0")
    supported_flag_test("cxx_rpath_arg", "-Wl,-rpath,", "nag@1.0")
    supported_flag_test("f77_rpath_arg", "-Wl,-Wl,,-rpath,,", "nag@1.0")
    supported_flag_test("fc_rpath_arg",  "-Wl,-Wl,,-rpath,,", "nag@1.0")
    supported_flag_test("linker_arg", "-Wl,-Wl,,", "nag@1.0")
    supported_flag_test("debug_flags", ['-g', '-gline', '-g90'], 'nag@1.0')
    supported_flag_test("opt_flags", ['-O', '-O0', '-O1', '-O2', '-O3', '-O4'],
                        'nag@1.0')


def test_nvhpc_flags():
    supported_flag_test("openmp_flag", "-mp", "nvhpc@20.9")
    supported_flag_test("cxx11_flag", "--c++11", "nvhpc@20.9")
    supported_flag_test("cxx14_flag", "--c++14", "nvhpc@20.9")
    supported_flag_test("cxx17_flag", "--c++17", "nvhpc@20.9")
    supported_flag_test("c99_flag", "-c99", "nvhpc@20.9")
    supported_flag_test("c11_flag", "-c11", "nvhpc@20.9")
    supported_flag_test("cc_pic_flag",  "-fpic", "nvhpc@20.9")
    supported_flag_test("cxx_pic_flag", "-fpic", "nvhpc@20.9")
    supported_flag_test("f77_pic_flag", "-fpic", "nvhpc@20.9")
    supported_flag_test("fc_pic_flag",  "-fpic", "nvhpc@20.9")
    supported_flag_test("debug_flags", ['-g', '-gopt'], 'nvhpc@20.9')
    supported_flag_test("opt_flags", ['-O', '-O0', '-O1', '-O2', '-O3', '-O4'],
                        'nvhpc@20.9')
    supported_flag_test("stdcxx_libs", ('-c++libs',), 'nvhpc@20.9')


def test_pgi_flags():
    supported_flag_test("openmp_flag", "-mp", "pgi@1.0")
    supported_flag_test("cxx11_flag", "-std=c++11", "pgi@1.0")
    unsupported_flag_test("c99_flag", "pgi@12.9")
    supported_flag_test("c99_flag", "-c99", "pgi@12.10")
    unsupported_flag_test("c11_flag", "pgi@15.2")
    supported_flag_test("c11_flag", "-c11", "pgi@15.3")
    supported_flag_test("cc_pic_flag",  "-fpic", "pgi@1.0")
    supported_flag_test("cxx_pic_flag", "-fpic", "pgi@1.0")
    supported_flag_test("f77_pic_flag", "-fpic", "pgi@1.0")
    supported_flag_test("fc_pic_flag",  "-fpic", "pgi@1.0")
    supported_flag_test("debug_flags", ['-g', '-gopt'], 'pgi@1.0')
    supported_flag_test("opt_flags", ['-O', '-O0', '-O1', '-O2', '-O3', '-O4'],
                        'pgi@1.0')


def test_xl_flags():
    supported_flag_test("openmp_flag", "-qsmp=omp", "xl@1.0")
    unsupported_flag_test("cxx11_flag", "xl@13.0")
    supported_flag_test("cxx11_flag", "-qlanglvl=extended0x", "xl@13.1")
    unsupported_flag_test("c99_flag", "xl@10.0")
    supported_flag_test("c99_flag", "-qlanglvl=extc99", "xl@10.1")
    supported_flag_test("c99_flag", "-std=gnu99", "xl@13.1.1")
    unsupported_flag_test("c11_flag", "xl@12.0")
    supported_flag_test("c11_flag", "-qlanglvl=extc1x", "xl@12.1")
    supported_flag_test("c11_flag", "-std=gnu11", "xl@13.1.2")
    supported_flag_test("cc_pic_flag",  "-qpic", "xl@1.0")
    supported_flag_test("cxx_pic_flag", "-qpic", "xl@1.0")
    supported_flag_test("f77_pic_flag", "-qpic", "xl@1.0")
    supported_flag_test("fc_pic_flag",  "-qpic", "xl@1.0")
    supported_flag_test("fflags", "-qzerosize", "xl@1.0")
    supported_flag_test("debug_flags",
                        ['-g', '-g0', '-g1', '-g2', '-g8', '-g9'],
                        'xl@1.0')
    supported_flag_test("opt_flags",
                        ['-O', '-O0', '-O1', '-O2', '-O3', '-O4', '-O5',
                         '-Ofast'],
                        'xl@1.0')


def test_xl_r_flags():
    supported_flag_test("openmp_flag", "-qsmp=omp", "xl_r@1.0")
    unsupported_flag_test("cxx11_flag", "xl_r@13.0")
    supported_flag_test("cxx11_flag", "-qlanglvl=extended0x", "xl_r@13.1")
    unsupported_flag_test("c99_flag", "xl_r@10.0")
    supported_flag_test("c99_flag", "-qlanglvl=extc99", "xl_r@10.1")
    supported_flag_test("c99_flag", "-std=gnu99", "xl_r@13.1.1")
    unsupported_flag_test("c11_flag", "xl_r@12.0")
    supported_flag_test("c11_flag", "-qlanglvl=extc1x", "xl_r@12.1")
    supported_flag_test("c11_flag", "-std=gnu11", "xl_r@13.1.2")
    supported_flag_test("cc_pic_flag",  "-qpic", "xl_r@1.0")
    supported_flag_test("cxx_pic_flag", "-qpic", "xl_r@1.0")
    supported_flag_test("f77_pic_flag", "-qpic", "xl_r@1.0")
    supported_flag_test("fc_pic_flag",  "-qpic", "xl_r@1.0")
    supported_flag_test("fflags", "-qzerosize", "xl_r@1.0")
    supported_flag_test("debug_flags",
                        ['-g', '-g0', '-g1', '-g2', '-g8', '-g9'],
                        'xl@1.0')
    supported_flag_test("opt_flags",
                        ['-O', '-O0', '-O1', '-O2', '-O3', '-O4', '-O5',
                         '-Ofast'],
                        'xl@1.0')


@pytest.mark.parametrize('compiler_spec,expected_result', [
    ('gcc@4.7.2', False), ('clang@3.3', False), ('clang@8.0.0', True)
])
def test_detecting_mixed_toolchains(compiler_spec, expected_result, config):
    compiler = spack.compilers.compilers_for_spec(compiler_spec).pop()
    assert spack.compilers.is_mixed_toolchain(compiler) is expected_result


@pytest.mark.regression('14798,13733')
def test_raising_if_compiler_target_is_over_specific(config):
    # Compiler entry with an overly specific target
    compilers = [{'compiler': {
        'spec': 'gcc@9.0.1',
        'paths': {
            'cc': '/usr/bin/gcc-9',
            'cxx': '/usr/bin/g++-9',
            'f77': '/usr/bin/gfortran-9',
            'fc': '/usr/bin/gfortran-9'
        },
        'flags': {},
        'operating_system': 'ubuntu18.04',
        'target': 'haswell',
        'modules': [],
        'environment': {},
        'extra_rpaths': []
    }}]
    arch_spec = spack.spec.ArchSpec(('linux', 'ubuntu18.04', 'haswell'))
    with spack.config.override('compilers', compilers):
        cfg = spack.compilers.get_compiler_config()
        with pytest.raises(ValueError):
            spack.compilers.get_compilers(cfg, 'gcc@9.0.1', arch_spec)


def test_compiler_get_real_version(working_env, monkeypatch, tmpdir):
    # Test variables
    test_version = '2.2.2'

    # Create compiler
    gcc = str(tmpdir.join('gcc'))
    with open(gcc, 'w') as f:
        f.write("""#!/bin/bash
if [[ $CMP_ON == "1" ]]; then
    echo "$CMP_VER"
fi
""")
    fs.set_executable(gcc)

    # Add compiler to config
    compiler_info = {
        'spec': 'gcc@foo',
        'paths': {
            'cc': gcc,
            'cxx': None,
            'f77': None,
            'fc': None,
        },
        'flags': {},
        'operating_system': 'fake',
        'target': 'fake',
        'modules': ['turn_on'],
        'environment': {
            'set': {'CMP_VER': test_version},
        },
        'extra_rpaths': [],
    }
    compiler_dict = {'compiler': compiler_info}

    # Set module load to turn compiler on
    def module(*args):
        if args[0] == 'show':
            return ''
        elif args[0] == 'load':
            os.environ['CMP_ON'] = "1"
    monkeypatch.setattr(spack.util.module_cmd, 'module', module)

    # Run and confirm output
    compilers = spack.compilers.get_compilers([compiler_dict])
    assert len(compilers) == 1
    compiler = compilers[0]
    version = compiler.get_real_version()
    assert version == test_version


def test_compiler_get_real_version_fails(working_env, monkeypatch, tmpdir):
    # Test variables
    test_version = '2.2.2'

    # Create compiler
    gcc = str(tmpdir.join('gcc'))
    with open(gcc, 'w') as f:
        f.write("""#!/bin/bash
if [[ $CMP_ON == "1" ]]; then
    echo "$CMP_VER"
fi
""")
    fs.set_executable(gcc)

    # Add compiler to config
    compiler_info = {
        'spec': 'gcc@foo',
        'paths': {
            'cc': gcc,
            'cxx': None,
            'f77': None,
            'fc': None,
        },
        'flags': {},
        'operating_system': 'fake',
        'target': 'fake',
        'modules': ['turn_on'],
        'environment': {
            'set': {'CMP_VER': test_version},
        },
        'extra_rpaths': [],
    }
    compiler_dict = {'compiler': compiler_info}

    # Set module load to turn compiler on
    def module(*args):
        if args[0] == 'show':
            return ''
        elif args[0] == 'load':
            os.environ['SPACK_TEST_CMP_ON'] = "1"
    monkeypatch.setattr(spack.util.module_cmd, 'module', module)

    # Make compiler fail when getting implicit rpaths
    def _call(*args, **kwargs):
        raise ProcessError("Failed intentionally")
    monkeypatch.setattr(spack.util.executable.Executable, '__call__', _call)

    # Run and no change to environment
    compilers = spack.compilers.get_compilers([compiler_dict])
    assert len(compilers) == 1
    compiler = compilers[0]
    try:
        _ = compiler.get_real_version()
        assert False
    except ProcessError:
        # Confirm environment does not change after failed call
        assert 'SPACK_TEST_CMP_ON' not in os.environ


def test_compiler_flags_use_real_version(working_env, monkeypatch, tmpdir):
    # Create compiler
    gcc = str(tmpdir.join('gcc'))
    with open(gcc, 'w') as f:
        f.write("""#!/bin/bash
echo "4.4.4"
""")  # Version for which c++11 flag is -std=c++0x
    fs.set_executable(gcc)

    # Add compiler to config
    compiler_info = {
        'spec': 'gcc@foo',
        'paths': {
            'cc': gcc,
            'cxx': None,
            'f77': None,
            'fc': None,
        },
        'flags': {},
        'operating_system': 'fake',
        'target': 'fake',
        'modules': ['turn_on'],
        'environment': {},
        'extra_rpaths': [],
    }
    compiler_dict = {'compiler': compiler_info}

    # Run and confirm output
    compilers = spack.compilers.get_compilers([compiler_dict])
    assert len(compilers) == 1
    compiler = compilers[0]
    flag = compiler.cxx11_flag
    assert flag == '-std=c++0x'


def test_apple_clang_setup_environment(mock_executable, monkeypatch):
    """Test a code path that is taken only if the package uses
    Xcode on MacOS.
    """
    class MockPackage(object):
        use_xcode = False

    apple_clang_cls = spack.compilers.class_for_compiler_name('apple-clang')
    compiler = apple_clang_cls(
        spack.spec.CompilerSpec('apple-clang@11.0.0'), 'catalina', 'x86_64', [
            '/usr/bin/clang', '/usr/bin/clang++', None, None
        ]
    )
    env = spack.util.environment.EnvironmentModifications()
    # Check a package that doesn't use xcode and ensure we don't add changes
    # to the environment
    pkg = MockPackage()
    compiler.setup_custom_environment(pkg, env)
    assert not env

    # Prepare mock executables to fake the Xcode environment
    xcrun = mock_executable('xcrun', """
if [[ "$2" == "clang" ]] ; then
  echo "/Library/Developer/CommandLineTools/usr/bin/clang"
fi
if [[ "$2" == "clang++" ]] ; then
  echo "/Library/Developer/CommandLineTools/usr/bin/clang++"
fi
""")
    mock_executable('xcode-select', """
echo "/Library/Developer"
""")
    bin_dir = os.path.dirname(xcrun)
    monkeypatch.setenv('PATH', bin_dir, prepend=os.pathsep)

    def noop(*args, **kwargs):
        pass

    real_listdir = os.listdir

    def _listdir(path):
        if not os.path.exists(path):
            return []
        return real_listdir(path)

    # Set a few operations to noop
    monkeypatch.setattr(shutil, 'copytree', noop)
    monkeypatch.setattr(os, 'unlink', noop)
    monkeypatch.setattr(os, 'symlink', noop)
    monkeypatch.setattr(os, 'listdir', _listdir)

    # Qt is so far the only package that uses this code path, change
    # introduced in https://github.com/spack/spack/pull/1832
    pkg.use_xcode = True
    compiler.setup_custom_environment(pkg, env)
    assert len(env) == 3
    assert env.env_modifications[0].name == 'SPACK_CC'
    assert env.env_modifications[1].name == 'SPACK_CXX'
    assert env.env_modifications[2].name == 'DEVELOPER_DIR'


@pytest.mark.parametrize('xcode_select_output', [
    '', '/Library/Developer/CommandLineTools'
])
def test_xcode_not_available(
        xcode_select_output, mock_executable, monkeypatch
):
    # Prepare mock executables to fake the Xcode environment
    xcrun = mock_executable('xcrun', """
    if [[ "$2" == "clang" ]] ; then
      echo "/Library/Developer/CommandLineTools/usr/bin/clang"
    fi
    if [[ "$2" == "clang++" ]] ; then
      echo "/Library/Developer/CommandLineTools/usr/bin/clang++"
    fi
    """)
    mock_executable('xcode-select', """
    echo "{0}"
    """.format(xcode_select_output))
    bin_dir = os.path.dirname(xcrun)
    monkeypatch.setenv('PATH', bin_dir, prepend=os.pathsep)
    # Prepare compiler
    apple_clang_cls = spack.compilers.class_for_compiler_name('apple-clang')
    compiler = apple_clang_cls(
        spack.spec.CompilerSpec('apple-clang@11.0.0'), 'catalina', 'x86_64', [
            '/usr/bin/clang', '/usr/bin/clang++', None, None
        ]
    )
    env = spack.util.environment.EnvironmentModifications()

    class MockPackage(object):
        use_xcode = True

    pkg = MockPackage()
    with pytest.raises(OSError):
        compiler.setup_custom_environment(pkg, env)


@pytest.mark.enable_compiler_verification
def test_compiler_executable_verification_raises(tmpdir):
    compiler = MockCompiler()
    compiler.cc = '/this/path/does/not/exist'

    with pytest.raises(spack.compiler.CompilerAccessError):
        compiler.verify_executables()


@pytest.mark.enable_compiler_verification
def test_compiler_executable_verification_success(tmpdir):
    def prepare_executable(name):
        real = str(tmpdir.join('cc').ensure())
        fs.set_executable(real)
        setattr(compiler, name, real)

    # setup mock compiler with real paths
    compiler = MockCompiler()
    for name in ('cc', 'cxx', 'f77', 'fc'):
        prepare_executable(name)

    # testing that this doesn't raise an error because the paths exist and
    # are executable
    compiler.verify_executables()

    # Test that null entries don't fail
    compiler.cc = None
    compiler.verify_executables()
