# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkg.builtin.libflame import LibflameBase


class Amdlibflame(LibflameBase):
    """libFLAME (AMD Optimized version) is a portable library for
    dense matrix computations, providing much of the functionality
    present in Linear Algebra Package (LAPACK). It includes a
    compatibility layer, FLAPACK, which includes complete LAPACK
    implementation.

    The library provides scientific and numerical computing communities
    with a modern, high-performance dense linear algebra library that is
    extensible, easy to use, and available under an open source
    license. libFLAME is a C-only implementation and does not
    depend on any external FORTRAN libraries including LAPACK.
    There is an optional backward compatibility layer, lapack2flame
    that maps LAPACK routine invocations to their corresponding
    native C implementations in libFLAME. This allows legacy
    applications to start taking advantage of libFLAME with
    virtually no changes to their source code.

    In combination with BLIS library which includes optimizations
    for the AMD EPYC processor family, libFLAME enables running
    high performing LAPACK functionalities on AMD platform."""

    _name = 'amdlibflame'
    homepage = "http://developer.amd.com/amd-cpu-libraries/blas-library/#libflame"
    url = "https://github.com/amd/libflame/archive/2.2.tar.gz"
    git = "https://github.com/amd/libflame.git"

    version('2.2', sha256='12b9c1f92d2c2fa637305aaa15cf706652406f210eaa5cbc17aaea9fcfa576dc')
    version('2.1', sha256='dc2dcaabd4a90ecb328bee3863db0908e412bf7ce5fb8f5e93377fdbca9abb65')
    version('2.0', sha256='c80517b455df6763341f67654a6bda909f256a4927ffe9b4f0a2daed487d3739')
    provides('flame@5.2', when='@2:')


    def configure_args(self):
        args = super(Amdlibflame, self).configure_args()
        args.append("--enable-external-lapack-interfaces")
        return args

    def install(self, spec, prefix):
        make()

        # make install in parallel fails with message 'File already exists'
        make("install", parallel=False)
