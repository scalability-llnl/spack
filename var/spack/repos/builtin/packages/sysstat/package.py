# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
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
    url = "https://github.com/sysstat/sysstat/archive/v12.1.6.tar.gz"

    license("GPL-2.0-or-later")

    version("12.7.6", sha256="dc77a08871f8e8813448ea31048833d4acbab7276dd9a456cd2526c008bd5301")
    with default_args(deprecated=True):
        # https://nvd.nist.gov/vuln/detail/CVE-2023-33204
        # https://nvd.nist.gov/vuln/detail/CVE-2022-39377
        version(
            "12.4.5", sha256="4e35abdd9eaf766ecdab55786f459093f3e1c350db23e57a15561afda417ff0d"
        )
        version(
            "12.2.0", sha256="614ab9fe8e7937a3edb7b2b6760792a3764ea3a7310ac540292dd0e3dfac86a6"
        )

    depends_on("c", type="build")  # generated

    depends_on("pkgconfig", type="build")
    depends_on("gettext")
    depends_on("lm-sensors")

    def setup_build_environment(self, env):
        env.append_flags("rcdir", self.spec.prefix.etc)
        env.append_flags("sa_dir", self.spec.prefix.log.sa)
        env.append_flags("conf_dir", self.spec.prefix.etc.sysconfig)

    def configure_args(self):
        args = ["--disable-pcp", "--disable-file-attr"]

        return args
