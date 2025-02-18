# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class HpcBeeflow(PythonPackage):
    """BEE is a workflow orchestration system designed to build containerized
    HPC applications and orchestrate workflows across HPC and cloud systems.
    BEE has adopted the Common Workflow Language (CWL) for specifying workflows.
    Complex scientific workflows specified by CWL are managed and visualized
    through a graph database, giving the user the ability to monitor the state
    of each task in the workflow. BEE runs jobs using the workload scheduler
    (i.e. Slurm or Flux) on the HPC system that tasks are
    specified to run on."""

    homepage = "https://github.com/lanl/bee"
    pypi = "hpc_beeflow/hpc_beeflow-0.1.9.tar.gz"

    # maintainers("pagrubel")

    license("MIT")

    version("0.1.9", sha256="196eb9155a5ca6e35d0cc514e0609cf352fc757088707306653496b83a311ac1")

    depends_on("python@3.8.3:3.12.2", type=("build", "run"))
    depends_on("py-poetry@0.12:", type="build")

    depends_on("py-flask@2.0:", type=("build", "run"))
    depends_on("py-fastapi@0.109.2", type=("build", "run"))
    depends_on("py-uvicorn@0.27.1", type=("build", "run"))
    depends_on("py-neo4j@5:", type=("build", "run"))
    depends_on("py-pyyaml@6.0.1:", type=("build", "run"))
    depends_on("py-flask-restful@0.3.9", type=("build", "run"))
    depends_on("py-cwl-utils@0.16:", type=("build", "run"))
    depends_on("py-apscheduler@3.6.3:", type=("build", "run"))
    depends_on("py-jsonpickle@2.2.0:", type=("build", "run"))
    depends_on("py-requests@:2.28", type=("build", "run"))
    depends_on("py-requests-unixsocket@0.3.0:", type=("build", "run"))
    depends_on("py-python-daemon@2.3.1:", type=("build", "run"))
    depends_on("py-gunicorn@20.1.0:22", type=("build", "run"))
    depends_on("py-typer@0.5.0:", type=("build", "run"))
    depends_on("py-cffi@1.15.1:", type=("build", "run"))
    depends_on("py-celery+redis+sqlalchemy@5.3.4:", type=("build", "run"))
    depends_on("py-docutils@0.18.1", type=("build", "run"))
    depends_on("py-graphviz@0.20.3:", type=("build", "run"))
