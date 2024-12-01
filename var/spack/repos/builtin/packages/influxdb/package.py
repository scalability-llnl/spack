# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import platform

from spack.package import *

_versions = {
    "1.8.1": {
        "Linux_amd64": (
            "64e60e438ac8a8fdacc6623f238c40bffae31c795642146d70eb316533d3d70f",
            "https://dl.influxdata.com/influxdb/releases/influxdb-1.8.1-static_linux_amd64.tar.gz",
        ),
        "Linux_aarch64": (
            "fd5d7c962827ab1ccae27f6504595fdcd30c20d505b8e07d8573e274824e1366",
            "https://dl.influxdata.com/influxdb/releases/influxdb-1.8.1_linux_arm64.tar.gz",
        ),
    },
    "1.8.0": {
        "Linux_amd64": (
            "aedc5083ae2e61ef374dbde5044ec2a5b27300e73eb92ccd135e6ff9844617e2",
            "https://dl.influxdata.com/influxdb/releases/influxdb-1.8.0-static_linux_amd64.tar.gz",
        ),
        "Linux_aarch64": (
            "e76c36c10e46c2fd17820156b290dd776a465da0298496af5d490e555504b079",
            "https://dl.influxdata.com/influxdb/releases/influxdb-1.8.0_linux_arm64.tar.gz",
        ),
    },
}


class Influxdb(Package):
    """InfluxDB is an open source time series platform."""

    homepage = "https://influxdata.com/"
    url = "https://dl.influxdata.com/influxdb/releases/influxdb-1.8.1-static_linux_amd64.tar.gz"

    for ver, packages in _versions.items():
        key = "{0}_{1}".format(platform.system(), platform.machine())
        pkg = packages.get(key)
        if pkg:
            version(ver, sha256=pkg[0], url=pkg[1])

    def setup_run_environment(self, env):
        env.prepend_path("PATH", self.prefix.usr.bin)

    def install(self, spec, prefix):
        install_tree("usr", prefix)
        install_tree("etc", prefix.etc)
        install_tree("var", prefix.var)
