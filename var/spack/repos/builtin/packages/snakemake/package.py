# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Snakemake(PythonPackage):
    """Workflow management system to create reproducible and scalable data analyses."""

    homepage = "https://snakemake.readthedocs.io/en"
    pypi = "snakemake/snakemake-8.18.2.tar.gz"
    maintainers("marcusboden", "w8jcik")

    license("MIT")

    version("8.18.2", sha256="7dc8cdc3c836444c2bc3d67a4a7f4d703557c1bf96a90da18f312f4df9daefc4")
    version("8.5.2", sha256="cc94876263182277e4a429e5d371c867400eeddc791c114dfd090d1bb3158975")
    version("7.32.4", sha256="fdc3f15dd7b06fabb7da30d460e0a3b1fba08e4ea91f9c32c47a83705cdc7b6e")
    version("7.31.1", sha256="6fadcc9a051737aa187dccf437879b3b83ddc917fff9bd7d400e056cf17a1788")
    version("7.30.2", sha256="0cb86cf9b43b9f2f45d5685cd932595131031c7087690f64c5bc7eaec88df029")
    version("7.29.0", sha256="c420a545924b599390efe9e2fa7a07c01d167cceac63d1d06fa6eff5e7b43be0")
    version("7.28.3", sha256="4d0d5f9643d97154cd8925830bdb3922e4bd9cfcf7f8b619df75e4ddfdbc3f9e")
    version("7.26.0", sha256="5e5b4750a943f73a1b62979ccac203f4bc87876559f5e44d0ce9305ac198aff0")
    version("7.25.4", sha256="e89146fd0df196a9135dcf41c9c70841551aa4735a18da9e0402bda6746afdcc")
    version("7.24.2", sha256="3e9bcbb9743aa2a073922e90659e9209edbea89e6d22bf7b29ea538e60983908")
    version("7.23.1", sha256="4dc960a721d2d8eaebd9b10e56564e3742f78c65d36cd31966ed205afcc4253d")
    version("7.22.0", sha256="68d7bb4ab7555f7b58a3ba748a880024df919042cfb670da231886385de697cd")
    version("7.21.0", sha256="ebf91f4ca5c70809fcbfd2e8cbc982096cdadac1ec34138bb147b4a8c975c85b")
    version("7.20.0", sha256="f5b45191f1d419ebf28606880cb9bfac3bfa7c5949d1d2b64f551586d4212a2a")
    version("7.19.1", sha256="390ad5e2d5106e84700b7219c0eddf41d61be2205787d77a815fa91e4d624f33")
    version("7.19.0", sha256="423bb6f10013d874b6b71c06cbb45b2935ce1a291f74e1fc1614efa44b08c3e7")
    version("7.18.2", sha256="23f52b9a0c86da3b974a3cfc097fa82b41c49dab05543c0d18377c854852f771")
    version("6.15.1", sha256="a219601d57037f565ead9963e6bd8d04d3bdd985d172371e54197dcbdba79865")
    version("6.13.1", sha256="22f57dcd8b1ca8a30aaa45c5d2c0f56d381d4731abd0988f24f9de46b7d9827c")
    version("6.12.3", sha256="af86af9a540da3dceb05dad1040f1d3d733e6a695f8b3f8c30f8cf3bc6570a88")

    depends_on("python@3.11:", type=("build", "run"), when="@8:")
    depends_on("python@3.7:", type=("build", "run"), when="@7.31.1:7")
    depends_on("python@3.9:", type=("build", "run"), when="@7.30.2:7.31.1")

    depends_on("py-setuptools@42:", type=("build", "run"), when="@7:")
    depends_on("py-setuptools", type=("build", "run"))
    depends_on("py-tomli", type=("build"), when="@7.20.0: ^python@:3.10")

    depends_on("py-appdirs", type=("build", "run"))
    depends_on("py-immutables", type=("build", "run"), when="@8:")
    depends_on("py-configargparse", type=("build", "run"))
    depends_on("py-connectionpool@0.0.3:", type=("build", "run"))
    depends_on("py-datrie", type=("build", "run"))
    depends_on("py-docutils", type=("build", "run"))
    depends_on("py-gitpython", type=("build", "run"))
    depends_on("py-humanfriendly", type=("build", "run"), when="@7.20.0:")
    depends_on("py-jinja2@3", type=("build", "run"), when="@7:")
    depends_on("py-jsonschema", type=("build", "run"))
    depends_on("py-nbformat", type=("build", "run"))
    depends_on("py-packaging", type=("build", "run"), when="@7.29.0:")
    depends_on("py-psutil", type=("build", "run"))
    depends_on("py-pulp@2.3.1:2.8", type=("build", "run"), when="@8.1.2:")
    depends_on("py-pulp@2:", type=("build", "run"), when="@:8.1.1")
    depends_on("py-pyyaml", type=("build", "run"))

    depends_on("py-requests@2.8.1:2", type=("build", "run"), when="@8.4.12")
    depends_on("py-requests", type=("build", "run"))

    depends_on("py-reretry", type=("build", "run"), when="@7:")

    depends_on("py-smart-open@4:7", type=("build", "run"), when="@8.11:")
    depends_on("py-smart-open@3:7", type=("build", "run"), when="@8.8:8.10")
    depends_on("py-smart-open@3:6", type=("build", "run"), when="@8.4.12:8.7")
    depends_on("py-smart-open@3:", type=("build", "run"))

    depends_on(
        "py-snakemake-interface-executor-plugins@9.2:9", type=("build", "run"), when="@8.15.0:"
    )
    depends_on(
        "py-snakemake-interface-executor-plugins@9.1:9", type=("build", "run"), when="@8.10.1:"
    )
    depends_on(
        "py-snakemake-interface-executor-plugins@9.0.2:9", type=("build", "run"), when="@8.10:"
    )
    depends_on("py-snakemake-interface-executor-plugins@9", type=("build", "run"), when="@8.6:")
    depends_on(
        "py-snakemake-interface-executor-plugins@8.1.3:8", type=("build", "run"), when="@8:8.5"
    )

    depends_on("py-snakemake-interface-common@1.17:1", type=("build", "run"), when="@8.4.10:")
    depends_on("py-snakemake-interface-common@1.15:1", type=("build", "run"), when="@8:")

    depends_on(
        "py-snakemake-interface-storage-plugins@3.2.3:3", type=("build", "run"), when="@8.15.1:"
    )
    depends_on(
        "py-snakemake-interface-storage-plugins@3.1:3", type=("build", "run"), when="@8.4.10:"
    )
    depends_on("py-snakemake-interface-storage-plugins@3", type=("build", "run"), when="@8:")

    depends_on("py-snakemake-interface-report-plugins@1", type=("build", "run"), when="@8.5:")
    depends_on("py-stopit", type=("build", "run"))
    depends_on("py-tabulate", type=("build", "run"))
    depends_on("py-throttler", type=("build", "run"), when="@7:")
    depends_on("py-toposort@1.10:1", type=("build", "run"), when="@8.4.12:")
    depends_on("py-toposort@1.10:", type=("build", "run"), when="@7.24.0:")
    depends_on("py-toposort", type=("build", "run"), when="@:7.23")
    depends_on("py-wrapt", type=("build", "run"))
    depends_on("py-yte@1.5.1:1", type=("build", "run"), when="@7.28.1:")
    depends_on("py-yte@1", type=("build", "run"), when="@7:7.28.0")
    depends_on("py-dpath@2.1.6:2", type=("build", "run"), when="@8.3:")
    depends_on("py-conda-inject@1.3.1:1", type=("build", "run"), when="@8:")

    variant("reports", default=False, description="Generate self-contained HTML reports")

    with when("+reports"):
        depends_on("py-pygments", type=("build", "run"))

        depends_on("py-jinja2", type=("build", "run"), when="@:7.19.1")
        depends_on("py-networkx", type=("build", "run"), when="@:7.1.1")
        depends_on("py-pygraphviz", type=("build", "run"), when="@:7.1.1")

    variant("google-cloud", default=False, description="Enable Google Cloud execution", when="@:7")

    with when("+google-cloud"):
        depends_on("py-google-api-python-client", type=("build", "run"))
        depends_on("py-google-cloud-storage", type=("build", "run"))
        depends_on("py-google-crc32c", type=("build", "run"))
        depends_on("py-oauth2client", type=("build", "run"))

    variant("azure", default=False, description="Enable Azure execution", when="@7.28.0:7")

    with when("+azure"):
        depends_on("py-azure-storage-blob", type=("build", "run"))
        depends_on("py-azure-batch", type=("build", "run"))
        depends_on("py-azure-core", type=("build", "run"))
        depends_on("py-azure-identity", type=("build", "run"))
        depends_on("py-azure-mgmt-batch", type=("build", "run"))

    depends_on("py-msrest", type=("build", "run"), when="@7.28.0")
    depends_on("py-filelock", type=("build", "run"), when="@:6")
    depends_on("py-ratelimiter", type=("build", "run"), when="@:6")

    variant("ftp", default=False, description="Handling input and output via FTP", when="@:7")
    depends_on("py-ftputil", when="+ftp", type=("build", "run"))

    variant(
        "s3", default=False, description="Amazon S3 API storage (AWS S3, MinIO, etc.)", when="@:7"
    )
    depends_on("py-boto3", when="+s3", type=("build", "run"))
    depends_on("py-botocore", when="+s3", type=("build", "run"))

    variant(
        "http", default=False, description="Downloading of input files from HTTP(s)", when="@:7"
    )
    depends_on("py-requests", when="+http", type=("build", "run"))

    def test_run(self):
        """Test if snakemake runs with the version option"""
        Executable(self.prefix.bin.snakemake)("--version")
