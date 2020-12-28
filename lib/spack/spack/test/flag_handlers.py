# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pytest
import os

import spack.spec
import spack.repo
import spack.build_environment

from spack.package import inject_flags, env_flags, build_system_flags


@pytest.fixture()
def temp_env():
    old_env = os.environ.copy()
    yield
    os.environ.clear()
    os.environ.update(old_env)


def add_o3_to_build_system_cflags(pkg, name, flags):
    build_system_flags = []
    if name == 'cflags':
        build_system_flags.append('-O3')
    return (flags, None, build_system_flags)


@pytest.mark.usefixtures('config', 'mock_packages')
class TestFlagHandlers(object):
    def test_no_build_system_flags(self, temp_env):
        # Test that both autotools and cmake work getting no build_system flags
        s1 = spack.spec.Spec('cmake-client')
        s1.concretize()
        pkg1 = spack.repo.get(s1)
        spack.build_environment.setup_package(pkg1, False)

        s2 = spack.spec.Spec('patchelf')
        s2.concretize()
        pkg2 = spack.repo.get(s2)
        spack.build_environment.setup_package(pkg2, False)

        # Use cppflags as a canary
        assert 'SPACK_CPPFLAGS' not in os.environ
        assert 'CPPFLAGS' not in os.environ

    def test_unbound_method(self, temp_env):
        # Other tests test flag_handlers set as bound methods and functions.
        # This tests an unbound method in python2 (no change in python3).
        s = spack.spec.Spec('mpileaks cppflags=-g')
        s.concretize()
        pkg = spack.repo.get(s)
        pkg.flag_handler = pkg.__class__.inject_flags
        spack.build_environment.setup_package(pkg, False)
        assert os.environ['SPACK_CPPFLAGS'] == '-g'
        assert 'CPPFLAGS' not in os.environ

    def test_inject_flags(self, temp_env):
        s = spack.spec.Spec('mpileaks cppflags=-g')
        s.concretize()
        pkg = spack.repo.get(s)
        pkg.flag_handler = inject_flags
        spack.build_environment.setup_package(pkg, False)

        assert os.environ['SPACK_CPPFLAGS'] == '-g'
        assert 'CPPFLAGS' not in os.environ

    def test_env_flags(self, temp_env):
        s = spack.spec.Spec('mpileaks cppflags=-g')
        s.concretize()
        pkg = spack.repo.get(s)
        pkg.flag_handler = env_flags
        spack.build_environment.setup_package(pkg, False)

        assert os.environ['CPPFLAGS'] == '-g'
        assert 'SPACK_CPPFLAGS' not in os.environ

    def test_build_system_flags_cmake(self, temp_env):
        s = spack.spec.Spec('cmake-client cppflags=-g')
        s.concretize()
        pkg = spack.repo.get(s)
        pkg.flag_handler = build_system_flags
        spack.build_environment.setup_package(pkg, False)

        assert 'SPACK_CPPFLAGS' not in os.environ
        assert 'CPPFLAGS' not in os.environ

        expected = set(['-DCMAKE_C_FLAGS=-g', '-DCMAKE_CXX_FLAGS=-g',
                        '-DCMAKE_Fortran_FLAGS=-g'])
        assert set(pkg.cmake_flag_args) == expected

    def test_build_system_flags_autotools(self, temp_env):
        s = spack.spec.Spec('patchelf cppflags=-g')
        s.concretize()
        pkg = spack.repo.get(s)
        pkg.flag_handler = build_system_flags
        spack.build_environment.setup_package(pkg, False)

        assert 'SPACK_CPPFLAGS' not in os.environ
        assert 'CPPFLAGS' not in os.environ

        assert 'CPPFLAGS=-g' in pkg.configure_flag_args

    def test_build_system_flags_not_implemented(self, temp_env):
        s = spack.spec.Spec('mpileaks cppflags=-g')
        s.concretize()
        pkg = spack.repo.get(s)
        pkg.flag_handler = build_system_flags

        # Test the command line flags method raises a NotImplementedError
        try:
            spack.build_environment.setup_package(pkg, False)
            assert False
        except NotImplementedError:
            assert True

    def test_add_build_system_flags_autotools(self, temp_env):
        s = spack.spec.Spec('patchelf cppflags=-g')
        s.concretize()
        pkg = spack.repo.get(s)
        pkg.flag_handler = add_o3_to_build_system_cflags
        spack.build_environment.setup_package(pkg, False)

        assert '-g' in os.environ['SPACK_CPPFLAGS']
        assert 'CPPFLAGS' not in os.environ

        assert pkg.configure_flag_args == ['CFLAGS=-O3']

    def test_add_build_system_flags_cmake(self, temp_env):
        s = spack.spec.Spec('cmake-client cppflags=-g')
        s.concretize()
        pkg = spack.repo.get(s)
        pkg.flag_handler = add_o3_to_build_system_cflags
        spack.build_environment.setup_package(pkg, False)

        assert '-g' in os.environ['SPACK_CPPFLAGS']
        assert 'CPPFLAGS' not in os.environ

        assert pkg.cmake_flag_args == ['-DCMAKE_C_FLAGS=-O3']

    def test_ld_flags_cmake(self, temp_env):
        s = spack.spec.Spec('cmake-client ldflags=-mthreads')
        s.concretize()
        pkg = spack.repo.get(s)
        pkg.flag_handler = build_system_flags
        spack.build_environment.setup_package(pkg, False)

        assert 'SPACK_LDFLAGS' not in os.environ
        assert 'LDFLAGS' not in os.environ

        expected = set(['-DCMAKE_EXE_LINKER_FLAGS=-mthreads',
                        '-DCMAKE_MODULE_LINKER_FLAGS=-mthreads',
                        '-DCMAKE_SHARED_LINKER_FLAGS=-mthreads',
                        '-DCMAKE_STATIC_LINKER_FLAGS=-mthreads'])
        assert set(pkg.cmake_flag_args) == expected

    def test_ld_libs_cmake(self, temp_env):
        s = spack.spec.Spec('cmake-client ldlibs=-lfoo')
        s.concretize()
        pkg = spack.repo.get(s)
        pkg.flag_handler = build_system_flags
        spack.build_environment.setup_package(pkg, False)

        assert 'SPACK_LDLIBS' not in os.environ
        assert 'LDLIBS' not in os.environ

        expected = set(['-DCMAKE_C_STANDARD_LIBRARIES=-lfoo',
                        '-DCMAKE_CXX_STANDARD_LIBRARIES=-lfoo',
                        '-DCMAKE_Fortran_STANDARD_LIBRARIES=-lfoo'])
        assert set(pkg.cmake_flag_args) == expected
