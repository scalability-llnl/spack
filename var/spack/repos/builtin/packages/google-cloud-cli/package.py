# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import platform

from spack.package import *

versions = {
    "502.0.0": {
        "linux": {
            "arm": "9a7315d287347d77f45e399ac13b51e6fcde8a1120d14faa7cd47e7ee959a6e6",
            "x86_64": "b40e9fe64c3d2b0c7ff289b50ca39f572cce54c783c0f8579810f2307c8fdf0b",
            "x86": "cad9ef0f5072a967ff6eb495b7fffb550ee63455fde9231e6155b471fd583d98",
        },
        "darwin": {
            "arm": "40a14db24af99154b6b42aeb114f2828711d3209b72e7a583ad3ca0b4c669f87",
            "x86_64": "8af3013b524591ef5347a3df48caa9d4b1a3510c50c1d45b64442a365c021f65",
            "x86": "0c652a53cc577e9157e4ae48ead5d28645dc81901b5db3940c79171a401986c6",
        },
        "windows": {
            "arm": "65f6c6f441099ab27355fa7bbbcbbebe954b1cffcee3cc89cfc3f8ce30940640",
            "x86_64": "82270ab11e486c50e552a8ec4e4152a234ddd97d23d062deb85d5d91faa8e5e7",
            "x86": "19fd1d359d4efd0824f89e568b08d58d734d78c1bee66f34b0e29dd9c43b1ce2",
        },
    },
    "456.0.0": {
        "linux": {
            "arm": "14ff9f3f5b289411b79a1612b5b7a457b2ea9997df5638df5f50273c1ba0189b",
            "x86_64": "c653ae1f92f1442f8bfb8d398cc5e945104bc2068f6d7e52454458b99d420dd0",
            "x86": "d5761f65a9756bb9e1b36dbac6f26da2544e967e0ec2df6c5795895afda66b87",
        },
        "darwin": {
            "arm": "829d9b8b312bbb58ecf766ca68d8077c3b72cb2b5874d5b0b90cecb66efeea44",
            "x86_64": "b77530b1c66fcc81b91fcc13ac8b6d246c90da25822a6fad30ebab687a6493b4",
            "x86": "5bd4cc63c413b83e5f37777f9b38043a86647542adfd01e40626d11563f8da83",
        },
        "windows": {
            "arm": "f2bb7617f35b7b97051b9f18a736803bc8b090cd88398e95e118daff8ba2275c",
            "x86_64": "706430bc39927a2912e3e7379ae9d9521ca9739eb609661c816695ef8db31317",
            "x86": "614d8caf10329a3e5a1a67773fd2b580b35be3847bc777879edb1ab5075bc1e9",
        },
    },
    "426.0.0": {
        "linux": {
            "arm": "8409b8cc00f0ae8089be97d8a565f4072eada890776345bccb988bcd4d4bb27f",
            "x86_64": "c653a8ac1e48889005fd00e2de580a27be5a3cb46ceccc570146982c4ddf4245",
            "x86": "13e8b75a3ba352bda58e9974ed5779c16a6631e2957ea6e43cf3b11d5da49ae7",
        },
        "darwin": {
            "arm": "5228c93f04af2e3eda3cf03c18bcc75a5440c62170fcdcd46e77e4e97452786a",
            "x86_64": "1ac867378e8e6d59aacadfa0a5282b549146cd8bcd971341d047006c6f702c63",
            "x86": "dd95eb5f3ef82825f3e930f538c3964c5ae37e3bf35492e21f5fed3916b980c0",
        },
        "windows": {
            "arm": "d45bdb6808ca737b6c14d6ac85f3380ab1037eeb3c641164d5d4fad032d382af",
            "x86_64": "2a5199f04414df36e483c892d0e89cdc9e962266414ce7990cf2b59058b94e9b",
            "x86": "c04c39b6a7c82365f3c4a0d79ed60dbc6c5ce672970a87a70478bb7c55926852",
        },
    },
}

targets = {"aarch64": "arm", "arm64": "arm", "amd64": "x86_64", "x86_64": "x86_64", "x86": "x86"}


class GoogleCloudCli(Package):
    """Create and manage Google Cloud resources and services directly on the command line
    or via scripts using the Google Cloud CLI."""

    homepage = "https://cloud.google.com/cli"

    # https://cloud.google.com/sdk/docs/downloads-versioned-archives
    system = platform.system().lower()
    machine = platform.machine().lower()
    if machine in targets:
        machine = targets[machine]
    ext = "zip" if system == "windows" else "tar.gz"

    license("Apache-2.0")

    for ver in versions:
        if system in versions[ver] and machine in versions[ver][system]:
            version(ver, sha256=versions[ver][system][machine])

    depends_on("c", type="build")  # generated

    with default_args(type=("build", "run")):
        depends_on("python@3.8:3.13", when="@500:")
        depends_on("python@3.8:3.12", when="@456:499")
        depends_on("python@3.8:3.10", when="@488:")
        depends_on("python@3.5:", when="@427:")

    def url_for_version(self, version):
        return f"https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-{version}-{self.system}-{self.machine}.{self.ext}"

    def setup_build_environment(self, env):
        # https://cloud.google.com/sdk/gcloud/reference/topic/startup
        env.set("CLOUDSDK_PYTHON", self.spec["python"].command.path)
        # ~70 dependencies with no hints as to what versions are supported, just use bundled deps
        env.set("CLOUDSDK_PYTHON_SITEPACKAGES", "0")

    def setup_run_environment(self, env):
        self.setup_build_environment(env)

    def install(self, spec, prefix):
        # https://cloud.google.com/sdk/docs/install
        installer = Executable(r".\install.bat" if self.system == "windows" else "./install.sh")
        installer(
            "--usage-reporting=false",
            "--screen-reader=false",
            "--command-completion=false",
            "--path-update=false",
            "--quiet",
            "--install-python=false",
            "--no-compile-python",
        )

        install_tree("bin", prefix.bin)
        install_tree("lib", prefix.lib)
