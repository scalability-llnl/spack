# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
class ConditionalValuesInVariant(Package):
    """Mimic the real netlib-lapack, that may be built on top of an
    optimized blas.
    """
    homepage = "https://dev.null"

    version('1.73.0')
    version('1.72.0')
    version('1.62.0')

    variant(
        'cxxstd', default='98',
        values=(
            '98', '11', '14',
            # C++17 is not supported by Boost < 1.63.0.
            Value('17', when='@1.63.0:'),
            # C++20/2a is not support by Boost < 1.73.0
            Value('2a', when='@1.73.0:')
        ),
        multi=False,
        description='Use the specified C++ standard when building.'
    )
