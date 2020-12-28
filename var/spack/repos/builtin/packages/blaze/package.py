# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Blaze(CMakePackage):
    """Blaze is an open-source, high-performance C++ math library for dense and
    sparse arithmetic. With its state-of-the-art Smart Expression Template
    implementation Blaze combines the elegance and ease of use of a
    domain-specific language with HPC-grade performance, making it one of the
    most intuitive and fastest C++ math libraries available.
    """

    homepage = "https://bitbucket.org/blaze-lib/blaze/overview"
    url      = "https://bitbucket.org/blaze-lib/blaze/downloads/blaze-3.8.tar.gz"
    git      = "https://bitbucket.org/blaze-lib/blaze.git"

    # Blaze requires at least cmake 3.8.0 for C++14 features.
    depends_on('cmake@3.8.0:', type='build')
    depends_on('blas')

    version('master', branch='master')
    version('3.8', sha256='dfaae1a3a9fea0b3cc92e78c9858dcc6c93301d59f67de5d388a3a41c8a629ae')
    version('3.7', sha256='ef3cbc5db7d62dcdde0af88d3c951051254afd750d26773406fddb6afc5ad890')
    version('3.6', sha256='2ebbadacaf3f066e27352c1e413ead127b7ced8a3b202ae45f39c8f5f12324cc')
    version('3.5', sha256='f50d4a57796b8012d3e6d416667d9abe6f4d95994eb9deb86cd4491381dec624')
    version('3.4', sha256='fd474ab479e81d31edf27d4a529706b418f874caa7b046c67489128c20dda66f')
    version('3.3', sha256='138cbb7b95775c10bf56a5ab3596a32205751299b19699984b6ed55b1bf989d0')
    version('3.2', sha256='fb7e83d3a8c1ba04d3a51234708092b75a1abf3b7c4d0db5e6cf3cbed771b869')
    version('3.1', sha256='a122d6758d9ada7ab516417f7b5ad186a4a9b390bba682f009df6585f5550716')
    version('3.0', sha256='d66abaf4633d60b6e6472f6ecd7db7b4fb5f74a4afcfdf00c92e1ea61f2e0870')
    version('2.6', sha256='a6b927db14b43fad483670dfa2acd7ecc94fd53085cdf18f262d2dc613857fb6')
    version('2.5', sha256='5faeca8a26e04f70a5b3f94e88ef1fbe96a89e3722cd89e5f9d4bc8267b33d41')
    version('2.4', sha256='34af70c8bb4da5fd0017b7c47e5efbfef9aadbabc5aae416582901a4059d1fa3')
    version('2.3', sha256='785089db7f15684c24018b931f9f564954a79389166ac1f3e256a56c667d49f2')
    version('2.2', sha256='448e70a440d71afa6325bae254ca7367b10e61431084adbf2ac679dbd5da78d2')
    version('2.1', sha256='b982c03236c6a7ae396850eba0ef8fb1642ddf6448531063bf7239d9ff3290fd')
    version('2.0', sha256='7bdf555e97455a2f42f40396b32caa9cf3e52bdd1877e0289115825113f4dcb2')
    version('1.5', sha256='5c69b605b712616dcd29fa25abecb20b977ef318207ef96176ab67b2ad891e1e')
    version('1.4', sha256='2e48d2e5a3a06abb23716829501bb0b825c58ad156faab6df0cfeef1bcdfbc82')
    version('1.3', sha256='361bfbf2d2bf8557d123da3af8abc70e4c3b13d9c94a8227aeb751e06acdb8cf')
    version('1.2', sha256='16f56d4f61dca229fa7e17a0d1e348a1f3246c65cded2df5db33babebf8f9b9d')
    version('1.1', sha256='6add20eb9c176ea9f8091c49b101f46d1a1a6bd9c31553a6eff5e53603f0527f')
    version('1.0', sha256='ee13cfd467c1a4b0fe7cc58b61b846eae862167a90dd2e60559626a30418b5a3')
