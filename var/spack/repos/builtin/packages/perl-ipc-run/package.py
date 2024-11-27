# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlIpcRun(PerlPackage):
    """IPC::Run allows you to run and interact with child processes using
    files, pipes, and pseudo-ttys. Both system()-style and scripted usages are
    supported and may be mixed. Likewise, functional and OO API styles are both
    supported and may be mixed."""

    homepage = "https://metacpan.org/pod/IPC::Run"
    url = "https://cpan.metacpan.org/authors/id/T/TO/TODDR/IPC-Run-20180523.0.tar.gz"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version(
        "20231003.0", sha256="eb25bbdf5913d291797ef1bfe998f15130b455d3ed02aacde6856f0b25e4fe57"
    )
    version(
        "20220807.0", sha256="277d781dbbc98af18e979c7ef36f222513d7361742c52507c3348b265f6f5e69"
    )
    version(
        "20180523.0", sha256="3850d7edf8a4671391c6e99bb770698e1c45da55b323b31c76310913349b6c2f"
    )

    depends_on("perl-io-tty", type=("build", "run"))
    depends_on("perl-readonly", type="build")
