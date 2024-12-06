# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Notmuch(AutotoolsPackage):
    """Notmuch is a mail indexer.

    Essentially, is a very thin front end on top of xapian.
    """

    homepage = "https://notmuchmail.org/"
    url = "https://notmuchmail.org/releases/notmuch-0.23.7.tar.gz"

    license("GPL-3.0-or-later")

    version("0.23.7", sha256="f11bb10d71945f6c3f16d23117afc70810aa485878e66bb4bf43cc3f08038913")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("zlib-api")
    depends_on("talloc")
    depends_on("gmime@2.6:")
    depends_on("xapian-core")
