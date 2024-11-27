# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyRay(PythonPackage):
    """Ray provides a simple, universal API for building distributed applications."""

    homepage = "https://github.com/ray-project/ray"
    url = "https://github.com/ray-project/ray/archive/ray-0.8.7.tar.gz"

    license("Apache-2.0")

    version("2.0.1", sha256="b8b2f0a99d2ac4c001ff11c78b4521b217e2a02df95fb6270fd621412143f28b")
    version("0.8.7", sha256="2df328f1bcd3eeb4fa33119142ea0d669396f4ab2a3e78db90178757aa61534b")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("default", default=False, description="Install default extras", when="@2.0.1")

    depends_on("python@3.6:3.10", when="@2.0.1", type=("build", "run"))
    depends_on("python@3.6:3.8", when="@0.8.7", type=("build", "run"))
    depends_on("bazel@4.2.2", when="@2.0.1", type="build")
    depends_on("bazel@3.2.0", when="@0.8.7", type="build")
    depends_on("npm", type="build")
    depends_on("py-setuptools", type="build")
    depends_on("py-cython@0.29.26:", when="@2.0.1", type="build")
    depends_on("py-cython@0.29.14:", when="@0.8.7", type="build")
    depends_on("py-attrs", when="@2.0.1", type=("build", "run"))
    depends_on("py-click@7:8.0.4", when="@2.0.1", type=("build", "run"))
    depends_on("py-click@7.0:", when="@0.8.7", type=("build", "run"))
    depends_on("py-filelock", type=("build", "run"))
    depends_on("py-grpcio@1.32:1.43.0", when="@2.0.1 ^python@:3.9", type=("build", "run"))
    depends_on("py-grpcio@1.42:1.43.0", when="@2.0.1 ^python@3.10:", type=("build", "run"))
    depends_on("py-grpcio@1.28.1:", when="@0.8.7", type=("build", "run"))
    depends_on("py-jsonschema", type=("build", "run"))
    depends_on("py-msgpack@1", type=("build", "run"))
    depends_on("py-numpy@1.16:", when="^python@:3.8", type=("build", "run"))
    depends_on("py-numpy@1.19.3:", when="^python@3.9:", type=("build", "run"))
    depends_on("py-protobuf@3.15.3:3", when="@2.0.1", type=("build", "run"))
    depends_on("py-protobuf@3.8.0:", when="@0.8.7", type=("build", "run"))
    depends_on("py-pyyaml", type=("build", "run"))
    depends_on("py-frozenlist", when="@2.0.1", type=("build", "run"))
    depends_on("py-requests", type=("build", "run"))
    depends_on("py-typing-extensions", when="@2.0.1 ^python@:3.7", type=("build", "run"))
    depends_on("py-virtualenv", when="@2.0.1", type=("build", "run"))

    with when("+default"):
        depends_on("py-aiohttp@3.7:", type=("build", "run"))
        depends_on("py-aiohttp-cors", type=("build", "run"))
        depends_on("py-colorful", type=("build", "run"))
        depends_on("py-py-spy@0.2:", type=("build", "run"))
        depends_on("py-gpustat@1:", type=("build", "run"))
        depends_on("py-opencensus", type=("build", "run"))
        depends_on("py-pydantic", type=("build", "run"))
        depends_on("py-prometheus-client@0.7.1:0.13", type=("build", "run"))
        depends_on("py-smart-open", type=("build", "run"))

    # Historical dependencies
    with when("@0.8.7"):
        depends_on("py-aiohttp", type=("build", "run"))
        depends_on("py-aioredis", type=("build", "run"))
        depends_on("py-colorama", type=("build", "run"))
        depends_on("py-colorful", type=("build", "run"))
        depends_on("py-google", type=("build", "run"))
        depends_on("py-gpustat", type=("build", "run"))
        depends_on("py-py-spy@0.2.0:", type=("build", "run"))
        depends_on("py-redis@3.3.2:3.4", type=("build", "run"))
        depends_on("py-opencensus", type=("build", "run"))
        depends_on("py-prometheus-client@0.7.1:", type=("build", "run"))
        # If not guarded by SKIP_THIRDPARTY_INSTALL, those dependencies
        # would be automatically installed via pip by the setup.py script.
        depends_on("py-setproctitle", type=("build", "run"))
        depends_on("py-psutil", type=("build", "run"))
        # If not detected during install, the following dependency would
        # be automatically downloaded and installed by the setup.py script.
        depends_on("py-pickle5", when="^python@:3.8.1", type=("build", "run"))

    build_directory = "python"

    def patch(self):
        filter_file(
            'bazel_flags = ["--verbose_failures"]',
            f'bazel_flags = ["--verbose_failures", "--jobs={make_jobs}"]',
            join_path("python", "setup.py"),
            string=True,
        )

    def setup_build_environment(self, env):
        env.set("SKIP_THIRDPARTY_INSTALL", "1")

    # Compile the dashboard npm modules included in the project
    @run_before("install")
    def build_dashboard(self):
        with working_dir(join_path("python", "ray", "dashboard", "client")):
            npm = which("npm")
            npm("ci")
            npm("run", "build")
