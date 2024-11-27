# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Byobu(AutotoolsPackage):
    """Byobu: Text-based window manager and terminal multiplexer."""

    homepage = "https://www.byobu.co/"
    url = "https://launchpad.net/byobu/trunk/5.123/+download/byobu_5.123.orig.tar.gz"

    maintainers("matthiasdiener")

    license("GPL-3.0-or-later")

    version("5.131", sha256="77ac751ae79d8e3f0377ac64b64bc9738fa68d68466b8d2ff652b63b1d985e52")
    version("5.127", sha256="4bafc7cb69ff5b0ab6998816d58cd1ef7175e5de75abc1dd7ffd6d5288a4f63b")
    version("5.125", sha256="5022c82705a5d57f1d4e8dcb1819fd04628af2d4b4618b7d44fa27ebfcdda9db")
    version("5.123", sha256="2e5a5425368d2f74c0b8649ce88fc653420c248f6c7945b4b718f382adc5a67d")

    depends_on("tmux", type=("build", "run"))
