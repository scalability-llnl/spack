# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyUproot(PythonPackage):
    """ROOT I/O in pure Python and NumPy.

    Uproot is a reader and a writer of the ROOT file format using only Python
    and Numpy. Unlike the standard C++ ROOT implementation, Uproot is only an
    I/O library, primarily intended to stream data into machine learning
    libraries in Python. Unlike PyROOT and root_numpy, Uproot does not depend
    on C++ ROOT. Instead, it uses Numpy to cast blocks of data from the ROOT
    file as Numpy arrays."""

    homepage = "https://github.com/scikit-hep/uproot4"
    pypi = "uproot/uproot-4.0.6.tar.gz"

    maintainers("vvolkl")

    tags = ["hep"]

    license("BSD-3-Clause")

    version("5.0.5", sha256="1a2ac98d595bde7c83c7d5b716d33bb74abd44df6e8d84af62c638edb6c9abab")
    version("5.0.4", sha256="c4ea1af198e3292a4649e3fe789d11b038c1ed57c10f167fc3f52100300c2eea")
    version("5.0.3", sha256="a4ab3f2ea0b98746f601d43115a64b36f9c2145e9793da1e1cd9aaca72f311ab")
    version("5.0.2", sha256="734f70d9e44f964d84bbe3de581aa4a96585be09049b3ad104623390d10ac828")
    version("5.0.1", sha256="0ee6790df1df1cd0125b636d7fc8bddc3517d5b665c84246148fe83c79b336aa")
    version("5.0.0", sha256="7e4a87e602c6d9cc245aeab779fe9686471bf49cec993182ded324b6119a421e")
    version("4.3.7", sha256="264f148edde4c4a778d9b347c4ae975fe70a910e87d069fbd2b53e1f99874f0e")
    version("4.3.6", sha256="1dc2dade0d25beec25aacb1c1b2cb6db10886e3a0c8b5cad6a96ae3f7e46059c")
    version("4.3.5", sha256="5d18e1a7af07d367e900ab746aba24676ac29849718ea1a9c8b652f95af8509a")
    version("4.3.4", sha256="45457307ebda62b1afa4838f60c1d05e04a1c703bb15f0fb37504de9bd2dd8f8")
    version("4.3.3", sha256="766a02fe5a51b9fe1965dea5548bada3b3e2574ba5c66848c8be9576ab3adfb9")
    version("4.3.2", sha256="33bb2da3f1969a4e248369b60a3a42a3828c5c6376011c44640c0b75d59816b1")
    version("4.3.1", sha256="36e608c43585fb653a1a90c134f6dab964caa9512a6dd8ea7b52969da0b537d0")
    version("4.3.0", sha256="be688a431ee272c22690c98bdd06d8a32ea00d4365b78eb11c71a8145a0f1184")
    version("4.2.4", sha256="3e16f92131d73839c4e2708385c6199ae7cb9568c20cf8bffce010b8a84d7fd8")
    version("4.2.3", sha256="ed0b7bf54f8e20e30a96aec119d85551cc5d37f107708a52b32a23ecc6ba6389")
    version("4.2.2", sha256="d7ce5b5ffff566463fcdebfdc6468bce003cd764f17cf99e94823b9b80a6d793")
    version("4.1.8", sha256="09c46edc864520af50d018055e3d3577a4c6c37489484a664edfa4f1496b6755")
    version("4.0.11", sha256="5c8f62c7eeaa50e1315e05469580130d0bcc50a6cb4456825777f73cfaf5938a")
    version("4.0.10", sha256="b7f9786d87227fcdc6b84305a6219cd615844f934e3b7c2509e2d4ed095950ab")
    version("4.0.9", sha256="345c20dd4e1921e3493200bf9ed4079909fb1277d02faf3136e19f4b90f8aa86")
    version("4.0.8", sha256="98282142725d678815ec6f8c76f42cfb3539c9c3d5b5561b8ef2129ac5a86bcd")
    version("4.0.7", sha256="7adb688601fda1e9ab8eeb9a9de681f645827dac0943c6180cf85f03f73fb789")
    version("4.0.6", sha256="1bea2ccc899c6959fb2af69d7e5d1e2df210caab30d3510e26f3fc07c143c37e")

    variant("xrootd", default=True, description="Build with xrootd support ")
    variant(
        "lz4",
        default=True,
        description="Build with support for reading " "lz4-compressed rootfiles ",
    )

    variant(
        "zstd",
        default=True,
        description="Build with support for reading " "zstd-compressed rootfiles ",
    )

    depends_on("python@2.6:2,3.5:", type=("build", "run"))
    depends_on("python@3.6:", type=("build", "run"), when="@4.2.0:")
    depends_on("py-hatchling", when="@5:", type="build")
    depends_on("py-setuptools", when="@:4", type=("build", "run"))
    depends_on("py-setuptools@42:", type=("build", "run"), when="@4.1.8:4")
    depends_on("py-awkward@2:", type=("build", "run"), when="@5:")
    depends_on("py-importlib-metadata", when="@5: ^python@:3.7", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-packaging", when="@5:", type=("build", "run"))

    depends_on("xrootd", when="+xrootd")

    depends_on("lz4", when="+lz4")
    depends_on("xxhash", when="+lz4")

    depends_on("zstd", when="+zstd")
