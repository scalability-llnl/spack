# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlThreadQueue(PerlPackage):
    """Thread::Queue - Thread-safe queues.

    This module provides thread-safe FIFO queues that can be accessed safely by
    any number of threads."""

    homepage = "https://metacpan.org/pod/Thread::Queue"
    url = "https://cpan.metacpan.org/authors/id/J/JD/JDHEDDEN/Thread-Queue-3.13.tar.gz"

    version("3.13", sha256="6ba3dacddd2fbb66822b4aa1d11a0a5273cd04c825cb3ff31c20d7037cbfdce8")
