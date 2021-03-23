.. Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
   Spack Project Developers. See the top-level COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. _containers:

================
Container Images
================

Spack :ref:`environments` are a great tool to create container images, but
preparing one that is suitable for production requires some more boilerplate
than just:

.. code-block:: docker

   COPY spack.yaml /environment
   RUN spack -e /environment install

Additional actions may be needed to minimize the size of the
container, or to update the system software that is installed in the base
image, or to set up a proper entrypoint to run the image. These tasks are
usually both necessary and repetitive, so Spack comes with a command
to generate recipes for container images starting from a ``spack.yaml``.

--------------------
A Quick Introduction
--------------------

Consider having a Spack environment like the following:

.. code-block:: yaml

   spack:
     specs:
     - gromacs+mpi
     - mpich

Producing a ``Dockerfile`` from it is as simple as moving to the directory
where the ``spack.yaml`` file is stored and giving the following command:

.. code-block:: console

   $ spack containerize > Dockerfile

The ``Dockerfile`` that gets created uses multi-stage builds and
other techniques to minimize the size of the final image:

.. code-block:: docker

   # Build stage with Spack pre-installed and ready to be used
   FROM spack/ubuntu-bionic:latest as builder

   # What we want to install and how we want to install it
   # is specified in a manifest file (spack.yaml)
   RUN mkdir /opt/spack-environment \
   &&  (echo "spack:" \
   &&   echo "  specs:" \
   &&   echo "  - gromacs+mpi" \
   &&   echo "  - mpich" \
   &&   echo "  concretization: together" \
   &&   echo "  config:" \
   &&   echo "    install_tree: /opt/software" \
   &&   echo "  view: /opt/view") > /opt/spack-environment/spack.yaml

   # Install the software, remove unnecessary deps
   RUN cd /opt/spack-environment && spack env activate . && spack install --fail-fast && spack gc -y

   # Strip all the binaries
   RUN find -L /opt/view/* -type f -exec readlink -f '{}' \; | \
       xargs file -i | \
       grep 'charset=binary' | \
       grep 'x-executable\|x-archive\|x-sharedlib' | \
       awk -F: '{print $1}' | xargs strip -s

   # Modifications to the environment that are necessary to run
   RUN cd /opt/spack-environment && \
       spack env activate --sh -d . >> /etc/profile.d/z10_spack_environment.sh

   # Bare OS image to run the installed executables
   FROM ubuntu:18.04

   COPY --from=builder /opt/spack-environment /opt/spack-environment
   COPY --from=builder /opt/software /opt/software
   COPY --from=builder /opt/view /opt/view
   COPY --from=builder /etc/profile.d/z10_spack_environment.sh /etc/profile.d/z10_spack_environment.sh

   ENTRYPOINT ["/bin/bash", "--rcfile", "/etc/profile", "-l"]

The image itself can then be built and run in the usual way, with any of the
tools suitable for the task. For instance, if we decided to use ``docker``:

.. code-block:: bash

   $ spack containerize > Dockerfile
   $ docker build -t myimage .
   [ ... ]
   $ docker run -it myimage

The various components involved in the generation of the recipe and their
configuration are discussed in details in the sections below.

.. _container_spack_images:

--------------------------
Spack Images on Docker Hub
--------------------------

Docker images with Spack preinstalled and ready to be used are
built on `Docker Hub <https://hub.docker.com/u/spack>`_
at every push to ``develop`` or to a release branch. The OS that
are currently supported are summarized in the table below:

.. _containers-supported-os:

.. list-table:: Supported operating systems
   :header-rows: 1

   * - Operating System
     - Base Image
     - Spack Image
   * - Ubuntu 16.04
     - ``ubuntu:16.04``
     - ``spack/ubuntu-xenial``
   * - Ubuntu 18.04
     - ``ubuntu:18.04``
     - ``spack/ubuntu-bionic``
   * - CentOS 6
     - ``centos:6``
     - ``spack/centos6``
   * - CentOS 7
     - ``centos:7``
     - ``spack/centos7``

All the images are tagged with the corresponding release of Spack:

.. image:: dockerhub_spack.png

with the exception of the ``latest`` tag that points to the HEAD
of the ``develop`` branch. These images are available for anyone
to use and take care of all the repetitive tasks that are necessary
to setup Spack within a container. The container recipes generated
by Spack use them as default base images for their ``build`` stage,
even though handles to use custom base images provided by users are
available to accommodate complex use cases.

---------------------------------
Creating Images From Environments
---------------------------------

Any Spack Environment can be used for the automatic generation of container
recipes. Sensible defaults are provided for things like the base image or the
version of Spack used in the image.
If a finer tuning is needed it can be obtained by adding the relevant metadata
under the ``container`` attribute of environments:

.. code-block:: yaml

   spack:
     specs:
     - gromacs+mpi
     - mpich

     container:
       # Select the format of the recipe e.g. docker,
       # singularity or anything else that is currently supported
       format: docker

       # Sets the base images for the stages where Spack builds the
       # software or where the software gets installed after being built..
       images:
         os: "centos:7"
         spack: develop

       # Whether or not to strip binaries
       strip: true

       # Additional system packages that are needed at runtime
       os_packages:
         final:
         - libgomp

       # Extra instructions
       extra_instructions:
         final: |
           RUN echo 'export PS1="\[$(tput bold)\]\[$(tput setaf 1)\][gromacs]\[$(tput setaf 2)\]\u\[$(tput sgr0)\]:\w $ "' >> ~/.bashrc

       # Labels for the image
       labels:
         app: "gromacs"
         mpi: "mpich"

A detailed description of the options available can be found in the
:ref:`container_config_options` section.

-------------------
Setting Base Images
-------------------

The ``images`` subsection is used to select both the image where
Spack builds the software and the image where the built software
is installed. This attribute can be set in two different ways and
which one to use depends on the use case at hand.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Use Official Spack Images From Dockerhub
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To generate a recipe that uses an official Docker image from the
Spack organization to build the software and the corresponding official OS image
to install the built software, all the user has to do is specify:

1. An operating system under ``images:os``
2. A Spack version under ``images:spack``

Any combination of these two values that can be mapped to one of the images
discussed in :ref:`container_spack_images` is allowed. For instance, the
following ``spack.yaml``:

.. code-block:: yaml

   spack:
     specs:
     - gromacs+mpi
     - mpich

     container:
       images:
         os: centos:7
         spack: 0.15.4

uses ``spack/centos7:0.15.4``  and ``centos:7`` for the stages where the
software is respectively built and installed:

.. code-block:: docker

   # Build stage with Spack pre-installed and ready to be used
   FROM spack/centos7:0.15.4 as builder

   # What we want to install and how we want to install it
   # is specified in a manifest file (spack.yaml)
   RUN mkdir /opt/spack-environment \
   &&  (echo "spack:" \
   &&   echo "  specs:" \
   &&   echo "  - gromacs+mpi" \
   &&   echo "  - mpich" \
   &&   echo "  concretization: together" \
   &&   echo "  config:" \
   &&   echo "    install_tree: /opt/software" \
   &&   echo "  view: /opt/view") > /opt/spack-environment/spack.yaml
   [ ... ]
   # Bare OS image to run the installed executables
   FROM centos:7

   COPY --from=builder /opt/spack-environment /opt/spack-environment
   COPY --from=builder /opt/software /opt/software
   COPY --from=builder /opt/view /opt/view
   COPY --from=builder /etc/profile.d/z10_spack_environment.sh /etc/profile.d/z10_spack_environment.sh

   ENTRYPOINT ["/bin/bash", "--rcfile", "/etc/profile", "-l"]

This method of selecting base images is the simplest of the two, and we advise
to use it whenever possible. There are cases though where using Spack official
images is not enough to fit production needs. In these situations users can manually
select which base image to start from in the recipe, as we'll see next.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Use Custom Images Provided by Users
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Consider, as an example, building a production grade image for a CUDA
application. The best strategy would probably be to build on top of
images provided by the vendor and regard CUDA as an external package.

Spack doesn't currently provide an official image with CUDA configured
this way, but users can build it on their own and then configure the
environment to explicitly pull it. This requires users to:

1. Specify the image used to build the software under ``images:build``
2. Specify the image used to install the built software under ``images:final``

A ``spack.yaml`` like the following:

.. code-block:: yaml

   spack:
     specs:
     - gromacs@2019.4+cuda build_type=Release
     - mpich
     - fftw precision=float
     packages:
       cuda:
         buildable: False
         externals:
         - spec: cuda%gcc
           prefix: /usr/local/cuda

     container:
       images:
         build: custom/cuda-10.1-ubuntu18.04:latest
         final: nvidia/cuda:10.1-base-ubuntu18.04

produces, for instance, the following ``Dockerfile``:

.. code-block:: docker

   # Build stage with Spack pre-installed and ready to be used
   FROM custom/cuda-10.1-ubuntu18.04:latest as builder

   # What we want to install and how we want to install it
   # is specified in a manifest file (spack.yaml)
   RUN mkdir /opt/spack-environment \
   &&  (echo "spack:" \
   &&   echo "  specs:" \
   &&   echo "  - gromacs@2019.4+cuda build_type=Release" \
   &&   echo "  - mpich" \
   &&   echo "  - fftw precision=float" \
   &&   echo "  packages:" \
   &&   echo "    cuda:" \
   &&   echo "      buildable: false" \
   &&   echo "      externals:" \
   &&   echo "      - spec: cuda%gcc" \
   &&   echo "        prefix: /usr/local/cuda" \
   &&   echo "  concretization: together" \
   &&   echo "  config:" \
   &&   echo "    install_tree: /opt/software" \
   &&   echo "  view: /opt/view") > /opt/spack-environment/spack.yaml

   # Install the software, remove unnecessary deps
   RUN cd /opt/spack-environment && spack env activate . && spack install --fail-fast && spack gc -y

   # Strip all the binaries
   RUN find -L /opt/view/* -type f -exec readlink -f '{}' \; | \
       xargs file -i | \
       grep 'charset=binary' | \
       grep 'x-executable\|x-archive\|x-sharedlib' | \
       awk -F: '{print $1}' | xargs strip -s

   # Modifications to the environment that are necessary to run
   RUN cd /opt/spack-environment && \
       spack env activate --sh -d . >> /etc/profile.d/z10_spack_environment.sh

   # Bare OS image to run the installed executables
   FROM nvidia/cuda:10.1-base-ubuntu18.04

   COPY --from=builder /opt/spack-environment /opt/spack-environment
   COPY --from=builder /opt/software /opt/software
   COPY --from=builder /opt/view /opt/view
   COPY --from=builder /etc/profile.d/z10_spack_environment.sh /etc/profile.d/z10_spack_environment.sh

   ENTRYPOINT ["/bin/bash", "--rcfile", "/etc/profile", "-l"]

where the base images for both stages are completely custom.

This second mode of selection for base images is more flexible than just
choosing an operating system and a Spack version, but is also more demanding.
Users may need to generate by themselves their base images and it's also their
responsibility to ensure that:

1. Spack is available in the ``build`` stage and set up correctly to install the required software
2. The artifacts produced in the ``build`` stage can be executed in the ``final`` stage

Therefore we don't recommend its use in cases that can be otherwise
covered by the simplified mode shown first.

----------------------------
Singularity Definition Files
----------------------------

In addition to producing recipes in ``Dockerfile`` format Spack can produce
Singularity Definition Files by just changing the value of the ``format``
attribute:

.. code-block:: console

   $ cat spack.yaml
   spack:
     specs:
     - hdf5~mpi
     container:
       format: singularity

   $ spack containerize > hdf5.def
   $ sudo singularity build hdf5.sif hdf5.def

The minimum version of Singularity required to build a SIF (Singularity Image Format)
image from the recipes generated by Spack is ``3.5.3``.

.. _container_config_options:

-----------------------
Configuration Reference
-----------------------

The tables below describe all the configuration options that are currently supported
to customize the generation of container recipes:

.. list-table:: General configuration options for the ``container`` section of ``spack.yaml``
   :header-rows: 1

   * - Option Name
     - Description
     - Allowed Values
     - Required
   * - ``format``
     - The format of the recipe
     - ``docker`` or ``singularity``
     - Yes
   * - ``images:os``
     - Operating system used as a base for the image
     - See :ref:`containers-supported-os`
     - Yes, if using constrained selection of base images
   * - ``images:spack``
     - Version of Spack use in the ``build`` stage
     - Valid tags for ``base:image``
     - Yes, if using constrained selection of base images
   * - ``images:build``
     - Image to be used in the ``build`` stage
     - Any valid container image
     - Yes, if using custom selection of base images
   * - ``images:final``
     - Image to be used in the ``build`` stage
     - Any valid container image
     - Yes, if using custom selection of base images
   * - ``strip``
     - Whether to strip binaries
     - ``true`` (default) or ``false``
     - No
   * - ``os_packages:command``
     - Tool used to manage system packages
     - ``apt``, ``yum``
     - Only with custom base images
   * - ``os_packages:update``
     - Whether or not to update the list of available packages
     - True or False (default: True)
     - No
   * - ``os_packages:build``
     - System packages needed at build-time
     - Valid packages for the current OS
     - No
   * - ``os_packages:final``
     - System packages needed at run-time
     - Valid packages for the current OS
     - No
   * - ``extra_instructions:build``
     - Extra instructions (e.g. `RUN`, `COPY`, etc.) at the end of the ``build`` stage
     - Anything understood by the current ``format``
     - No
   * - ``extra_instructions:final``
     - Extra instructions (e.g. `RUN`, `COPY`, etc.) at the end of the ``final`` stage
     - Anything understood by the current ``format``
     - No
   * - ``labels``
     - Labels to tag the image
     - Pairs of key-value strings
     - No

.. list-table:: Configuration options specific to Singularity
   :header-rows: 1

   * - Option Name
     - Description
     - Allowed Values
     - Required
   * - ``singularity:runscript``
     - Content of ``%runscript``
     - Any valid script
     - No
   * - ``singularity:startscript``
     - Content of ``%startscript``
     - Any valid script
     - No
   * - ``singularity:test``
     - Content of ``%test``
     - Any valid script
     - No
   * - ``singularity:help``
     - Description of the image
     - Description string
     - No

--------------
Best Practices
--------------

^^^
MPI
^^^
Due to the dependency on Fortran for OpenMPI, which is the spack default
implementation, consider adding ``gfortran`` to the ``apt-get install`` list.

Recent versions of OpenMPI will require you to pass ``--allow-run-as-root``
to your ``mpirun`` calls if started as root user inside Docker.

For execution on HPC clusters, it can be helpful to import the docker
image into Singularity in order to start a program with an *external*
MPI. Otherwise, also add ``openssh-server`` to the ``apt-get install`` list.

^^^^
CUDA
^^^^
Starting from CUDA 9.0, Nvidia provides minimal CUDA images based on
Ubuntu. Please see `their instructions <https://hub.docker.com/r/nvidia/cuda/>`_.
Avoid double-installing CUDA by adding, e.g.

.. code-block:: yaml

   packages:
     cuda:
       externals:
       - spec: "cuda@9.0.176%gcc@5.4.0 arch=linux-ubuntu16-x86_64"
         prefix: /usr/local/cuda
       buildable: False

to your ``spack.yaml``.

Users will either need ``nvidia-docker`` or e.g. Singularity to *execute*
device kernels.

^^^^^^^^^^^^^^^^^^^^^^^^^
Docker on Windows and OSX
^^^^^^^^^^^^^^^^^^^^^^^^^

On Mac OS and Windows, docker runs on a hypervisor that is not allocated much
memory by default, and some spack packages may fail to build due to lack of
memory. To work around this issue, consider configuring your docker installation
to use more of your host memory. In some cases, you can also ease the memory
pressure on parallel builds by limiting the parallelism in your config.yaml.

.. code-block:: yaml

   config:
     build_jobs: 2

