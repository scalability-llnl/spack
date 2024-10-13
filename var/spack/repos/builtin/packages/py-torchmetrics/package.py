# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTorchmetrics(PythonPackage):
    """Machine learning metrics for distributed, scalable PyTorch applications."""

    homepage = "https://github.com/PyTorchLightning/metrics"
    pypi = "torchmetrics/torchmetrics-0.3.1.tar.gz"

    license("Apache-2.0")
    maintainers("adamjstewart")

    version("1.4.3", sha256="5554a19167e91f543afe82ff58a01059c8eec854359ad22896449c2c8fb0ad89")
    version("1.4.2", sha256="7a40cbec85e5645090812b87601696b4adf158294ec8c407ae58a71710938b87")
    version("1.4.0", sha256="0b1e5acdcc9beb05bfe369d3d56cfa5b143f060ebfd6079d19ccc59ba46465b3")
    version("1.3.2", sha256="0a67694a4c4265eeb54cda741eaf5cb1f3a71da74b7e7e6215ad156c9f2379f6")
    version("1.3.1", sha256="8d371f7597a1a5eb02d5f2ed59642d6fef09093926997ce91e18b1147cc8defa")
    version(
        "1.3.0",
        sha256="e8ac3adcc61e7a847d0504b0a0e0a3b7f57796178b239c6fafb5d20c0c9460ac",
        deprecated=True,
    )  # Yanked
    version("1.2.1", sha256="217387738f84939c39b534b20d4983e737cc448d27aaa5340e0327948d97ca3e")
    version("1.2.0", sha256="7eb28340bde45e13187a9ad54a4a7010a50417815d8181a5df6131f116ffe1b7")
    version("1.1.1", sha256="65ea34205c0506eecfd06b98f63f4d2a2c5c0e17367cf324e1747adc854c80a5")
    version("1.1.0", sha256="94b51aeb3d5ff55503fa47086bbc2af9e26efabb840e2d3c2381db9623dda5fd")
    version("1.0.3", sha256="1c20ea2f0db434334e88da6c015ddf936d43379bfb403e9dc2a7272b0eab453c")
    version("1.0.2", sha256="537989d02337814e621a45232eeb1eacfd4700a66c2b5161d19ca2158246e075")
    version("0.11.4", sha256="1fe45a14b44dd65d90199017dd5a4b5a128d56a8a311da7916c402c18c671494")
    version("0.11.3", sha256="6a2bcc17361f0e4c1668c92595b12ef30ccf9ef1d03263bee7c6136a882afe30")
    version("0.11.2", sha256="5a1f5fff9b1fb695bbcab6442d768e2e9b9535d00f4b4dea9ce03d40c866be07")
    version("0.11.1", sha256="de2e9feb3316f798ab08b318302ff04e764f47e691f0847f780044279fa176ca")
    version("0.11.0", sha256="c838e0491d80775daadd0802e27ae3af112a52086c9ba8cbcd1e2807243c89ac")
    version("0.10.3", sha256="9e6ab66175f2dc13e246c37485b2c27c77931dfe47fc2b81c76217b8efdc1e57")
    version("0.10.2", sha256="daa29d96bff5cff04d80eec5b9f5076993d6ac9c2d2163e88b6b31f8d38f7c25")
    version("0.10.1", sha256="e892ecd413e6bf63950329d1317c70f697d81d0f7e386152238062e322c8f1f3")
    version("0.10.0", sha256="990bafc7f76d7442894533771d0ba7492dbca2bbf2989fb32de7e9c68eb3d133")
    version("0.9.3", sha256="4ebfd2466021db26397636966ee1a195d3b340ba5d71bb258e764340dfc2476f")
    version("0.9.2", sha256="8178c9242e243318093d9b7237738a504535193d2006da6e58b0ed4003e318d2")
    version("0.9.0", sha256="3aa32ea575915b313d872d3460996c0f12a7bb37e6ce3da0e8d80865603b89f6")
    version("0.7.0", sha256="dbfb8989086f38020045a935e83928504e1af1d84ae92b073f6a83d018f4bc00")
    version("0.5.1", sha256="22fbcb6fc05348ca3f2bd06e0763e88411a6b68c2b9fc26084b39d40cc4021b0")
    version("0.4.1", sha256="2fc50f812210c33b8c2649dbb1482e3c47e93cae33e4b3d0427fb830384effbd")
    version("0.3.1", sha256="78f4057db53f7c219fdf9ec9eed151adad18dd43488a44e5c780806d218e3f1d")
    version("0.2.0", sha256="481a28759acd2d77cc088acba6bc7dc4a356c7cb767da2e1495e91e612e2d548")

    variant("image", default=False, description="image support", when="@0.11.2:")

    # setup.py
    depends_on("py-setuptools", type="build")

    # requirements/base.txt (upper bound is removed during processing)
    with default_args(type=("build", "run")):
        depends_on("py-numpy@1.20.1:", when="@1:")
        depends_on("py-numpy@1.17.2:", when="@0.4:")
        depends_on("py-numpy", when="@0.3:")
        depends_on("py-packaging@17.2:", when="@1.2.1:")
        depends_on("py-packaging", when="@0.3:1.1.0")
        depends_on("py-torch@1.10:", when="@1.3:")
        depends_on("py-torch@1.8.1:", when="@0.11:")
        depends_on("py-torch@1.3.1:")
        depends_on("py-typing-extensions", when="@0.9: ^python@:3.8")
        depends_on("py-lightning-utilities@0.8:", when="@1.1:")
        depends_on("py-lightning-utilities@0.7:", when="@1:")

        depends_on("py-scipy@1.0.1:", when="+image")
        depends_on("py-torchvision@0.8:", when="+image")
        depends_on("py-torch-fidelity", when="+image")
        depends_on("py-lpips", when="@:1.2.0+image")

        # Historical dependencies
        depends_on("py-pretty-errors@1.2.25", when="@1.4.0")
        depends_on("py-pydeprecate@0.3", when="@0.7:0.8")
