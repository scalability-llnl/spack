# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGoogleCloudStorage(PythonPackage):
    """Google Cloud Storage API client library."""

    homepage = "https://github.com/googleapis/python-storage"
    pypi = "google-cloud-storage/google-cloud-storage-2.14.0.tar.gz"

    license("Apache-2.0")

    version("2.14.0", sha256="2d23fcf59b55e7b45336729c148bb1c464468c69d5efbaee30f7201dd90eb97e")
    version("2.13.0", sha256="f62dc4c7b6cd4360d072e3deb28035fbdad491ac3d9b0b1815a12daea10f37c7")
    version("2.12.0", sha256="57c0bcda2f5e11f008a155d8636d8381d5abab46b58e0cae0e46dd5e595e6b46")
    version("2.11.0", sha256="6fbf62659b83c8f3a0a743af0d661d2046c97c3a5bfb587c4662c4bc68de3e31")
    version("2.10.0", sha256="934b31ead5f3994e5360f9ff5750982c5b6b11604dc072bc452c25965e076dc7")
    version("2.9.0", sha256="9b6ae7b509fc294bdacb84d0f3ea8e20e2c54a8b4bbe39c5707635fec214eff3")
    version("2.8.0", sha256="4388da1ff5bda6d729f26dbcaf1bfa020a2a52a7b91f0a8123edbda51660802c")
    version("2.7.0", sha256="1ac2d58d2d693cb1341ebc48659a3527be778d9e2d8989697a2746025928ff17")
    version("1.18.0", sha256="9fb3dc68948f4c893c2b16f5a3db3daea2d2f3b8e9d5c2d505fe1523758009b6")

    depends_on("py-setuptools", type="build")

    with when("@2:"):
        depends_on("py-google-auth@2.23.3:2", type=("build", "run"), when="@2.12:")
        depends_on("py-google-auth@1.25:2", type=("build", "run"))
        depends_on("py-google-api-core@1.31.5:1,2.3.1:2", type=("build", "run"))
        depends_on("py-google-cloud-core@2.3:2", type=("build", "run"))
        depends_on("py-google-resumable-media@2.6:", type=("build", "run"), when="@2.11:")
        depends_on("py-google-resumable-media@2.3.2:", type=("build", "run"))
        depends_on("py-requests@2.18:2", type=("build", "run"))
        depends_on("py-google-crc32c@1", type=("build", "run"), when="@2.12:")

    with when("@:1"):
        depends_on("py-google-auth@1.2.0:", type=("build", "run"))
        depends_on("py-google-cloud-core@1.0:1", type=("build", "run"))
        depends_on("py-google-resumable-media@0.3.1:", type=("build", "run"))
