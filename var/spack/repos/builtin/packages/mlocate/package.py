# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Mlocate(AutotoolsPackage):
    """mlocate is a locate/updatedb implementation.  The 'm' stands for "merging":
    updatedb reuses the existing database to avoid rereading most of the file
    system, which makes updatedb faster and does not trash the system caches as
    much."""

    homepage = "https://pagure.io/mlocate"
    url = "https://releases.pagure.org/mlocate/mlocate-0.26.tar.xz"

    license("GPL-2.0-only")

    version("0.26", sha256="3063df79fe198fb9618e180c54baf3105b33d88fe602ff2d8570aaf944f1263e")
    version("0.25", sha256="ab95c111f9dba35b5690896180dd0a7639dbf07d70b862fcb0731264d9273951")
    version("0.24", sha256="5787bee846735e21ff57df9e345d5db73d684d2cea9efc0f387462ccfbc6796f")

    depends_on("c", type="build")  # generated
