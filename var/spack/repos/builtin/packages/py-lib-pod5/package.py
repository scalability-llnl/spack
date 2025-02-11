# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import platform
import sys

from spack.package import *

arch, os = platform.machine(), sys.platform
arch64_32, _ = platform.architecture()


class PyLibPod5(PythonPackage):
    """
    POD5 is a file format for storing nanopore dna data in an easily accessible way.
    The format is able to be written in a streaming manner which allows a sequencing
    instrument to directly write the format.
    """

    homepage = "https://github.com/nanoporetech/pod5-file-format"
    url = "https://files.pythonhosted.org/packages/bd/67/c1720a8e2ccd4442f49320dc238aa5ad5d92266f0aec21e50f5f42d392a6/lib_pod5-0.3.10-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl"

    maintainers("Pandapip1")

    license("MPL-2.0", checked_by="Pandapip1")

    if (arch == "x86_64" or arch == "x64") and os == "linux":  # Linux on x86_64
        version(
            "0.3.10-python312",
            sha256="6a340e412555855a19b6ffe46409e544e269e89bb4018cd5e0deef2521daddb8",
            url="https://files.pythonhosted.org/packages/bd/67/c1720a8e2ccd4442f49320dc238aa5ad5d92266f0aec21e50f5f42d392a6/lib_pod5-0.3.10-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl",
            expand=False,
        )
        version(
            "0.3.10-python311",
            sha256="d331a9d68dfca9f49674bbdadd7fb98d7d98b422633e8e082d511e046f195bca",
            url="https://files.pythonhosted.org/packages/16/1b/bfe58e07a4ca6de8f783e97cbf7999c54d9989e6ec389be81a91be258a17/lib_pod5-0.3.10-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl",
            expand=False,
        )
        version(
            "0.3.10-python310",
            sha256="b891f175dbc0665be3041e799fe13f32569d706f5f3f8c0d0e7394b40fd41cf6",
            url="https://files.pythonhosted.org/packages/d6/89/cdbab5b237e94b9b5a3cae79f1749cfc9118392ee3b4f3ae9382b91bf53d/lib_pod5-0.3.10-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl",
            expand=False,
        )
        version(
            "0.3.10-python39",
            sha256="40d7f60571e023071024e42a9c69cd9957e10a50f310e42b244a97d438a1613a",
            url="https://files.pythonhosted.org/packages/d4/61/7772d1a07a7fae5cda35863e5b3660369dfab9a838ee43d860afe0dfa429/lib_pod5-0.3.10-cp39-cp39-manylinux_2_17_x86_64.manylinux2014_x86_64.whl",
            expand=False,
        )
        version(
            "0.3.10-python38",
            sha256="f19ebc08bf8a9416a03d465599cec4d29fdcc50c9ae1dcf5d3954a711fef3add",
            url="https://files.pythonhosted.org/packages/91/82/ed0d18fea1267ae22b4de22f64bdb48e965686c2ab2d0cab1b7a90cd166a/lib_pod5-0.3.10-cp38-cp38-manylinux_2_17_x86_64.manylinux2014_x86_64.whl",
            expand=False,
        )
    elif arch == "aarch64" and os == "linux":  # Linux on 64-bit ARM
        version(
            "0.3.10-python312",
            sha256="341d27c5d70bfc132906bd8e5231f5bfd0b3963c8025c91e407fceb28c84186c",
            url="https://files.pythonhosted.org/packages/c5/8b/4ea175749178fa76fd23fbb96d69279bcbcdbaf1c7db0e8d5bbcd44fc422/lib_pod5-0.3.10-cp312-cp312-manylinux_2_17_aarch64.manylinux2014_aarch64.whl",
            expand=False,
        )
        version(
            "0.3.10-python311",
            sha256="7f9c61416bb5e508ffb818d38aad2e3080d1f0dc52b03151be2d6480fade41a2",
            url="https://files.pythonhosted.org/packages/dd/b5/5a2e9c24bbb73d74a1f4a911fdefa8a287c0648db735b85dfcccc721fa08/lib_pod5-0.3.10-cp311-cp311-manylinux_2_17_aarch64.manylinux2014_aarch64.whl",
            expand=False,
        )
        version(
            "0.3.10-python310",
            sha256="e604563666806d6a93f5f92b9ac437fe6cc15716046c98b794baf34e5ab3f14b",
            url="https://files.pythonhosted.org/packages/4d/5c/3fc42f448d156c3ca5dd42db468da76f5ef44c501d91e2ab0caef17f6d87/lib_pod5-0.3.10-cp310-cp310-manylinux_2_17_aarch64.manylinux2014_aarch64.whl",
            expand=False,
        )
        version(
            "0.3.10-python39",
            sha256="ab79809b42026b7a50cb16cac1a976f83619ed1ac476943d421e66d8181d80df",
            url="https://files.pythonhosted.org/packages/fe/d8/0f3f050b21ef8c2243ff813f826a8cde5bb6b01a9dfaa655728367f52a29/lib_pod5-0.3.10-cp39-cp39-manylinux_2_17_aarch64.manylinux2014_aarch64.whl",
            expand=False,
        )
        version(
            "0.3.10-python38",
            sha256="bcd8cfc9a6fc23b7501da5a72561b54d4fa51f1283addb9fcbfc86cb42a93b0c",
            url="https://files.pythonhosted.org/packages/13/fb/a27a0adcb6bfc8273e9761610c35086184267fec9d872762f250ba48948f/lib_pod5-0.3.10-cp38-cp38-manylinux_2_17_aarch64.manylinux2014_aarch64.whl",
            expand=False,
        )
    elif (arch == "x86_64" or arch == "x64") and os == "darwin":  # MacOS on x86_64
        version(
            "0.3.10-python312",
            sha256="36034e1ffdf35c91e7a4c3c2db878463286417d53ccae0407805f89c6b02f0a9",
            url="https://files.pythonhosted.org/packages/8a/81/5164a27abafa9db0c725848e7c9a112010e53c5018ef88551bcfc8a0a914/lib_pod5-0.3.10-cp312-cp312-macosx_10_15_universal2.whl",
            expand=False,
        )
        version(
            "0.3.10-python311",
            sha256="6d91ac60e9d7b1e47f390f1cf7d49364d3fb26eb35e6983ed9a398678437295c",
            url="https://files.pythonhosted.org/packages/ba/1c/a984e9bdac5db1e758c2d2e32659c85edf925d588454823ba902a828bb75/lib_pod5-0.3.10-cp311-cp311-macosx_10_15_universal2.whl",
            expand=False,
        )
        version(
            "0.3.10-python310",
            sha256="c20c5f4e79ca624068a9e11281261d94623a732cfd279fa4928b0d677992d9d6",
            url="https://files.pythonhosted.org/packages/77/db/aa884faec2a2d915e18bebbdcadeec673634e3d5e06bcec5a1cf35547a10/lib_pod5-0.3.10-cp310-cp310-macosx_10_15_universal2.whl",
            expand=False,
        )
        version(
            "0.3.10-python39",
            sha256="5c8cd7128e5012c7d59ca8a795aa227e9e783a384a4e25c332a674403ff671f0",
            url="https://files.pythonhosted.org/packages/31/06/f3d40dd210a1518aff3147c1cb530a45223ee7142c227d5c278f28c7f098/lib_pod5-0.3.10-cp39-cp39-macosx_10_15_x86_64.whl",
            expand=False,
        )
        version(
            "0.3.10-python38",
            sha256="e8f29a5c1ebc4a938b0fd1cfc5acb525dba12acc2bb9486a218f1da34162ca12",
            url="https://files.pythonhosted.org/packages/16/9b/28af9eee8df352c60df35332f350d4e371b244afc02d7e605397ddaa1a00/lib_pod5-0.3.10-cp38-cp38-macosx_10_15_x86_64.whl",
            expand=False,
        )
    elif not (arch == "x86_64" or arch == "x64") and os == "darwin":  # MacOS on Apple Silicon
        version(
            "0.3.10-python312",
            sha256="438005f335b5ddf7f43a2802e7db2e59e4fe3ec3934bc664a0b53a850e159b3c",
            url="https://files.pythonhosted.org/packages/c5/a1/e14ac73d099db809b26baff8db0e2dc01e61f13a4d60a516a26affbd3558/lib_pod5-0.3.10-cp312-cp312-macosx_11_0_arm64.whl",
            expand=False,
        )
        version(
            "0.3.10-python311",
            sha256="fc46db53664bab41baa92e208075cacda12009aead554524f041d49da19556fe",
            url="https://files.pythonhosted.org/packages/05/28/ccdcd8ffbca3836952c49240826cefe36d79feb348eca99fedba10925a68/lib_pod5-0.3.10-cp311-cp311-macosx_11_0_arm64.whl",
            expand=False,
        )
        version(
            "0.3.10-python310",
            sha256="a6aa6e804da1cdf5ea16034f3a9e4a529abfc783739978bd04ffe494e1b37c05",
            url="https://files.pythonhosted.org/packages/86/30/0f518874de35f2e0a760f8e27ef1e78e89054e5f29c78eb2f8b2e0f1cb8d/lib_pod5-0.3.10-cp310-cp310-macosx_11_0_arm64.whl",
            expand=False,
        )
        version(
            "0.3.10-python39",
            sha256="0a18239a4f1934f80bfad75c6411bc6f349294183e442f92adfde2741436a753",
            url="https://files.pythonhosted.org/packages/c8/64/926a61d32c5cc6e68587c0e91674c258dd155ed806619b68dc8761370455/lib_pod5-0.3.10-cp39-cp39-macosx_11_0_arm64.whl",
            expand=False,
        )
        version(
            "0.3.10-python38",
            sha256="2bef87104d3ff65ec93d724994d6ed1654a28edc720275732f7369ac449005ec",
            url="https://files.pythonhosted.org/packages/f4/03/92fe4ca1cbabefca07d1ab12c85e5134d1c4ed609dc0df6c766f128b2db5/lib_pod5-0.3.10-cp38-cp38-macosx_11_0_arm64.whl",
            expand=False,
        )
    elif arch64_32 == "64bit" and os == "win32":  # 64-bit windows
        version(
            "0.3.10-python312",
            sha256="38950890a4555a2b5bb63323090fd0bb4333a536c819d867734f2fe1ff8ce0eb",
            url="https://files.pythonhosted.org/packages/0c/d1/e8ae7856e7749a57cce33830326dafd41df99756c627e97c18c10ff2a378/lib_pod5-0.3.10-cp312-cp312-win_amd64.whl",
            expand=False,
        )
        version(
            "0.3.10-python311",
            sha256="6d91ac60e9d7b1e47f390f1cf7d49364d3fb26eb35e6983ed9a398678437295c",
            url="https://files.pythonhosted.org/packages/96/bc/203f2ff4b0c56e9a883c7d89549a6a978614433d8a59d4dd60a5986f68d3/lib_pod5-0.3.10-cp311-cp311-win_amd64.whl",
            expand=False,
        )
        version(
            "0.3.10-python310",
            sha256="e6a68cc16e0e984f66b73d18c01755a69df2695fd4997c2aad368d3c9fa2491a",
            url="https://files.pythonhosted.org/packages/c3/93/b2642947eb5758bb366fb69a0c295d0262b371f010908fcf49e478e3b376/lib_pod5-0.3.10-cp310-cp310-win_amd64.whl",
            expand=False,
        )
        version(
            "0.3.10-python39",
            sha256="8c6393e98c654933d017b401c39956c4cd7c14df3f02c1bd59528a7f07229168",
            url="https://files.pythonhosted.org/packages/97/d0/3f5e5c66d3ccf59c3f7fd78c04a623b39435db34e24e498cfe73f5ae6014/lib_pod5-0.3.10-cp39-cp39-win_amd64.whl",
            expand=False,
        )
        version(
            "0.3.10-python38",
            sha256="69a55903ef39c16272439facfb96c44cf60209f9b8742d3243ee6122cb86d235",
            url="https://files.pythonhosted.org/packages/4a/ea/d84aa5a3586ce8667e50482f81cc5b07a9734dc837799cfd48168e6cebd5/lib_pod5-0.3.10-cp38-cp38-win_amd64.whl",
            expand=False,
        )

    depends_on("python@3.12", type=("build", "run"), when="@0.3.10-python312")
    depends_on("python@3.11", type=("build", "run"), when="@0.3.10-python311")
    depends_on("python@3.10", type=("build", "run"), when="@0.3.10-python310")
    depends_on("python@3.9", type=("build", "run"), when="@0.3.10-python39")
    depends_on("python@3.8", type=("build", "run"), when="@0.3.10-python38")
    depends_on("py-setuptools", type="build")
    depends_on("py-numpy@1.21.0:", type=("build", "run"))
