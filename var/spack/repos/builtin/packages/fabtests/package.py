# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Fabtests(AutotoolsPackage):
    """Fabtests provides a set of runtime analysis tools and examples that use
    libfabric."""

    homepage = "https://libfabric.org"
    url = "https://github.com/ofiwg/libfabric/releases/download/v1.9.1/fabtests-1.9.1.tar.bz2"
    maintainers("kgerheiser")

    license("GPL-2.0-only")

    version("1.21.0", sha256="d022a186d37bd6ccb52303e0588c28e29f0f56c25a384c37acb16c881ba99e64")
    version("1.20.2", sha256="624beb02ffc8e325834545810566330f2a1204d5c6ad015ba095303121cb8ae6")
    version("1.20.1", sha256="687884b6fd3046f46e2f878e19e76e4506b50950bd2f59a731618b89d02a5436")
    version("1.20.0", sha256="61d483452163b39d81dcb9f578e5d9007817e0496235bc2aac1e82b7737fd65e")
    version("1.19.1", sha256="57b11f2e0e3cd77b104d63f0ecb453161fa8a17bc4f7ca2d7a17a7a34f7fb85c")
    version("1.19.0", sha256="82d714020df9258cfdd659c51f2be8f4507cbe157c7f03c992c70fc528d8d837")
    version("1.18.2", sha256="3d85486ff80151defdb66414a851a9a9a2d4adc6cf696e2b8e4bb3ce340512c2")
    version("1.18.1", sha256="fe9864acc0e17a5b0157b1cc996bb3c578cfa32c87bd43bc17b5e31e24ef63b5")
    version("1.18.0", sha256="9201ba020c3cf2f07dbf16d9837b565031f2eab664efd02f2e4345443983ae3e")
    version("1.17.1", sha256="efc89c6c2412168b7b8fdd495c2f46d9074205363959e80e4c8d452ba97d4c0d")
    version("1.17.0", sha256="5d3cf28de32549822cbb155329fe7ce0f88423157e1210a76b23c498c848ce2a")
    version("1.16.1", sha256="0e5def832ac9438ba7c50b8198f0089b568935fcc13d1ccb50a5f8a1dcf4ec30")
    version("1.16.0", sha256="c428ec353f64b073fb17ac0061aab76b9cc8c41614adb772d00575f3e486884d")
    version("1.15.2", sha256="9afdc992bedf3f47c068824ba3408156c890b5cb2587964ec2ad9f658102db63")
    version("1.9.1", sha256="6f8ced2c6b3514759a0e177c8b2a19125e4ef0714d4cc0fe0386b33bd6cd5585")
    version("1.9.0", sha256="60cc21db7092334904cbdafd142b2403572976018a22218e7c453195caef366e")
    version("1.8.1", sha256="e9005d8fe73ca3849c872649c29811846bd72a62f897ecab73a08c7a9514f37b")
    # old releases, published in a separate repository
    version("1.6.2", sha256="37405c6202f5b1aa81f8ea211237a2d87937f06254fa3ed44a9b69ac73b234e8")
    version("1.6.1", sha256="d357466b868fdaf1560d89ffac4c4e93a679486f1b4221315644d8d3e21174bf")
    version("1.6.0", sha256="dc3eeccccb005205017f5af60681ede15782ce202a0103450a6d56a7ff515a67")
    version("1.5.3", sha256="3835b3bf86cd00d23df0ddba8bf317e4a195e8d5c3c2baa918b373d548f77f29")
    version("1.5.0", sha256="1dddd446c3f1df346899f9a8636f1b4265de5b863103ae24876e9f0c1e40a69d")
    version("1.4.2", sha256="3b78d0ca1b223ff21b7f5b3627e67e358e3c18b700f86b017e2233fee7e88c2e")

    depends_on("c", type="build")  # generated

    versions = [
        "1.21.0",
        "1.20.2",
        "1.20.1",
        "1.20.0",
        "1.19.1",
        "1.19.0",
        "1.18.2",
        "1.18.1",
        "1.18.0",
        "1.17.1",
        "1.17.0",
        "1.16.1",
        "1.16.0",
        "1.15.2",
        "1.9.1",
        "1.9.0",
        "1.8.1",
        "1.6.2",
        "1.6.1",
        "1.6.0",
        "1.5.3",
        "1.5.0",
        "1.4.2",
    ]

    for v in versions:
        depends_on("libfabric@{0}".format(v), when="@{0}".format(v))

    def url_for_version(self, version):
        if version >= Version("1.8.1"):
            url = "https://github.com/ofiwg/libfabric/releases/download/v{0}/fabtests-{0}.tar.bz2"
        else:
            url = "https://github.com/ofiwg/fabtests/releases/download/v{0}/fabtests-{0}.tar.gz"
        return url.format(version.dotted)
