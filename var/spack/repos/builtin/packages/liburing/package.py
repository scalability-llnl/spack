# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Liburing(AutotoolsPackage):
    """Linux-native io_uring I/O access library.

    liburing provides helpers to setup and teardown io_uring instances,
    and a simplified interface for applications that don't need (or want)
    to deal with the full kernel side implementation. It enables high-performance
    asynchronous I/O operations on Linux systems supporting the io_uring
    interface.
    """

    homepage = "https://github.com/axboe/liburing"
    url = "https://github.com/axboe/liburing/archive/refs/tags/liburing-2.3.tar.gz"
    git = "https://github.com/axboe/liburing.git"

    maintainers("alecbcs")

    license("LGPL-2.1-or-later OR MIT")

    sanity_check_is_file = ["include/liburing.h", "lib/liburing.so"]
    sanity_check_is_dir = ["include", "lib"]

    version("master", branch="master")
    version("2.9", sha256="897b1153b55543e8b92a5a3eb9b906537a5fedcf8afaf241f8b8787940c79f8d")
    version("2.4", sha256="2398ec82d967a6f903f3ae1fd4541c754472d3a85a584dc78c5da2fabc90706b")
    version("2.3", sha256="60b367dbdc6f2b0418a6e0cd203ee0049d9d629a36706fcf91dfb9428bae23c8")

    depends_on("c", type="build")
    depends_on("cxx", type="build")  # only for tests

    requires("platform=linux", msg="liburing is only supported on Linux.")

    @property
    def build_targets(self):
        if self.spec.satisfies("@2.7:"):
            # avoid examples and test
            return ["library"]
        else:
            return ["all"]
