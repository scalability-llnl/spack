# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Sysstat(AutotoolsPackage):
    """The sysstat package contains various utilities, common to many
    commercial Unixes, to monitor system performance and usage activity
    Sysstat also contains tools you can schedule via cron or systemd to
    collect and historize performance and activity data."""

    homepage = "https://github.com/sysstat"
    url      = "https://github.com/sysstat/sysstat/archive/v12.1.6.tar.gz"

    version('12.2.0', sha256='614ab9fe8e7937a3edb7b2b6760792a3764ea3a7310ac540292dd0e3dfac86a6')
    version('12.1.7', sha256='293b31ca414915896c639a459f4d03a742b3a472953975394bef907b245b3a9f')
    version('12.1.6', sha256='50f4cbf023f8b933ed6f1fee0e6d33e508d9dc20355a47f6927e0c6046c6acf6')
    version('12.1.5', sha256='d0ea36f278fe10c7978be2a383cb8055c1277d60687ac9030ba694a08a80f6ff')
