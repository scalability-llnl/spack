# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class VarnishCache(AutotoolsPackage):
    """This is Varnish Cache, the high-performance HTTP accelerator."""

    homepage = "https://www.varnish-cache.org/"
    url = "https://github.com/varnishcache/varnish-cache/archive/refs/tags/varnish-6.4.0.tar.gz"

    license("BSD-2-Clause")

    version("7.6.1", sha256="6cfa30d761fa5edf33322048564cda3ee99de93ee57732c10f720d98d12f1899")
    with default_args(deprecated=True):
        # https://nvd.nist.gov/vuln/detail/CVE-2022-23959
        version("6.4.0", sha256="d9702c2c689c5d4ecd911886f769ddf22f46ac0722e275bee4033928cab09243")
        version("6.3.2", sha256="e50f3dd4e26d5669c5b73657cdb0d5ddac7dcc3cfa1761a983afa24b659f3785")
        version("6.3.1", sha256="8cc57360c1db36e8c77fc51304a935803a06247f6d6120fa47e8345efadf17a9")
        version("6.3.0", sha256="c7170d4bc57f1d2454da046fc5e43e2d19a804448d2dd839fa5c33f76bd677bb")
        version("6.2.3", sha256="64cd273aa155c78c21e74def53622be5920c8a7d952fee74f0663e57a01c9a9d")

    depends_on("c", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("pcre2", when="@7:")
    depends_on("pcre", when="@:6")
    depends_on("readline")
    depends_on("python", type=("build", "run"))
    depends_on("py-sphinx", type=("build", "run"))
    depends_on("py-docutils", type=("build", "run"))
