# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRcppblaze(RPackage):
    """'Blaze' is an open-source, high-performance C++ math library for dense
    and sparse arithmetic.

    With its state-of-the-art Smart Expression Template implementation 'Blaze'
    combines the elegance and ease of use of a domain-specific language with
    'HPC'-grade performance, making it one of the most intuitive and fastest
    C++ math libraries available. The 'Blaze' library offers: - high
    performance through the integration of 'BLAS' libraries and manually tuned
    'HPC' math kernels - vectorization by 'SSE', 'SSE2', 'SSE3', 'SSSE3',
    'SSE4', 'AVX', 'AVX2', 'AVX-512', 'FMA', and 'SVML' - parallel execution by
    'OpenMP', C++11 threads and 'Boost' threads ('Boost' threads are disabled
    in 'RcppBlaze') - the intuitive and easy to use API of a domain specific
    language - unified arithmetic with dense and sparse vectors and matrices -
    thoroughly tested matrix and vector arithmetic - completely portable, high
    quality C++ source code. The 'RcppBlaze' package includes the header files
    from the 'Blaze' library with disabling some functionalities related to
    link to the thread and system libraries which make 'RcppBlaze' be a
    header-only library. Therefore, users do not need to install 'Blaze' and
    the dependency 'Boost'. 'Blaze' is licensed under the New (Revised) BSD
    license, while 'RcppBlaze' (the 'Rcpp' bindings/bridge to 'Blaze') is
    licensed under the GNU GPL version 2 or later, as is the rest of 'Rcpp'.
    Note that since 'Blaze' has committed to 'C++14' commit to 'C++14' which
    does not used by most R users from version 3.0, we will use the version 2.6
    of 'Blaze' which is 'C++98' compatible to support the most compilers and
    system."""

    cran = "RcppBlaze"

    license("BSD-3-Clause")

    version("1.0.1", sha256="2d152294dc231e4ab097a377ddeda6f2bbb608970c82563a893c77de08916227")
    version("0.2.2", sha256="67550ed8aea12a219047af61b41e5b9f991608a21ce9a8fbf7ac55da0f7c2742")

    depends_on("r@3.0.2:", type=("build", "run"))
    depends_on("r@4.2.0:", type=("build", "run"), when="@1.0.0:")
    depends_on("r-rcpp@0.11.0:", type=("build", "run"))
    depends_on("r-rcpp@1.0.0:", type=("build", "run"), when="@1.0.0:")
    depends_on("r-matrix@1.1-0:", type=("build", "run"))
    depends_on("r-matrix@1.5-0:", type=("build", "run"), when="@1.0.0:")

    depends_on("r-bh@1.54.0-2:", type=("build", "run"), when="@:0.2.2")
