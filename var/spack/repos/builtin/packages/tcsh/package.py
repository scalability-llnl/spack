# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


def fedora_patch(commit, file, **kwargs):
    prefix = "https://src.fedoraproject.org/rpms/tcsh/raw/{0}/f/".format(commit)
    patch("{0}{1}".format(prefix, file), **kwargs)


class Tcsh(AutotoolsPackage):
    """Tcsh is an enhanced but completely compatible version of csh, the C
    shell. Tcsh is a command language interpreter which can be used both as
    an interactive login shell and as a shell script command processor. Tcsh
    includes a command line editor, programmable word completion, spelling
    correction, a history mechanism, job control and a C language like
    syntax."""

    homepage = "https://www.tcsh.org/"
    url = "http://ftp.funet.fi/pub/mirrors/ftp.astron.com/pub/tcsh/tcsh-6.20.00.tar.gz"
    list_url = "https://ftp.funet.fi/pub/mirrors/ftp.astron.com/pub/tcsh/old/"

    license("BSD-3-Clause")

    version("6.24.00", sha256="60be2c504bd8f1fa6e424b1956495d7e7ced52a2ac94db5fd27f4b6bfc8f74f0")
    version("6.22.02", sha256="ed287158ca1b00ba477e8ea57bac53609838ebcfd05fcb05ca95021b7ebe885b")
    version("6.21.00", sha256="c438325448371f59b12a4c93bfd3f6982e6f79f8c5aef4bc83aac8f62766e972")
    version("6.20.00", sha256="b89de7064ab54dac454a266cfe5d8bf66940cb5ed048d0c30674ea62e7ecef9d")

    depends_on("c", type="build")  # generated

    # Upstream patches
    fedora_patch(
        "96b95844cc685b11ed0cc215137e394da4505d41",
        "tcsh-6.22.02-avoid-gcc-to-fail.patch",
        when="@:6.22.02",
        sha256="392615011adb7afeb0010152409a37b150f03dbde5b534503e9cd7363b742a19",
    )
    fedora_patch(
        "8a6066c901fb4fc75013dd488ba958387f00c74d",
        "tcsh-6.20.00-000-add-all-flags-for-gethost-build.patch",
        when="@6.20.00",
        sha256="f8266916189ebbdfbad5c2c28ac00ed25f07be70f054d9830eb84ba84b3d03ef",
    )
    fedora_patch(
        "8a6066c901fb4fc75013dd488ba958387f00c74d",
        "tcsh-6.20.00-001-delay-arginp-interpreting.patch",
        when="@6.20.00",
        sha256="57c7a9b0d94dd41e4276b57b0a4a89d91303d36180c1068b9e3ab8f6149b18dd",
    )
    fedora_patch(
        "8a6066c901fb4fc75013dd488ba958387f00c74d",
        "tcsh-6.20.00-002-type-of-read-in-prompt-confirm.patch",
        when="@6.20.00",
        sha256="837a6a82f815c0905cf7ea4c4ef0112f36396fc8b2138028204000178a1befa5",
    )
    fedora_patch(
        "8a6066c901fb4fc75013dd488ba958387f00c74d",
        "tcsh-6.20.00-003-fix-out-of-bounds-read.patch",
        when="@6.20.00",
        sha256="f973bd33a7fd8af0002a9b8992216ffc04fdf2927917113e42e58f28b702dc14",
    )
    fedora_patch(
        "8a6066c901fb4fc75013dd488ba958387f00c74d",
        "tcsh-6.20.00-004-do-not-use-old-pointer-tricks.patch",
        when="@6.20.00",
        sha256="333e111ed39f7452f904590b47b996812590b8818f1c51ad68407dc05a1b18b0",
    )
    fedora_patch(
        "8a6066c901fb4fc75013dd488ba958387f00c74d",
        "tcsh-6.20.00-005-reset-fixes-numbering.patch",
        when="@6.20.00",
        sha256="d1b54b5c5432faed9791ffde813560e226896a68fc5933d066172bcf3b2eb8bd",
    )
    fedora_patch(
        "8a6066c901fb4fc75013dd488ba958387f00c74d",
        "tcsh-6.20.00-006-cleanup-in-readme-files.patch",
        when="@6.20.00",
        sha256="b4e7428ac6c2918beacc1b73f33e784ac520ef981d87e98285610b1bfa299d7b",
    )
    fedora_patch(
        "8a6066c901fb4fc75013dd488ba958387f00c74d",
        "tcsh-6.20.00-007-look-for-tgetent-in-libtinfo.patch",
        when="@6.20.00",
        sha256="e6c88ffc291c9d4bda4d6bedf3c9be89cb96ce7dc245163e251345221fa77216",
    )
    fedora_patch(
        "8a6066c901fb4fc75013dd488ba958387f00c74d",
        "tcsh-6.20.00-008-guard-ascii-only-reversion.patch",
        when="@6.20.00",
        sha256="7ee195e4ce4c9eac81920843b4d4d27254bec7b43e0b744f457858a9f156e621",
    )
    fedora_patch(
        "8a6066c901fb4fc75013dd488ba958387f00c74d",
        "tcsh-6.20.00-009-fix-regexp-for-backlash-quoting-tests.patch",
        when="@6.20.00",
        sha256="d2358c930d5ab89e5965204dded499591b42a22d0a865e2149b8c0f1446fac34",
    )

    # Downstream patches
    fedora_patch(
        "8a6066c901fb4fc75013dd488ba958387f00c74d",
        "tcsh-6.20.00-manpage-memoryuse.patch",
        sha256="3a4e60fe56a450632140c48acbf14d22850c1d72835bf441e3f8514d6c617a9f",
    )

    depends_on("ncurses+termlib")

    @run_after("install")
    def link_csh(self):
        symlink("tcsh", "{0}/csh".format(self.prefix.bin))
        symlink("tcsh.1", "{0}/csh.1".format(self.prefix.share.man.man1))
