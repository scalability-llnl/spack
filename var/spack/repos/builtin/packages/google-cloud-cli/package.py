# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import platform

from spack.package import *

versions = {
    "504.0.1": {
        "darwin": {
            "arm": "00485cda52bcb80ae796914304dff59ec609eafe1153474746c5ac3bc576a574",
            "x86": "3400783268ff25bfdab23ad52ad7de00e2b794ce6d14790316af77e84f7eb3f0",
            "x86_64": "7900504a22bb918563d74446a794308eb3da55e7e2b0b20d6545c950def7ffd0",
        },
        "linux": {
            "arm": "89d148e4dc5837a6ed7292237b49171051ce054886838ada0aca4f4f3f9b7bba",
            "x86": "e85d4623795ef3bb3d003b457b65f2599176432bacdec92d6010d12922b75df4",
            "x86_64": "a01ff5312980a18b073c9d2cd6f287ff7d2684f33bd4c927aec20d1d17344874",
        },
        "windows": {
            "arm": "33601f2e3e8b13baaad74216d401f3e40e475a30bcfc50bf7d8c5e57247a5e64",
            "x86": "c5c00ecac095e60fa347b124c024496e7af3cf3d61de5a68be766ee7c997b987",
            "x86_64": "02665dc0b9c76c154029e921cecd493da8023de491439c99557cf36fd4b4d954",
        },
    },
    "426.0.0": {
        "darwin": {
            "arm": "5228c93f04af2e3eda3cf03c18bcc75a5440c62170fcdcd46e77e4e97452786a",
            "x86": "dd95eb5f3ef82825f3e930f538c3964c5ae37e3bf35492e21f5fed3916b980c0",
            "x86_64": "1ac867378e8e6d59aacadfa0a5282b549146cd8bcd971341d047006c6f702c63",
        },
        "linux": {
            "arm": "8409b8cc00f0ae8089be97d8a565f4072eada890776345bccb988bcd4d4bb27f",
            "x86": "13e8b75a3ba352bda58e9974ed5779c16a6631e2957ea6e43cf3b11d5da49ae7",
            "x86_64": "c653a8ac1e48889005fd00e2de580a27be5a3cb46ceccc570146982c4ddf4245",
        },
        "windows": {
            "arm": "d45bdb6808ca737b6c14d6ac85f3380ab1037eeb3c641164d5d4fad032d382af",
            "x86": "c04c39b6a7c82365f3c4a0d79ed60dbc6c5ce672970a87a70478bb7c55926852",
            "x86_64": "2a5199f04414df36e483c892d0e89cdc9e962266414ce7990cf2b59058b94e9b",
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

    depends_on("c", type="build")

    # RELEASE_NOTES
    with default_args(type=("build", "run")):
        depends_on("python")
        depends_on("python@:3.13", when="@500:")
        depends_on("python@:3.12", when="@456:499")
        depends_on("python@:3.10", when="@:455")

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
