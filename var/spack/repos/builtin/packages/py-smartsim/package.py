# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class PySmartsim(PythonPackage):
    """A workflow library to easily integrate machine learning libraries with
    high performance computing simulations and applications
    """

    homepage = "https://www.craylabs.org/docs/overview.html"
    git = "https://github.com/CrayLabs/SmartSim"
    pypi = "smartsim/smartsim-0.5.0.tar.gz"

    maintainers("MattToast")

    license("BSD-2-Clause")

    version("0.5.0", sha256="35b36243dc84af62261a7f772bae92f0b3502faf01401423899cb2a48339858c")

    variant("torch", default=True, description="Build with the pytorch backend")

    depends_on("python@3.8:3.10", type=("build", "run"))
    depends_on("py-setuptools@39.2:", type=("build",))
    depends_on("cmake@3.13:", type=("build",))

    depends_on("py-psutil@5.7.2:", type=("build", "run"))
    depends_on("py-coloredlogs@10:", type=("build", "run"))
    depends_on("py-tabulate@0.8.9:", type=("build", "run"))
    depends_on("py-redis@4.5:", type=("build", "run"))
    depends_on("py-tqdm@4.50.2:", type=("build", "run"))
    depends_on("py-filelock@3.4.2:", type=("build", "run"))
    depends_on("py-protobuf@3.20:3", type=("build", "run"))

    # Companion libs
    depends_on("py-smartredis@0.4.1:", type=("build", "run"), when="@0.5.0")

    # Backends
    # SmartSim defines sensible and well tested lower bounds for redis
    # for the CLI to fetch in the `smartsim._core._install.buildenv.Versioner`
    # class (lower versions are unable to parse the default `redis.conf` shipped
    # with SmartSim), but allows users to upgrade explicitly by setting
    # environment variables.
    depends_on("redis@7.0.5:", type=("build", "run"))
    depends_on("redis-ai", type=("build", "run"))

    # ML Deps
    # The lower bound for these py-* deps can be found in the source code
    # at `smartsim/_core/_install/buildenv.py`.
    with when("+torch"):
        depends_on("redis-ai+torch", type=("build", "run"))
        depends_on("py-torch@1.11.0:", type=("build", "run"))
        depends_on("py-torchvision@0.12.0:", type=("build", "run"))

    # By default, the SmartSim `setup.py` will attempt to fetch and build
    # its own copy of Redis. This should be patched out and the version of
    # Redis retrieved through spack should be used instead.
    patch("ss-dont-build-db.patch")

    # SmartSim provides its own CLI to fetch and build its own
    # copy of Redis, RedisAI, and ML deps. This functionality should be
    # patched out so that users do not accidentally overwrite/break
    # dependencies fetched though Spack
    patch("ss-0-5-0-remove-cli-build-fns.patch")

    def setup_build_environment(self, env):
        env.set("BUILD_JOBS", make_jobs)

    @run_after("install")
    def symlink_bin_deps(self):
        ss_core_path = join_path(python_purelib, "smartsim", "_core")
        os.symlink(
            self.spec["redis"].prefix.bin.join("redis-server"),
            join_path(ss_core_path, "bin", "redis-server"),
        )
        os.symlink(
            self.spec["redis"].prefix.bin.join("redis-cli"),
            join_path(ss_core_path, "bin", "redis-cli"),
        )
        os.symlink(self.spec["redis-ai"].prefix, join_path(ss_core_path, "lib"))
