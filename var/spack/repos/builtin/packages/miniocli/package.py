# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Miniocli(MakefilePackage):
    """MinIO Client (mc) provides a modern alternative to UNIX commands
    like ls, cat, cp, mirror, diff etc. It supports filesystems and
    Amazon S3 compatible cloud storage service (AWS Signature v2 and v4)."""

    homepage = "https://docs.min.io/docs/minio-client-complete-guide.html"
    url = "https://github.com/minio/mc/archive/refs/tags/RELEASE.2022-02-02T02-03-24Z.tar.gz"

    license("AGPL-3.0-only")

    version(
        "2023-06-28",
        sha256="033a80439474595665bdbc3ec72b059dc9e69e99db85fe6820877ad8973a080b",
        url="https://github.com/minio/mc/archive/refs/tags/RELEASE.2023-06-28T21-54-17Z.tar.gz",
    )
    version(
        "2022-05-04",
        sha256="2b935c3744228978c93c14186b65a6078e4ffc267f32cdb8c994eff2dda95a6e",
        url="https://github.com/minio/mc/archive/RELEASE.2022-05-04T06-07-55Z.tar.gz",
    )
    version(
        "2022-03-31",
        sha256="3b983ea1cc50768b0826989dba931044ac3f8e841cc09aefed217301c92fa8a3",
        url="https://github.com/minio/mc/archive/RELEASE.2022-03-31T04-55-30Z.tar.gz",
    )
    # versions of 2022-03-* or later require  github.com/shirou/gopsutil/v3 and
    # this is generating an error
    version(
        "2022-02-02",
        sha256="2d4a64c17935d40d0e325761cc214b2efceb19ce006101c192da9b31f8920a97",
        url="https://github.com/minio/mc/archive/RELEASE.2022-02-02T02-03-24Z.tar.gz",
    )
    version(
        "2022-01-05",
        sha256="d5dbd32b7a7f79baace09dd6518121798d2fcbb84b81046b61ff90f980c8f963",
        url="https://github.com/minio/mc/archive/RELEASE.2022-01-05T23-52-51Z.tar.gz",
    )

    depends_on("go", type="build")

    def install(self, spec, prefix):
        go("build")
        mkdirp(prefix.bin)
        install("mc", prefix.bin)
