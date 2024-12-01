# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRadicalPilot(PythonPackage):
    """RADICAL-Pilot is a Pilot system specialized in executing applications
    composed of many computational tasks on high performance computing (HPC)
    platforms."""

    homepage = "https://radical-cybertools.github.io"
    git = "https://github.com/radical-cybertools/radical.pilot.git"
    pypi = "radical.pilot/radical.pilot-1.47.0.tar.gz"

    maintainers("andre-merzky")

    license("MIT")

    version("develop", branch="devel")
    version("1.47.0", sha256="58f41a0c42fe61381f15263a63424294732606ab7cee717540c0b730308f7908")
    version("1.39.0", sha256="7ba0bfa3258b861db71e73d52f0915bfb8b3ac1099badacf69628307cab3b913")

    version(
        "1.20.0",
        sha256="a0747e573a01a856dc330797dbee158f7e1cf8652001dc26f06a1d6c5e553bc6",
        deprecated=True,
    )
    version(
        "1.18.1",
        sha256="fd6a0ffaa727b6b9bab35d8f2dc300bf4d9c4ff3541136d83560aa7b853d6100",
        deprecated=True,
    )
    version(
        "1.17.0",
        sha256="0bfbb321a623a684e6694241aa3b7804208846515d23afa3b930553274f4a69f",
        deprecated=True,
    )
    version(
        "1.16.0",
        sha256="057941a206ee96b62b97a63a507c1136b7fe821ae9f9e5eebe7949a3f53941f9",
        deprecated=True,
    )
    version(
        "1.15.1",
        sha256="35c3b179a0bc85f52d2165e98e19acf2bf79037dd14f4d9ff3fc55ae0122d17e",
        deprecated=True,
    )
    version(
        "1.14.0",
        sha256="462471065de25f6d6e8baee705790828444c2eebb2073f5faf67a8da800d15a9",
        deprecated=True,
    )
    version(
        "1.13.0",
        sha256="5bd9eef1884ccca09c242ab6d1361588a442d9cd980613c66604ba140786bde5",
        deprecated=True,
    )
    version(
        "1.12.0",
        sha256="a266355d30d838f20b6cac190ce589ca919acd41883ad06aec62386239475133",
        deprecated=True,
    )
    version(
        "1.11.2",
        sha256="9d239f747589b8ae5d6faaea90ea5304b6f230a1edfd8d4efb440bc3799c8a9d",
        deprecated=True,
    )
    version(
        "1.10.2",
        sha256="56e9d8b1ce7ed05eff471d7df660e4940f485027e5f353aa36fd17425846a499",
        deprecated=True,
    )
    version(
        "1.10.1",
        sha256="003f4c519b991bded31693026b69dd51547a5a69a5f94355dc8beff766524b3c",
        deprecated=True,
    )
    version(
        "1.9.2",
        sha256="7c872ac9103a2aed0c5cd46057048a182f672191e194e0fd42794b0012e6e947",
        deprecated=True,
    )
    version(
        "1.8.0",
        sha256="a4c3bca163db61206e15a2d820d9a64e888da5c72672448ae975c26768130b9d",
        deprecated=True,
    )
    version(
        "1.6.8",
        sha256="fa8fd3f348a68b54ee8338d5c5cf1a3d99c10c0b6da804424a839239ee0d313d",
        deprecated=True,
    )
    version(
        "1.6.7",
        sha256="6ca0a3bd3cda65034fa756f37fa05681d5a43441c1605408a58364f89c627970",
        deprecated=True,
    )

    depends_on("py-radical-utils@1.44:", type=("build", "run"), when="@1.47:")
    depends_on("py-radical-saga@1.40:", type=("build", "run"), when="@1.47:")
    depends_on("py-radical-gtod", type=("build", "run"), when="@1.14:")

    depends_on("py-radical-utils@1.39", type=("build", "run"), when="@1.39")
    depends_on("py-radical-saga@1.39", type=("build", "run"), when="@1.39")
    depends_on("py-radical-gtod@1.39", type=("build", "run"), when="@1.39")

    depends_on("py-radical-utils@1.12:1.20", type=("build", "run"), when="@1.12:1.20")
    depends_on("py-radical-saga@1.12:1.20", type=("build", "run"), when="@1.12:1.20")

    depends_on("py-radical-utils@1.8.4:1.11", type=("build", "run"), when="@1.11")
    depends_on("py-radical-saga@1.8:1.11", type=("build", "run"), when="@1.11")

    depends_on("py-radical-utils@:1.8.3", type=("build", "run"), when="@:1.10")
    depends_on("py-radical-saga@:1.7", type=("build", "run"), when="@:1.10")

    depends_on("py-pymongo@:3", type=("build", "run"), when="@:1.39")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-dill", type=("build", "run"), when="@1.14:")
    depends_on("py-setproctitle", type=("build", "run"))
    depends_on("py-setuptools", type="build")
