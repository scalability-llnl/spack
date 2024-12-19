# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PySnakemakeStoragePluginFs(PythonPackage):
    """A Snakemake storage plugin that reads and writes from a locally mounted filesystem
    using rsync."""

    homepage = "https://github.com/snakemake/snakemake-storage-plugin-fs"
    pypi = "snakemake_storage_plugin_fs/snakemake_storage_plugin_fs-0.1.5.tar.gz"

    license("MIT")

    version("1.0.6", sha256="8d8ead1883d7e670b1d34ea084f7c927bb4fab71fd8d221b7478680cc09a443e")
    version("1.0.5", sha256="4f7ce1bf16d10510f8f4a2fde2ae22d047131020bd5efa603132dabfc85f444b")
    version("1.0.4", sha256="d9467d2d8f00689c6af6478f67f693373ce3cb0404d10c6d783997465d5110a9")
    version("1.0.3", sha256="36086fc8a2970fd89218683655c345907a5834f07416f6c1ddf370489398f9c8")
    version("1.0.2", sha256="d9febf6acc3aea89c9e0e5f37c32e36f96bd5fda3a41b2e8f9925a250638cb84")
    version("1.0.1", sha256="47f27d0dad307f36cdfa7e25fa5164d3e6d313aa1c2417922cc31388d7c9ecd4")
    version("1.0.0", sha256="de4ed37232173b604fadbf93cd84b05a8c28fa3e1d3167426bef181c7256e22c")
    version("0.2.0", sha256="cad1859036cbf429ea6fdb97f242567ec54a36d0b6ff900ce0d3ecfb6a824ae7")

    depends_on("py-sysrsync@1.1.1:1", type=("build", "run"))
    depends_on("py-reretry@0.11.8:0.11", type=("build", "run"))

    depends_on("py-snakemake-interface-common@1.17:1", type=("build", "run"))
    depends_on(
        "py-snakemake-interface-storage-plugins@3.2.2:3", type=("build", "run"), when="@1.0.3:"
    )
    depends_on("py-snakemake-interface-storage-plugins@3.1:3", type=("build", "run"))

    depends_on("python@3.11:3", type=("build", "run"))
    depends_on("py-poetry-core", type="build")
