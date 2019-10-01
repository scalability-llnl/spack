# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class Libaio(MakefilePackage):
    """Linux native Asynchronous I/O interface library.

    AIO enables even a single application thread to overlap I/O operations
    with other processing, by providing an interface for submitting one or
    more I/O requests in one system call (io_submit()) without waiting for
    completion, and a separate interface (io_getevents()) to reap completed
    I/O operations associated with a given completion group.
    """

    homepage = "http://lse.sourceforge.net/io/aio.html"
    url = "https://debian.inf.tu-dresden.de/debian/pool/main/liba/libaio/libaio_0.3.110.orig.tar.gz"

    version('0.3.110', '2a35602e43778383e2f4907a4ca39ab8')

    conflicts('platform=darwin', msg="libaio is a linux specific library")

    @property
    def install_targets(self):
        return ['prefix={0}'.format(self.spec.prefix), 'install']
