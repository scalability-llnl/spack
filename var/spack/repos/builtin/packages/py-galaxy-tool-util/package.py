# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyGalaxyToolUtil(PythonPackage):
    """The Galaxy tool utilities."""

    homepage = "https://github.com/galaxyproject/galaxy"

    version(
        "22.1.5",
        url="https://files.pythonhosted.org/packages/76/b0/4745ccb75fdb5c48a27a73900f8430119afe6c7c95b1aafed004f093788c/galaxy_tool_util-22.1.5-py2.py3-none-any.whl",
        sha256="062a758024cda103d3d40ba232379c0c1853e8e181b58a65c4e954456cdcc040",
        expand=False,
    )

    depends_on("python@3.7:3.10", type=("build", "run"))
    depends_on("py-setuptools", type="build")

    depends_on("py-galaxy-util", type=("build", "run"))

    # depends_on("py-a2wsgi", type=("build", "run"))
    # depends_on("py-aiofiles", type=("build", "run"))
    # depends_on("py-alembic", type=("build", "run"))
    # depends_on("py-apispec", type=("build", "run"))
    # depends_on("py-babel", type=("build", "run"))
    # depends_on("py-bdbag@1.6.3:", type=("build", "run"))
    # depends_on("py-beaker@1.11.0", type=("build", "run"))
    # depends_on("py-bioblend", type=("build", "run"))
    # depends_on("py-bleach", type=("build", "run"))
    # depends_on("py-boltons", type=("build", "run"))
    # depends_on("py-boto", type=("build", "run"))
    # depends_on("py-bx-python", type=("build", "run"))
    # depends_on("py-celery", type=("build", "run"))
    # depends_on("py-cheetah3@:3.2.6.post1,3.2.7:", type=("build", "run"))
    # depends_on("py-cloudauthz@0.6.0", type=("build", "run"))
    # depends_on("py-cloudbridge", type=("build", "run"))
    # depends_on("py-circus", type=("build", "run"))
    # depends_on("py-cwltool@3.1.20221109155812", type=("build", "run"))
    # depends_on("py-dictobj", type=("build", "run"))
    # depends_on("py-dnspython", type=("build", "run"))
    # depends_on("py-docutils@:0.16,0.18:", type=("build", "run"))
    # depends_on("py-edam-ontology", type=("build", "run"))
    # depends_on("py-fastapi@0.71.0:", type=("build", "run"))
    # depends_on("py-fastapi-utils", type=("build", "run"))
    # depends_on("py-fs", type=("build", "run"))
    # depends_on("py-future", type=("build", "run"))
    # depends_on("py-galaxy-sequence-utils", type=("build", "run"))
    # depends_on("py-gravity@0.10.0:", type=("build", "run"))
    # depends_on("py-gunicorn", type=("build", "run"))
    # depends_on("py-gxformat2", type=("build", "run"))
    # depends_on("py-h5py", type=("build", "run"))
    # depends_on("py-importlib-resources", type=("build", "run"))
    # depends_on("py-isa-rwval", type=("build", "run"))
    # depends_on("py-kombu", type=("build", "run"))
    # depends_on("py-lagom", type=("build", "run"))
    # depends_on("py-mako", type=("build", "run"))
    # depends_on("py-markdown", type=("build", "run"))
    # depends_on("py-markupsafe", type=("build", "run"))
    # depends_on("mercurial", type=("build", "run"))
    # depends_on("py-mrcfile", type=("build", "run"))
    # depends_on("py-nodeenv", type=("build", "run"))
    # depends_on("py-numpy", type=("build", "run"))
    # depends_on("py-paramiko@:2.8.1,2.9.2:", type=("build", "run"))
    # depends_on("py-parsley", type=("build", "run"))
    # depends_on("py-paste", type=("build", "run"))
    # depends_on("py-pebble", type=("build", "run"))
    # depends_on("py-psutil", type=("build", "run"))
    # depends_on("py-pulsar-galaxy-lib@0.15.0.dev0:", type=("build", "run"))
    # depends_on("py-pycryptodome", type=("build", "run"))
    # depends_on("py-pydantic", type=("build", "run"))
    # depends_on("py-pyjwt", type=("build", "run"))
    # depends_on("py-pykwalify", type=("build", "run"))
    # depends_on("py-pylibmagic", type=("build", "run"))
    # depends_on("py-pyparsing", type=("build", "run"))
    # depends_on("py-pysam", type=("build", "run"))
    # depends_on("py-python-dateutil", type=("build", "run"))
    # depends_on("py-python-magic", type=("build", "run"))
    # depends_on("py-python-multipart", type=("build", "run"))
    # depends_on("py-pyyaml", type=("build", "run"))
    # depends_on("py-refgenconf@0.12.0:", type=("build", "run"))
    # depends_on("py-requests", type=("build", "run"))
    # depends_on("py-rocrate", type=("build", "run"))
    # depends_on("py-routes", type=("build", "run"))
    # depends_on("py-schema-salad@:8.3.20220717184004,8.3.20220801194920:", type=("build", "run"))
    # depends_on("py-social-auth-core@4.0.3", type=("build", "run"))
    # depends_on("py-sortedcontainers", type=("build", "run"))
    # depends_on("py-sqlalchemy@1.4.25:2", type=("build", "run"))
    # depends_on("py-sqlalchemy-migrate", type=("build", "run"))
    # depends_on("py-sqlitedict", type=("build", "run"))
    # depends_on("py-sqlparse", type=("build", "run"))
    # depends_on("py-starlette", type=("build", "run"))
    # depends_on("py-starlette-context", type=("build", "run"))
    # depends_on("py-svgwrite", type=("build", "run"))
    # depends_on("py-tifffile", type=("build", "run"))
    # depends_on("py-tuswsgi", type=("build", "run"))
    # depends_on("py-typing-extensions", type=("build", "run"))
    # depends_on("py-uvicorn", type=("build", "run"))
    # depends_on("py-uvloop", type=("build", "run"))
    # depends_on("py-webob", type=("build", "run"))
    # depends_on("py-whoosh", type=("build", "run"))
    # depends_on("py-zipstream-new", type=("build", "run"))
