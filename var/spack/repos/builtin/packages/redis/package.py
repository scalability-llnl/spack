# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Redis(MakefilePackage):
    """Redis is an open source (BSD licensed), in-memory data structure store,
    used as a database, cache and message broker.
    It supports data structures such as strings, hashes, lists, sets, sorted
    sets with range queries, bitmaps, hyperloglogs, geospatial indexes with
    radius queries and streams. Redis has built-in replication, Lua scripting,
    LRU eviction, transactions and different levels of on-disk persistence,
    and provides high availability via Redis Sentinel and automatic
    partitioning with Redis Cluster
    """

    homepage = "https://redis.io"
    urls = [
        "https://download.redis.io/releases/redis-7.4.0.tar.gz",
        "https://github.com/redis/redis/archive/refs/tags/7.4.0.tar.gz",
    ]
    git = "https://github.com/redis/redis.git"

    maintainers("lpottier")

    license("BSD-3-Clause")

    version("7.4.0", sha256="57b47c2c6682636d697dbf5d66d8d495b4e653afc9cd32b7adf9da3e433b8aaf")
    with default_args(deprecated=True):
        # https://nvd.nist.gov/vuln/detail/CVE-2023-36824
        version("7.0.5", sha256="67054cc37b58c125df93bd78000261ec0ef4436a26b40f38262c780e56315cc3")
        version("7.0.4", sha256="f0e65fda74c44a3dd4fa9d512d4d4d833dd0939c934e946a5c622a630d057f2f")
        version("7.0.3", sha256="2cde7d17214ffe305953da9fff12333e8a72caa57fd4923e4872f6362a208e73")
        version("7.0.2", sha256="5e57eafe7d4ac5ecb6a7d64d6b61db775616dbf903293b3fcc660716dbda5eeb")
        version("7.0.1", sha256="ca1820d527e4759884620be2917079e61e996fa81da5fbe5c07c4a7b507264dc")
        version("7.0.0", sha256="284d8bd1fd85d6a55a05ee4e7c31c31977ad56cbf344ed83790beeb148baa720")
        # https://nvd.nist.gov/vuln/detail/CVE-2022-24834
        version("6.2.7", sha256="b7a79cc3b46d3c6eb52fa37dde34a4a60824079ebdfb3abfbbfa035947c55319")
        version("6.2.6", sha256="5b2b8b7a50111ef395bf1c1d5be11e6e167ac018125055daa8b5c2317ae131ab")
        version("6.2.5", sha256="4b9a75709a1b74b3785e20a6c158cab94cf52298aa381eea947a678a60d551ae")
        version("6.2.4", sha256="ba32c406a10fc2c09426e2be2787d74ff204eb3a2e496d87cff76a476b6ae16e")
        version("6.2.3", sha256="98ed7d532b5e9671f5df0825bb71f0f37483a16546364049384c63db8764512b")
        version("6.2.2", sha256="7a260bb74860f1b88c3d5942bf8ba60ca59f121c6dce42d3017bed6add0b9535")
        version("6.2.1", sha256="cd222505012cce20b25682fca931ec93bd21ae92cb4abfe742cf7b76aa907520")
        version("6.2.0", sha256="67d624c25d962bd68aff8812a135df85bad07556b8825f3bcd5b522a9932dbca")
        version(
            "6.0.15", sha256="4bc295264a95bc94423c162a9eee66135a24a51eefe5f53f18fc9bde5c3a9f74"
        )
        version("6.0.5", sha256="42cf86a114d2a451b898fcda96acd4d01062a7dbaaad2801d9164a36f898f596")
        version("5.0.3", sha256="e290b4ddf817b26254a74d5d564095b11f9cd20d8f165459efa53eb63cd93e02")
        version("5.0.2", sha256="937dde6164001c083e87316aa20dad2f8542af089dfcb1cbb64f9c8300cd00ed")
        version("5.0.1", sha256="82a67c0eec97f9ad379384c30ec391b269e17a3e4596393c808f02db7595abcb")
        version("5.0.0", sha256="70c98b2d0640b2b73c9d8adb4df63bcb62bad34b788fe46d1634b6cf87dc99a4")
        version(
            "4.0.13", sha256="17d955227966dcd68590be6139e5fe7f2d19fc4fb7334248a904ea9cdd30c1d4"
        )
        version(
            "4.0.12", sha256="6447259d2eed426a949c9c13f8fdb2d91fb66d9dc915dd50db13b87f46d93162"
        )
        version(
            "4.0.11", sha256="fc53e73ae7586bcdacb4b63875d1ff04f68c5474c1ddeda78f00e5ae2eed1bbb"
        )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("tls", default=False, when="@6:", description="Builds with TLS support")
    depends_on("openssl@1.1:", type=("build", "link"), when="+tls")

    variant(
        "systemd",
        default=False,
        description="Builds with systemd support (systemd development libraries required)",
    )

    @property
    def build_targets(self):
        use_tls = "yes" if "+tls" in self.spec else "no"
        use_systemd = "yes" if "+systemd" in self.spec else "no"
        return ["BUILD_TLS={0}".format(use_tls), "USE_SYSTEMD={0}".format(use_systemd)]

    @property
    def install_targets(self):
        return ["PREFIX={0}".format(self.spec.prefix), "install"]

    @run_after("install")
    def install_conf(self):
        mkdirp(self.prefix.conf)
        install("redis.conf", self.prefix.conf)
