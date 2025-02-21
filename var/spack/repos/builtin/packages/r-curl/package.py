# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RCurl(RPackage):
    """A Modern and Flexible Web Client for R.

    The curl() and curl_download() functions provide highly configurable
    drop-in replacements for base url() and download.file() with better
    performance, support for encryption (https, ftps), gzip compression,
    authentication, and other libcurl goodies. The core of the package
    implements a framework for performing fully customized requests where data
    can be processed either in memory, on disk, or streaming via the callback
    or connection interfaces. Some knowledge of libcurl is recommended; for a
    more-user-friendly web client see the 'httr' package which builds on this
    package with http specific tools and logic."""

    cran = "curl"

    license("MIT")

    version("6.2.0", sha256="0399bb6bcad5f31ad2a2a7165ff8c976111707125ca0a9c4b8ccf40bb5eb1635")
    version("5.2.1", sha256="4a7a4d8c08aa1bca2fcd9c58ade7b4b0ea2ed9076d0521071be29baac8adfa90")
    version("5.0.0", sha256="d7f3cac9b513914ffa8f6f64e6fa5dd96c8273378ace6b0c16b71bc6ba59c9b2")
    version("4.3.3", sha256="3567b6acad40dad68acfe07511c853824839d451a50219a96dd6d125ed617c9e")
    version("4.3.2", sha256="90b1facb4be8b6315bb3d272ba2dd90b88973f6ea1ab7f439550230f8500a568")
    version("4.3", sha256="7406d485bb50a6190e3ed201e3489063fd249b8b3b1b4f049167ac405a352edb")

    # requires deprecated curl
    version(
        "4.0",
        sha256="09a99c9c86666449188fbb211cb1e9fbdb5108ab56f0d09322cd0ae50e926171",
        deprecated=True,
    )
    version(
        "3.3",
        sha256="0cb0b9a9280edc42ebed94708541ec86b4f48779e722171e45227eab8a88a5bd",
        deprecated=True,
    )
    version(
        "3.0",
        sha256="7bf8e3ae7cc77802ae300277e85d925d4c0611a9b7dad5c5601e0d2cbe14a506",
        deprecated=True,
    )
    version(
        "2.3",
        sha256="f901dad6bb70a6875a85da75bcbb42afffdcdf4ef221909733826bcb012d7c3d",
        deprecated=True,
    )
    version(
        "1.0",
        sha256="f8927228754fdfb21dbf08b9e67c5f97e06764c4adf327a4126eed84b1508f3d",
        deprecated=True,
    )
    version(
        "0.9.7",
        sha256="46e150998723fd1937da598f47f49fe47e40c1f57ec594436c6ef1e0145b44dc",
        deprecated=True,
    )

    depends_on("r@3.0.0:", type=("build", "run"))
    depends_on("curl", when="@4.3:")
    depends_on("curl@:7.63", when="@:4.0")

    # https://bugs.freebsd.org/bugzilla/show_bug.cgi?id=282908
    requires("curl@:8.10", when="@:5.2.1")

    # (Jan 2025) MacOS ships a very buggy libcurl 8.7.1 so we avoid this until apple updates it
    # See: https://github.com/jeroen/curl/issues/376
    # from: https://github.com/jeroen/curl/blob/v6.2.0/configure#L18
    depends_on("curl@8.8.0:", when="@6.2.0: platform=darwin")
