# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDatalad(PythonPackage):
    """data distribution geared toward scientific datasets.

    DataLad makes data management and data distribution more accessible. To do
    that, it stands on the shoulders of Git and Git-annex to deliver a
    decentralized system for data exchange. This includes automated ingestion
    of data from online portals and exposing it in readily usable form as
    Git(-annex) repositories, so-called datasets. The actual data storage and
    permission management, however, remains with the original data providers.
    """

    homepage = "https://datalad.org/"
    pypi = "datalad/datalad-0.14.6.tar.gz"
    git = "https://github.com/datalad/datalad.git"

    version("0.18.4", sha256="d832f3d70b79b7b66519ca30315791a6a265bdf8a86ddac5846489b75385cb09")
    version("0.18.3", sha256="2da57df609f62a52a6652ade802e8ce0f229d498a5b93b15df2b8c69f8875b6e")
    version("0.17.5", sha256="a221312c58b0b9b57605cc1a2288838f24932491b2e50475dd7a940151cafccd")
    version("0.15.5", sha256="e569494a5bd4e0f100013ec30529d5ac02e78ba476a75fc533c0d89c0e5473bc")
    version("0.15.3", sha256="44f8c5b3960c6d9848aeecd868c82330c49689a21e975597df5b112dc2e5c9f0")
    version("0.15.2", sha256="1a878cf521270f089ee1f50339e71cfd7eed41e708d895a12d5c483a9b59991b")
    version("0.15.1", sha256="0a905b3c3419786ae85b61a7aee34b0fc9eecd814f38408f2767ae7122b57a8b")
    version("0.14.6", sha256="149b25a00da133a81be3cbdc041a1985418f0918fa5961ba979e23b5b3c08c63")

    variant("downloaders-extra", default=False, description="Enable extra downloaders support")
    variant("misc", default=False, description="Enable misc")
    variant("tests", default=False, description="Enable tests")
    variant("duecredit", default=False, description="Enable duecredit support")
    variant("full", default=False, description="Enable support for all available variants")

    variant(
        "metadata-extra", when="@:0.17", default=False, description="Enable extra metadata support"
    )

    depends_on("py-setuptools@40.8.0:", type="build")
    # upper bound needed because otherwise the following error occurs:
    # 'extras_require' must be a dictionary whose values are strings or lists
    # of strings containing valid project/version requirement specifiers.
    depends_on("py-setuptools@40.8.0:66", when="@:17", type="build")

    depends_on("git", type=("build", "run"))
    depends_on("git-annex", type=("build", "run"))

    # core
    depends_on("py-platformdirs", when="@0.16:", type=("build", "run"))
    depends_on("py-chardet@3.0.4:", when="@0.18.2:", type=("build", "run"))
    depends_on("py-chardet@3.0.4:4", when="@:0.18.1", type=("build", "run"))
    depends_on("py-colorama", when="platform=windows", type=("build", "run"))
    depends_on("py-distro", when="^python@3.8:", type=("build", "run"))
    depends_on("py-importlib-metadata@3.6:", when="@0.16: ^python@:3.9", type=("build", "run"))
    depends_on("py-importlib-metadata", when="@:0.15 ^python@:3.7", type=("build", "run"))
    depends_on("py-iso8601", type=("build", "run"))
    depends_on("py-humanize", type=("build", "run"))
    depends_on("py-fasteners@0.14:", type=("build", "run"))
    depends_on("py-packaging", when="@0.15.4:", type=("build", "run"))
    depends_on("py-patool@1.7:", type=("build", "run"))
    depends_on("py-tqdm", type=("build", "run"))
    depends_on("py-typing-extensions@4:", when="@0.18.4: ^python@:3.10", type=("build", "run"))
    depends_on("py-typing-extensions", when="@0.18.3: ^python@:3.9", type=("build", "run"))
    depends_on("py-annexremote", type=("build", "run"))
    depends_on("py-looseversion", when="@0.18:", type=("build", "run"))
    depends_on("py-appdirs", when="@:0.15", type=("build", "run"))
    depends_on("py-wrapt", when="@:0.15", type=("build", "run"))

    # downloaders
    depends_on("py-boto", type=("build", "run"))
    depends_on("py-keyring@20.0:23.8,23.9.1:", when="@0.16:", type=("build", "run"))
    depends_on("py-keyring@8.0:", type=("build", "run"))
    depends_on("py-keyrings-alt", type=("build", "run"))
    depends_on("py-msgpack", type=("build", "run"))
    depends_on("py-requests@1.2:", type=("build", "run"))

    # publish
    depends_on("py-python-gitlab", when="@0.14.7:", type=("build", "run"))
    depends_on("py-pygithub", when="@:0.16", type=("build", "run"))
    depends_on("py-jsmin", when="@:0.14", type=("build", "run"))

    # metadata
    with when("@:0.17"):
        depends_on("py-simplejson", type=("build", "run"))
        depends_on("py-whoosh", type=("build", "run"))

    with when("+downloaders-extra"):
        depends_on("py-requests-ftp", type=("build", "run"))

    with when("+misc"):
        depends_on("py-argcomplete@1.12.3:", when="@0.16.5:", type=("build", "run"))
        depends_on("py-argcomplete", when="@0.14.7:", type=("build", "run"))
        depends_on("py-pyperclip", type=("build", "run"))
        depends_on("py-python-dateutil", type=("build", "run"))

    with when("+tests"):
        depends_on("py-beautifulsoup4", type=("build", "run"))
        depends_on("py-httpretty@0.9.4:", type=("build", "run"))
        depends_on("py-mypy", when="@0.18.3:", type=("build", "run"))
        depends_on("py-mypy@0.900:0", when="@0.17.4:0.18.2", type=("build", "run"))
        depends_on("py-pytest", when="@0.17.9:", type=("build", "run"))
        depends_on("py-pytest@7", when="@0.17.0:0.17.8", type=("build", "run"))
        depends_on("py-pytest-cov", when="@0.17.9:", type=("build", "run"))
        depends_on("py-pytest-cov@3", when="@0.17.0:0.17.8", type=("build", "run"))
        depends_on("py-pytest-fail-slow@0.2:0", when="@0.17:", type=("build", "run"))
        depends_on("py-types-python-dateutil", when="@0.17.4:", type=("build", "run"))
        depends_on("py-types-requests", when="@0.17.4:", type=("build", "run"))
        depends_on("py-vcrpy", type=("build", "run"))
        depends_on("py-nose@1.3.4:", when="@:0.16", type=("build", "run"))

    with when("+duecredit"):
        depends_on("py-duecredit", type=("build", "run"))

    # for version @:0.17
    with when("+metadata-extra"):
        depends_on("py-pyyaml", type=("build", "run"))
        depends_on("py-mutagen@1.36:", type=("build", "run"))
        depends_on("py-exifread", type=("build", "run"))
        depends_on("py-python-xmp-toolkit", type=("build", "run"))
        depends_on("pil", type=("build", "run"))

    # full
    # use conflict to avoid to have to maintain the dependencies twice
    conflicts("~downloaders-extra", when="+full")
    conflicts("~misc", when="+full")
    conflicts("~tests", when="+full")
    conflicts("~duecredit", when="+full")

    # for version @:0.17
    conflicts("~metadata-extra", when="+full")

    install_time_test_callbacks = ["test", "installtest"]

    def installtest(self):
        datalad = Executable(self.prefix.bin.datalad)
        datalad("wtf")
