# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Libaio(MakefilePackage):
    """Linux native Asynchronous I/O interface library.

    AIO enables even a single application thread to overlap I/O operations
    with other processing, by providing an interface for submitting one or
    more I/O requests in one system call (io_submit()) without waiting for
    completion, and a separate interface (io_getevents()) to reap completed
    I/O operations associated with a given completion group.
    """

    homepage = "https://lse.sourceforge.net/io/aio.html"
    url = (
        "https://debian.inf.tu-dresden.de/debian/pool/main/liba/libaio/libaio_0.3.110.orig.tar.gz"
    )

    license("LGPL-2.1-or-later")

    version("0.3.113", sha256="2c44d1c5fd0d43752287c9ae1eb9c023f04ef848ea8d4aafa46e9aedb678200b")
    version("0.3.110", sha256="e019028e631725729376250e32b473012f7cb68e1f7275bfc1bbcdd0f8745f7e")

    depends_on("c", type="build")  # generated

    conflicts("platform=darwin", msg="libaio is a linux specific library")

    @property
    def install_targets(self):
        return ["prefix={0}".format(self.spec.prefix), "install"]
