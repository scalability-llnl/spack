# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class IntelGtpin(Package):
    """Intel(R) GtPin is a dynamic binary instrumentation framework for GEN
    (Intel(R) graphics) Architecture. It is a unique SW platform for
    profiling a code running on GEN Execution Units (EUs). GTPin
    includes a binary instrumentation engine for Intel(R) GPUs EUs, along
    with an API for developing analysis tools, and many sample
    tools. GTPin allows you to capture a range of dynamic profiling
    data at the finest granularity of the specific GPU EU instruction.
    GTPin supports both compute and graphics workloads. It operates on
    regular, real-world GPU applications, as well as on pre-captured
    API streams. The technology enables fast and accurate dynamic
    analysis of the code that is executing on the GPU EUs. GTPin opens
    up new opportunities to perform dynamic, low level workload and HW
    analysis on an Intel(R) GPU, with greater efficiency than other
    current solutions. Some of the GTPin capabilities are integrated
    into Intel(R) VTune(TM) Profiler, Intel(R) Advisor, and the Intel(R)
    Graphics Performance Analyzers (Intel(R) GPA).

    GTPin is available, along with a set of analysis tools based on
    the GTPin framework. It also enables more advanced users to
    develop their own analysis tools. GTPin can analyze any GPU
    application. It also collects dynamic profiling data which the
    application executes on the GPU.
    """

    homepage = "https://www.intel.com/content/www/us/en/developer/articles/tool/gtpin.html"
    url = "https://downloadmirror.intel.com/762747/external-release-gtpin-3.2.2-linux.tar.xz"

    maintainers("rashawnlk")

    license("MIT")

    version(
        "4.0",
        sha256="fc12fb3aefdd4ae75b21ef9325e4058439dace52501200900895240c6ef3f0d8",
        url="https://downloadmirror.intel.com/816037/external-release-gtpin-4.0-linux.tar.xz",
    )

    version(
        "3.7",
        sha256="366edb46369a67bdbaea3c11ad5bf9a9ead5a7234efb780a27dffd70d1150c39",
        url="https://downloadmirror.intel.com/793592/external-release-gtpin-3.7-linux.tar.xz",
    )

    version(
        "3.4",
        sha256="c96d08a2729c255e3bc67372fc1271ba60ca8d7bd913f92c2bd951d7d348f553",
        url="https://downloadmirror.intel.com/777295/external-release-gtpin-3.4-linux.tar.xz",
    )

    version(
        "3.2.2",
        sha256="6c51b08451935ed8c86778d197e2ff36d4b91883f41292968ff413b53ac8910a",
        url="https://downloadmirror.intel.com/762747/external-release-gtpin-3.2.2-linux.tar.xz",
    )

    version(
        "3.0",
        sha256="8a8a238ab9937d85e4cc5a5c15a79cad0e4aa306b57e5d72dad3e09230a4cdab",
        url="https://downloadmirror.intel.com/730598/external-release-gtpin-3.0-linux.tar.xz",
    )

    version(
        "2.19",
        sha256="996cdfbcf7fbe736407d063e0ed1794e51bf31a72b50cf733a407af71118a304",
        url="https://downloadmirror.intel.com/686383/external-gtpin-2.19-linux.tar.xz",
    )

    version(
        "2.13",
        sha256="d715a55074147b73d51583bf684660b40f871e38e29af2bfc14dfe070fcbbada",
        url="https://downloadmirror.intel.com/682776/external-gtpin-2.13-linux.tar.bz2",
    )
    version(
        "2.12",
        sha256="432f1365bf4b3ff5847bb1059fb468ce6c7237ccd1489fbe8005f48e5a11e218",
        url="https://downloadmirror.intel.com/682777/external-gtpin-2.12-linux.tar.bz2",
    )
    version(
        "2.11.4",
        sha256="57f4d3aa67e8b7eb8a2456a4a770e60af770c599180cb2b6c3c8addd37311093",
        url="https://downloadmirror.intel.com/682779/external-gtpin-2.11.4-linux.tar.bz2",
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("patchelf", type="build")

    # Gtpin only runs on linux x86_64.
    conflicts("platform=darwin", msg="intel-gtpin only runs on linux")
    conflicts("target=ppc64:", msg="intel-gtpin only runs on x86_64")
    conflicts("target=ppc64le:", msg="intel-gtpin only runs on x86_64")
    conflicts("target=aarch64:", msg="intel-gtpin only runs on x86_64")

    # The gtbin tar file installs into Bin, Include, Lib directories.
    @property
    def command(self):
        return Executable(self.prefix.Bin.gtpin)

    @property
    def headers(self):
        return find_headers("gtpin", self.prefix.Include)

    @property
    def libs(self):
        return find_libraries("libgtpin", self.prefix.Lib, recursive=True)

    # The gtpin binary uses libraries from its own Lib directory but
    # doesn't set rpath.
    def install(self, spec, prefix):
        patchelf = spec["patchelf"].command
        patchelf(
            "--set-rpath", join_path("$ORIGIN", "..", "Lib", "intel64"), join_path("Bin", "gtpin")
        )

        install_tree(".", prefix)
