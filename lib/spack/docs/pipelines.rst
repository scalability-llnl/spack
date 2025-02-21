.. Copyright Spack Project Developers. See COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. _pipelines:

============
CI Pipelines
============

Spack provides commands that support generating and running automated build pipelines in CI instances.  At the highest
level it works like this: provide a spack environment describing the set of packages you care about, and include a
description of how those packages should be mapped to Gitlab runners.  Spack can then generate a ``.gitlab-ci.yml``
file containing job descriptions for all your packages that can be run by a properly configured CI instance.  When
run, the generated pipeline will build and deploy binaries, and it can optionally report to a CDash instance
regarding the health of the builds as they evolve over time.

------------------------------
Getting started with pipelines
------------------------------

To get started with automated build pipelines a Gitlab instance with version ``>= 12.9``
(more about Gitlab CI `here <https://about.gitlab.com/product/continuous-integration/>`_)
with at least one `runner <https://docs.gitlab.com/runner/>`_ configured is required. This
can be done quickly by setting up a local Gitlab instance.

It is possible to set up pipelines on gitlab.com, but the builds there are limited to
60 minutes and generic hardware.  It is possible to
`hook up <https://about.gitlab.com/blog/2018/04/24/getting-started-gitlab-ci-gcp>`_
Gitlab to Google Kubernetes Engine (`GKE <https://cloud.google.com/kubernetes-engine/>`_)
or Amazon Elastic Kubernetes Service (`EKS <https://aws.amazon.com/eks>`_), though those
topics are outside the scope of this document.

After setting up a Gitlab instance for running CI, the basic steps for setting up a build pipeline are as follows:

#. Create a repository in the Gitlab instance with CI and a runner enabled.
#. Add a ``spack.yaml`` at the root containing your pipeline environment
#. Add a ``.gitlab-ci.yml`` at the root containing two jobs (one to generate
   the pipeline dynamically, and one to run the generated jobs).
#. Push a commit containing the ``spack.yaml`` and ``.gitlab-ci.yml`` mentioned above
   to the gitlab repository

See the :ref:`functional_example` section for a minimal working example.  See also
the :ref:`custom_Workflow` section for a link to an example of a custom workflow
based on spack pipelines.

Spack's pipelines are now making use of the
`trigger <https://docs.gitlab.com/ee/ci/yaml/#trigger>`_ syntax to run
dynamically generated
`child pipelines <https://docs.gitlab.com/ee/ci/pipelines/parent_child_pipelines.html>`_.
Note that the use of dynamic child pipelines requires running Gitlab version
``>= 12.9``.

.. _functional_example:

------------------
Functional Example
------------------

The simplest fully functional standalone example of a working pipeline can be
examined live at this example `project <https://gitlab.com/spack/pipeline-quickstart>`_
on gitlab.com.

Here's the ``.gitlab-ci.yml`` file from that example that builds and runs the
pipeline:

.. code-block:: yaml

   stages: [ "generate", "build" ]

   variables:
     SPACK_REPOSITORY: "https://github.com/spack/spack.git"
     SPACK_REF: "develop-2024-10-06"
     SPACK_USER_CONFIG_PATH: ${CI_PROJECT_DIR}
     SPACK_BACKTRACE: 1

   generate-pipeline:
     tags:
       - saas-linux-small-amd64
     stage: generate
     image:
       name: ghcr.io/spack/ubuntu20.04-runner-x86_64:2023-01-01
     script:
       - git clone ${SPACK_REPOSITORY}
       - cd spack && git checkout ${SPACK_REF} && cd ../
       - . "./spack/share/spack/setup-env.sh"
       - spack --version
       - spack env activate --without-view .
       - spack -d -v --color=always
         ci generate
         --check-index-only
         --artifacts-root "${CI_PROJECT_DIR}/jobs_scratch_dir"
         --output-file "${CI_PROJECT_DIR}/jobs_scratch_dir/cloud-ci-pipeline.yml"
     artifacts:
       paths:
         - "${CI_PROJECT_DIR}/jobs_scratch_dir"

   build-pipeline:
     stage: build
     trigger:
       include:
         - artifact: jobs_scratch_dir/cloud-ci-pipeline.yml
           job: generate-pipeline
       strategy: depend
     needs:
       - artifacts: True
         job: generate-pipeline


The key thing to note above is that there are two jobs: The first job to run,
``generate-pipeline``, runs the ``spack ci generate`` command to generate a
dynamic child pipeline and write it to a yaml file, which is then picked up
by the second job, ``build-jobs``, and used to trigger the downstream pipeline.

And here's the spack environment built by the pipeline represented as a
``spack.yaml`` file:

.. code-block:: yaml

   spack:
     view: false
     concretizer:
       unify: true
       reuse: false

     definitions:
     - pkgs:
       - zlib
       - bzip2 ~debug
     - compiler:
       - '%gcc'

     specs:
     - matrix:
       - - $pkgs
       - - $compiler

     ci:
       target: gitlab

       pipeline-gen:
       - any-job:
           tags:
             - saas-linux-small-amd64
           image:
             name: ghcr.io/spack/ubuntu20.04-runner-x86_64:2023-01-01
           before_script:
           - git clone ${SPACK_REPOSITORY}
           - cd spack && git checkout ${SPACK_REF} && cd ../
           - . "./spack/share/spack/setup-env.sh"
           - spack --version
           - export SPACK_USER_CONFIG_PATH=${CI_PROJECT_DIR}
           - spack config blame mirrors


.. note::
   The use of ``reuse: false`` in spack environments used for pipelines is
   almost always what you want, as without it your pipelines will not rebuild
   packages even if package hashes have changed. This is due to the concretizer
   strongly preferring known hashes when ``reuse: true``.

The ``ci`` section in the above environment file contains the bare minimum
configuration required for ``spack ci generate`` to create a working pipeline.
The ``target: gitlab`` tells spack that the desired pipeline output is for
gitlab.  However, this isn't strictly required, as currently gitlab is the
only possible output format for pipelines. The ``pipeline-gen`` section
contains the key information needed to specify attributes for the generated
jobs.  Notice that it contains a list which has only a single element in
this case.  In real pipelines it will almost certainly have more elements,
and in those cases, order is important: spack starts at the bottom of the
list and works upwards when applying attributes.

But in this simple case, we use only the special key ``any-job`` to
indicate that spack should apply the specified attributes (``tags``, ``image``,
and ``before_script``) to any job it generates.  This includes jobs for
building/pushing all packages, a ``rebuild-index`` job at the end of the
pipeline, as well as any ``noop`` jobs that might be needed by gitlab when
no rebuilds are required.

Something to note is that in this simple case, we rely on spack to
generate a reasonable script for the package build jobs (it just creates
a script that invokes ``spack ci rebuild``).

Another thing to note is the use of the ``SPACK_USER_CONFIG_DIR`` environment
variable in any generated jobs.  The purpose of this is to make spack
aware of one final file in the example, the one that contains the mirror
configuration.  This file, ``mirrors.yaml`` looks like this:

.. code-block:: yaml

   mirrors:
     buildcache-destination:
       url: oci://registry.gitlab.com/spack/pipeline-quickstart
       binary: true
       access_pair:
         id_variable: CI_REGISTRY_USER
         secret_variable: CI_REGISTRY_PASSWORD


Note the name of the mirror is ``buildcache-destination``, which is required
as of Spack 0.23 (see below for more information).  The mirror url simply
points to the container registry associated with the project, while
``id_variable`` and ``secret_variable`` refer to to environment variables
containing the access credentials for the mirror.

When spack builds packages for this example project, they will be pushed to
the project container registry, where they will be available for subsequent
jobs to install as dependencies, or for other pipelines to use to build runnable
container images.

-----------------------------------
Spack commands supporting pipelines
-----------------------------------

Spack provides a ``ci`` command with a few sub-commands supporting spack
ci pipelines.  These commands are covered in more detail in this section.

.. _cmd-spack-ci:

^^^^^^^^^^^^
``spack ci``
^^^^^^^^^^^^

Super-command for functionality related to generating pipelines and executing
pipeline jobs.

.. _cmd-spack-ci-generate:

^^^^^^^^^^^^^^^^^^^^^
``spack ci generate``
^^^^^^^^^^^^^^^^^^^^^

Throughout this documentation, references to the "mirror" mean the target
mirror which is checked for the presence of up-to-date specs, and where
any scheduled jobs should push built binary packages.  In the past, this
defaulted to the mirror at index 0 in the mirror configs, and could be
overridden using the ``--buildcache-destination`` argument. Starting with
Spack 0.23, ``spack ci generate`` will require you to identify this mirror
by the name "buildcache-destination".  While you can configure any number
of mirrors as sources for your pipelines, you will need to identify the
destination mirror by name.

Concretizes the specs in the active environment, stages them (as described in
:ref:`staging_algorithm`), and writes the resulting ``.gitlab-ci.yml`` to disk.
During concretization of the environment, ``spack ci generate`` also writes a
``spack.lock`` file which is then provided to generated child jobs and made
available in all generated job artifacts to aid in reproducing failed builds
in a local environment.  This means there are two artifacts that need to be
exported in your pipeline generation job (defined in your ``.gitlab-ci.yml``).
The first is the output yaml file of ``spack ci generate``, and the other is
the directory containing the concrete environment files.  In the
:ref:`functional_example` section, we only mentioned one path in the
``artifacts`` ``paths`` list because we used ``--artifacts-root`` as the
top level directory containing both the generated pipeline yaml and the
concrete environment.

Using ``--prune-dag`` or ``--no-prune-dag`` configures whether or not jobs are
generated for specs that are already up to date on the mirror.   If enabling
DAG pruning using ``--prune-dag``, more information may be required in your
``spack.yaml`` file, see the :ref:`noop_jobs` section below regarding
``noop-job``.

The optional ``--check-index-only`` argument can be used to speed up pipeline
generation by telling spack to consider only remote buildcache indices when
checking the remote mirror to determine if each spec in the DAG is up to date
or not.  The default behavior is for spack to fetch the index and check it,
but if the spec is not found in the index, to also perform a direct check for
the spec on the mirror.  If the remote buildcache index is out of date, which
can easily happen if it is not updated frequently, this behavior ensures that
spack has a way to know for certain about the status of any concrete spec on
the remote mirror, but can slow down pipeline generation significantly.

The optional ``--output-file`` argument should be an absolute path (including
file name) to the generated pipeline, and if not given, the default is
``./.gitlab-ci.yml``.

While optional, the ``--artifacts-root`` argument is used to determine where
the concretized environment directory should be located.  This directory will
be created by ``spack ci generate`` and will contain the ``spack.yaml`` and
generated ``spack.lock`` which are then passed to all child jobs as an
artifact.  This directory will also be the root directory for all artifacts
generated by jobs in the pipeline.

.. _cmd-spack-ci-rebuild:

^^^^^^^^^^^^^^^^^^^^
``spack ci rebuild``
^^^^^^^^^^^^^^^^^^^^

The purpose of ``spack ci rebuild`` is to take an assigned
spec and ensure a binary of a successful build exists on the target mirror.
If the binary does not already exist, it is built from source and pushed
to the mirror. The associated stand-alone tests are optionally run against
the new build. Additionally, files for reproducing the build outside of the
CI environment are created to facilitate debugging.

If a binary for the spec does not exist on the target mirror, an install
shell script, ``install.sh``, is created and saved in the current working
directory. The script is run in a job to install the spec from source. The
resulting binary package is pushed to the mirror. If ``cdash`` is configured
for the environment, then the build results will be uploaded to the site.

Environment variables and values in the ``ci::pipeline-gen`` section of the
``spack.yaml`` environment file provide inputs to this process. The
two main sources of environment variables are variables written into
``.gitlab-ci.yml`` by ``spack ci generate`` and the GitLab CI runtime.
Several key CI pipeline variables are described in
:ref:`ci_environment_variables`.

If the ``--tests`` option is provided, stand-alone tests are performed but
only if the build was successful *and* the package does not appear in the
list of ``broken-tests-packages``. A shell script, ``test.sh``, is created
and run to perform the tests. On completion, test logs are exported as job
artifacts for review and to facilitate debugging. If `cdash` is configured,
test results are also uploaded to the site.

A snippet from an example ``spack.yaml`` file illustrating use of this
option *and* specification of a package with broken tests is given below.
The inclusion of a spec for building ``gptune`` is not shown here. Note
that ``--tests`` is passed to ``spack ci rebuild`` as part of the
``build-job`` script.

.. code-block:: yaml

  ci:
    pipeline-gen:
    - build-job
        script:
          - . "./share/spack/setup-env.sh"
          - spack --version
          - cd ${SPACK_CONCRETE_ENV_DIR}
          - spack env activate --without-view .
          - spack config add "config:install_tree:projections:${SPACK_JOB_SPEC_PKG_NAME}:'morepadding/{architecture}/{compiler.name}-{compiler.version}/{name}-{version}-{hash}'"
           - mkdir -p ${SPACK_ARTIFACTS_ROOT}/user_data
           - if [[ -r /mnt/key/intermediate_ci_signing_key.gpg ]]; then spack gpg trust /mnt/key/intermediate_ci_signing_key.gpg; fi
           - if [[ -r /mnt/key/spack_public_key.gpg ]]; then spack gpg trust /mnt/key/spack_public_key.gpg; fi
           - spack -d ci rebuild --tests > >(tee ${SPACK_ARTIFACTS_ROOT}/user_data/pipeline_out.txt) 2> >(tee ${SPACK_ARTIFACTS_ROOT}/user_data/pipeline_err.txt >&2)

     broken-tests-packages:
       - gptune

In this case, even if ``gptune`` is successfully built from source, the
pipeline will *not* run its stand-alone tests since the package is listed
under ``broken-tests-packages``.

Spack's cloud pipelines provide actual, up-to-date examples of the CI/CD
configuration and environment files used by Spack. You can find them
under Spack's `stacks
<https://github.com/spack/spack/tree/develop/share/spack/gitlab/cloud_pipelines/stacks>`_ repository directory.

.. _cmd-spack-ci-rebuild-index:

^^^^^^^^^^^^^^^^^^^^^^^^^^
``spack ci rebuild-index``
^^^^^^^^^^^^^^^^^^^^^^^^^^

This is a convenience command to rebuild the buildcache index associated with
the mirror in the active, gitlab-enabled environment (specifying the mirror
url or name is not required).

.. _cmd-spack-ci-reproduce-build:

^^^^^^^^^^^^^^^^^^^^^^^^^^^^
``spack ci reproduce-build``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Given the url to a gitlab pipeline rebuild job, downloads and unzips the
artifacts into a local directory (which can be specified with the optional
``--working-dir`` argument), then finds the target job in the generated
pipeline to extract details about how it was run.  Assuming the job used a
docker image, the command prints a ``docker run`` command line and some basic
instructions on how to reproduce the build locally.

Note that jobs failing in the pipeline will print messages giving the
arguments you can pass to ``spack ci reproduce-build`` in order to reproduce
a particular build locally.

------------------------------------
Job Types
------------------------------------

^^^^^^^^^^^^^^^
Rebuild (build)
^^^^^^^^^^^^^^^

Rebuild jobs, denoted as ``build-job``'s in the ``pipeline-gen`` list, are jobs
associated with concrete specs that have been marked for rebuild. By default a simple
script for doing rebuild is generated, but may be modified as needed.

The default script does three main steps, change directories to the pipelines concrete
environment, activate the concrete environment, and run the ``spack ci rebuild`` command:

.. code-block:: bash

  cd ${concrete_environment_dir}
  spack env activate --without-view .
  spack ci rebuild

.. _rebuild_index:

^^^^^^^^^^^^^^^^^^^^^^
Update Index (reindex)
^^^^^^^^^^^^^^^^^^^^^^

By default, while a pipeline job may rebuild a package, create a buildcache
entry, and push it to the mirror, it does not automatically re-generate the
mirror's buildcache index afterward.  Because the index is not needed by the
default rebuild jobs in the pipeline, not updating the index at the end of
each job avoids possible race conditions between simultaneous jobs, and it
avoids the computational expense of regenerating the index.  This potentially
saves minutes per job, depending on the number of binary packages in the
mirror.  As a result, the default is that the mirror's buildcache index may
not correctly reflect the mirror's contents at the end of a pipeline.

To make sure the buildcache index is up to date at the end of your pipeline,
spack generates a job to update the buildcache index of the target mirror
at the end of each pipeline by default.  You can disable this behavior by
adding ``rebuild-index: False`` inside the ``ci`` section of your
spack environment.

Reindex jobs do not allow modifying the ``script`` attribute since it is automatically
generated using the target mirror listed in the ``mirrors::mirror`` configuration.

^^^^^^^^^^^^^^^^^
Signing (signing)
^^^^^^^^^^^^^^^^^

This job is run after all of the rebuild jobs are completed and is intended to be used
to sign the package binaries built by a protected CI run. Signing jobs are generated
only if a signing job ``script`` is specified and the spack CI job type is protected.
Note, if an ``any-job`` section contains a script, this will not implicitly create a
``signing`` job, a signing job may only exist if it is explicitly specified in the
configuration with a ``script`` attribute. Specifying a signing job without a script
does not create a signing job and the job configuration attributes will be ignored.
Signing jobs are always assigned the runner tags ``aws``, ``protected``, and ``notary``.

.. _noop_jobs:

^^^^^^^^^^^^
No Op (noop)
^^^^^^^^^^^^

If no specs in an environment need to be rebuilt during a given pipeline run
(meaning all are already up to date on the mirror), a single successful job
(a NO-OP) is still generated to avoid an empty pipeline (which GitLab
considers to be an error).  The ``noop-job*`` sections
can be added to your ``spack.yaml`` where you can provide ``tags`` and
``image`` or ``variables`` for the generated NO-OP job.  This section also
supports providing ``before_script``, ``script``, and ``after_script``, in
case you want to take some custom actions in the case of any empty pipeline.

Following is an example of this section added to a ``spack.yaml``:

.. code-block:: yaml

  spack:
     ci:
       pipeline-gen:
       - noop-job:
           tags: ['custom', 'tag']
           image:
             name: 'some.image.registry/custom-image:latest'
             entrypoint: ['/bin/bash']
           script::
             - echo "Custom message in a custom script"

The example above illustrates how you can provide the attributes used to run
the NO-OP job in the case of an empty pipeline.  The only field for the NO-OP
job that might be generated for you is ``script``, but that will only happen
if you do not provide one yourself. Notice in this example the ``script``
uses the ``::`` notation to prescribe override behavior. Without this, the
``echo`` command would have been prepended to the automatically generated script
rather than replacing it.

------------------------------------
ci.yaml
------------------------------------

Here's an example of a spack configuration file describing a build pipeline:

.. code-block:: yaml

  ci:
    target: gitlab

    rebuild_index: True

    broken-specs-url: https://broken.specs.url

    broken-tests-packages:
    - gptune

    pipeline-gen:
    - submapping:
      - match:
          - os=ubuntu18.04
        build-job:
          tags:
            - spack-kube
          image: spack/ubuntu-bionic
      - match:
          - os=centos7
        build-job:
          tags:
            - spack-kube
          image: spack/centos7

  cdash:
    build-group: Release Testing
    url: https://cdash.spack.io
    project: Spack
    site: Spack AWS Gitlab Instance

The ``ci`` config section is used to configure how the pipeline workload should be
generated, mainly how the jobs for building specs should be assigned to the
configured runners on your instance. The main section for configuring pipelines
is ``pipeline-gen``, which is a list of job attribute sections that are merged,
using the same rules as Spack configs (:ref:`config-scope-precedence`), from the bottom up.
The order sections are applied is to be consistent with how spack orders scope precedence when merging lists.
There are two main section types, ``<type>-job`` sections and ``submapping``
sections.


^^^^^^^^^^^^^^^^^^^^^^
Job Attribute Sections
^^^^^^^^^^^^^^^^^^^^^^

Each type of job may have attributes added or removed via sections in the ``pipeline-gen``
list. Job type specific attributes may be specified using the keys ``<type>-job`` to
add attributes to all jobs of type ``<type>`` or ``<type>-job-remove`` to remove attributes
of type ``<type>``. Each section may only contain one type of job attribute specification, ie. ,
``build-job`` and ``noop-job`` may not coexist but ``build-job`` and ``build-job-remove`` may.

.. note::
    The ``*-remove`` specifications are applied before the additive attribute specification.
    For example, in the case where both ``build-job`` and ``build-job-remove`` are listed in
    the same ``pipeline-gen`` section, the value will still exist in the merged build-job after
    applying the section.

All of the attributes specified are forwarded to the generated CI jobs, however special
treatment is applied to the attributes ``tags``, ``image``, ``variables``, ``script``,
``before_script``, and ``after_script`` as they are components recognized explicitly by the
Spack CI generator. For the ``tags`` attribute, Spack will remove reserved tags
(:ref:`reserved_tags`) from all jobs specified in the config. In some cases, such as for
``signing`` jobs, reserved tags will be added back based on the type of CI that is being run.

Once a runner has been chosen to build a release spec, the ``build-job*``
sections provide information determining details of the job in the context of
the runner.  At lease one of the ``build-job*`` sections must contain a ``tags`` key, which
is a list containing at least one tag used to select the runner from among the
runners known to the gitlab instance.  For Docker executor type runners, the
``image`` key is used to specify the Docker image used to build the release spec
(and could also appear as a dictionary with a ``name`` specifying the image name,
as well as an ``entrypoint`` to override whatever the default for that image is).
For other types of runners the ``variables`` key will be useful to pass any
information on to the runner that it needs to do its work (e.g. scheduler
parameters, etc.).  Any ``variables`` provided here will be added, verbatim, to
each job.

The ``build-job`` section also allows users to supply custom ``script``,
``before_script``, and ``after_script`` sections to be applied to every job
scheduled on that runner.  This allows users to do any custom preparation or
cleanup tasks that fit their particular workflow, as well as completely
customize the rebuilding of a spec if they so choose.  Spack will not generate
a ``before_script`` or ``after_script`` for jobs, but if you do not provide
a custom ``script``, spack will generate one for you that assumes the concrete
environment directory is located within your ``--artifacts_root`` (or if not
provided, within your ``$CI_PROJECT_DIR``), activates that environment for
you, and invokes ``spack ci rebuild``.

Sections that specify scripts (``script``, ``before_script``, ``after_script``) are all
read as lists of commands or lists of lists of commands. It is recommended to write scripts
as lists of lists if scripts will be composed via merging. The default behavior of merging
lists will remove duplicate commands and potentially apply unwanted reordering, whereas
merging lists of lists will preserve the local ordering and never removes duplicate
commands. When writing commands to the CI target script, all lists are expanded and
flattened into a single list.

^^^^^^^^^^^^^^^^^^^
Submapping Sections
^^^^^^^^^^^^^^^^^^^

A special case of attribute specification is the ``submapping`` section which may be used
to apply job attributes to build jobs based on the package spec associated with the rebuild
job. Submapping is specified as a list of spec ``match`` lists associated with
``build-job``/``build-job-remove`` sections. There are two options for ``match_behavior``,
either ``first`` or ``merge`` may be specified. In either case, the ``submapping`` list is
processed from the bottom up, and then each ``match`` list is searched for a string that
satisfies the check ``spec.satisfies({match_item})`` for each concrete spec.

The the case of ``match_behavior: first``, the first ``match`` section in the list of
``submappings`` that contains a string that satisfies the spec will apply it's
``build-job*`` attributes to the rebuild job associated with that spec. This is the
default behavior and will be the method if no ``match_behavior`` is specified.

The the case of ``merge`` match, all of the ``match`` sections in the list of
``submappings`` that contain a string that satisfies the spec will have the associated
``build-job*`` attributes applied to the rebuild job associated with that spec. Again,
the attributes will be merged starting from the bottom match going up to the top match.

In the case that no match is found in a submapping section, no additional attributes will be applied.


^^^^^^^^^^^^^^^^^^^^^^^^
Dynamic Mapping Sections
^^^^^^^^^^^^^^^^^^^^^^^^

For large scale CI where cost optimization is required, dynamic mapping allows for the use of real-time
mapping schemes served by a web service. This type of mapping does not support the ``-remove`` type
behavior, but it does follow the rest of the merge rules for configurations.

The dynamic mapping service needs to implement a single REST API interface for getting
requests ``GET <URL>[:PORT][/PATH]?spec=<pkg_name@pkg_version +variant1+variant2%compiler@compiler_version>``.

example request.

.. code-block::

  https://my-dyn-mapping.spack.io/allocation?spec=zlib-ng@2.1.6 +compat+opt+shared+pic+new_strategies arch=linux-ubuntu20.04-x86_64_v3%gcc@12.0.0


With an example response the updates kubernetes request variables, overrides the max retries for gitlab,
and prepends a note about the modifications made by the my-dyn-mapping.spack.io service.

.. code-block::

  200 OK

  {
    "variables":
    {
      "KUBERNETES_CPU_REQUEST": "500m",
      "KUBERNETES_MEMORY_REQUEST": "2G",
    },
    "retry": { "max:": "1"}
    "script+:":
    [
      "echo \"Job modified by my-dyn-mapping.spack.io\""
    ]
  }


The ci.yaml configuration section takes the URL endpoint as well as a number of options to configure how responses are handled.

It is possible to specify a list of allowed and ignored configuration attributes under ``allow`` and ``ignore``
respectively. It is also possible to configure required attributes under ``required`` section.

Options to configure the client timeout and SSL verification using the ``timeout`` and ``verify_ssl`` options.
By default, the ``timeout`` is set to the option in ``config:timeout`` and ``veryify_ssl`` is set the the option in ``config::verify_ssl``.

Passing header parameters to the request can be achieved through the ``header`` section. The values of the variables passed to the
header may be environment variables that are expanded at runtime, such as a private token configured on the runner.

Here is an example configuration pointing to ``my-dyn-mapping.spack.io/allocation``.


.. code-block:: yaml

  ci:
  - dynamic-mapping:
      endpoint: my-dyn-mapping.spack.io/allocation
      timeout: 10
      verify_ssl: True
      header:
        PRIVATE_TOKEN: ${MY_PRIVATE_TOKEN}
        MY_CONFIG: "fuzz_allocation:false"
      allow:
      - variables
      ignore:
      - script
      require: []


^^^^^^^^^^^^^
Bootstrapping
^^^^^^^^^^^^^


The ``bootstrap`` section allows you to specify lists of specs from
your ``definitions`` that should be staged ahead of the environment's ``specs``. At the moment
the only viable use-case for bootstrapping is to install compilers.

Here's an example of what bootstrapping some compilers might look like:

.. code-block:: yaml

   spack:
     definitions:
     - compiler-pkgs:
       - 'llvm+clang@6.0.1 os=centos7'
       - 'gcc@6.5.0 os=centos7'
       - 'llvm+clang@6.0.1 os=ubuntu18.04'
       - 'gcc@6.5.0 os=ubuntu18.04'
     - pkgs:
       - readline@7.0
     - compilers:
       - '%gcc@5.5.0'
       - '%gcc@6.5.0'
       - '%gcc@7.3.0'
       - '%clang@6.0.0'
       - '%clang@6.0.1'
     - oses:
       - os=ubuntu18.04
       - os=centos7
     specs:
     - matrix:
       - [$pkgs]
       - [$compilers]
       - [$oses]
       exclude:
         - '%gcc@7.3.0 os=centos7'
         - '%gcc@5.5.0 os=ubuntu18.04'
     ci:
       bootstrap:
         - name: compiler-pkgs
           compiler-agnostic: true
       pipeline-gen:
         # similar to the example higher up in this description
         ...

The example above adds a list to the ``definitions`` called ``compiler-pkgs``
(you can add any number of these), which lists compiler packages that should
be staged ahead of the full matrix of release specs (in this example, only
readline).  Then within the ``ci`` section, note the addition of a
``bootstrap`` section, which can contain a list of items, each referring to
a list in the ``definitions`` section.  These items can either
be a dictionary or a string.  If you supply a dictionary, it must have a name
key whose value must match one of the lists in definitions and it can have a
``compiler-agnostic`` key whose value is a boolean.  If you supply a string,
then it needs to match one of the lists provided in ``definitions``.  You can
think of the bootstrap list as an ordered list of pipeline "phases" that will
be staged before your actual release specs.  While this introduces another
layer of bottleneck in the pipeline (all jobs in all stages of one phase must
complete before any jobs in the next phase can begin), it also means you are
guaranteed your bootstrapped compilers will be available when you need them.

The ``compiler-agnostic`` key can be provided with each item in the
bootstrap list. It tells the ``spack ci generate`` command that any jobs staged
from that particular list should have the compiler removed from the spec, so
that any compiler available on the runner where the job is run can be used to
build the package.

When including a bootstrapping phase as in the example above, the result is that
the bootstrapped compiler packages will be pushed to the binary mirror (and the
local artifacts mirror) before the actual release specs are built.

Since bootstrapping compilers is optional, those items can be left out of the
environment/stack file, and in that case no bootstrapping will be done (only the
specs will be staged for building) and the runners will be expected to already
have all needed compilers installed and configured for spack to use.

^^^^^^^^^^^^^^^^
Broken Specs URL
^^^^^^^^^^^^^^^^

The optional ``broken-specs-url`` key tells Spack to check against a list of
specs that are known to be currently broken in ``develop``. If any such specs
are found, the ``spack ci generate`` command will fail with an error message
informing the user what broken specs were encountered. This allows the pipeline
to fail early and avoid wasting compute resources attempting to build packages
that will not succeed.

^^^^^
CDash
^^^^^

The optional ``cdash`` section provides information that will be used by the
``spack ci generate`` command (invoked by ``spack ci start``) for reporting
to CDash.  All the jobs generated from this environment will belong to a
"build group" within CDash that can be tracked over time.  As the release
progresses, this build group may have jobs added or removed. The url, project,
and site are used to specify the CDash instance to which build results should
be reported.

Take a look at the
`schema <https://github.com/spack/spack/blob/develop/lib/spack/spack/schema/ci.py>`_
for the ci section of the spack environment file, to see precisely what
syntax is allowed there.

.. _reserved_tags:

^^^^^^^^^^^^^
Reserved Tags
^^^^^^^^^^^^^

Spack has a subset of tags (``public``, ``protected``, and ``notary``) that it reserves
for classifying runners that may require special permissions or access. The tags
``public`` and ``protected`` are used to distinguish between runners that use public
permissions and runners with protected permissions. The ``notary`` tag is a special tag
that is used to indicate runners that have access to the highly protected information
used for signing binaries using the ``signing`` job.

.. _staging_algorithm:

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Summary of ``.gitlab-ci.yml`` generation algorithm
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

All specs yielded by the matrix (or all the specs in the environment) have their
dependencies computed, and the entire resulting set of specs are staged together
before being run through the ``ci/pipeline-gen`` entries, where each staged
spec is assigned a runner.  "Staging" is the name given to the process of
figuring out in what order the specs should be built, taking into consideration
Gitlab CI rules about jobs/stages.  In the staging process the goal is to maximize
the number of jobs in any stage of the pipeline, while ensuring that the jobs in
any stage only depend on jobs in previous stages (since those jobs are guaranteed
to have completed already).  As a runner is determined for a job, the information
in the merged ``any-job*`` and ``build-job*`` sections is used to populate various parts of the job
description that will be used by the target CI pipelines. Once all the jobs have been assigned
a runner, the ``.gitlab-ci.yml`` is written to disk.

The short example provided above would result in the ``readline``, ``ncurses``,
and ``pkgconf`` packages getting staged and built on the runner chosen by the
``spack-k8s`` tag.  In this example, spack assumes the runner is a Docker executor
type runner, and thus certain jobs will be run in the ``centos7`` container,
and others in the ``ubuntu-18.04`` container.  The resulting ``.gitlab-ci.yml``
will contain 6 jobs in three stages.  Once the jobs have been generated, the
presence of a ``SPACK_CDASH_AUTH_TOKEN`` environment variable during the
``spack ci generate`` command would result in all of the jobs being put in a
build group on CDash called "Release Testing" (that group will be created if
it didn't already exist).

-------------------------------------
Using a custom spack in your pipeline
-------------------------------------

If your runners will not have a version of spack ready to invoke, or if for some
other reason you want to use a custom version of spack to run your pipelines,
this section provides an example of how you could take advantage of
user-provided pipeline scripts to accomplish this fairly simply.  First, consider
specifying the source and version of spack you want to use with variables, either
written directly into your ``.gitlab-ci.yml``, or provided by CI variables defined
in the gitlab UI or from some upstream pipeline.  Let's say you choose the variable
names ``SPACK_REPO`` and ``SPACK_REF`` to refer to the particular fork of spack
and branch you want for running your pipeline.  You can then refer to those in a
custom shell script invoked both from your pipeline generation job and your rebuild
jobs.  Here's the ``generate-pipeline`` job from the top of this document,
updated to clone and source a custom spack:

.. code-block:: yaml

   generate-pipeline:
     tags:
       - <some-other-tag>
   before_script:
     - git clone ${SPACK_REPO}
     - pushd spack && git checkout ${SPACK_REF} && popd
     - . "./spack/share/spack/setup-env.sh"
   script:
     - spack env activate --without-view .
     - spack ci generate --check-index-only
       --artifacts-root "${CI_PROJECT_DIR}/jobs_scratch_dir"
       --output-file "${CI_PROJECT_DIR}/jobs_scratch_dir/pipeline.yml"
   after_script:
     - rm -rf ./spack
   artifacts:
     paths:
       - "${CI_PROJECT_DIR}/jobs_scratch_dir"

That takes care of getting the desired version of spack when your pipeline is
generated by ``spack ci generate``.  You also want your generated rebuild jobs
(all of them) to clone that version of spack, so next you would update your
``spack.yaml`` from above as follows:

.. code-block:: yaml

   spack:
     # ...
     ci:
       pipeline-gen:
       - build-job:
           tags:
             - spack-kube
           image: spack/ubuntu-bionic
           before_script:
             - git clone ${SPACK_REPO}
             - pushd spack && git checkout ${SPACK_REF} && popd
             - . "./spack/share/spack/setup-env.sh"
           script:
             - spack env activate --without-view ${SPACK_CONCRETE_ENV_DIR}
             - spack -d ci rebuild
           after_script:
             - rm -rf ./spack

Now all of the generated rebuild jobs will use the same shell script to clone
spack before running their actual workload.

Now imagine you have long pipelines with many specs to be built, and you
are pointing to a spack repository and branch that has a tendency to change
frequently, such as the main repo and its ``develop`` branch.  If each child
job checks out the ``develop`` branch, that could result in some jobs running
with one SHA of spack, while later jobs run with another.  To help avoid this
issue, the pipeline generation process saves global variables called
``SPACK_VERSION`` and ``SPACK_CHECKOUT_VERSION`` that capture the version
of spack used to generate the pipeline.  While the ``SPACK_VERSION`` variable
simply contains the human-readable value produced by ``spack -V`` at pipeline
generation time, the ``SPACK_CHECKOUT_VERSION`` variable can be used in a
``git checkout`` command to make sure all child jobs checkout the same version
of spack used to generate the pipeline.  To take advantage of this, you could
simply replace ``git checkout ${SPACK_REF}`` in the example ``spack.yaml``
above with ``git checkout ${SPACK_CHECKOUT_VERSION}``.

On the other hand, if you're pointing to a spack repository and branch under your
control, there may be no benefit in using the captured ``SPACK_CHECKOUT_VERSION``,
and you can instead just clone using the variables you define (``SPACK_REPO``
and ``SPACK_REF`` in the example above).

.. _custom_workflow:

---------------
Custom Workflow
---------------

There are many ways to take advantage of spack CI pipelines to achieve custom
workflows for building packages or other resources.  One example of a custom
pipelines workflow is the spack tutorial container
`repo <https://github.com/spack/spack-tutorial-container>`_.  This project uses
GitHub (for source control), GitLab (for automated spack ci pipelines), and
DockerHub automated builds to build Docker images (complete with fully populate
binary mirror) used by instructors and participants of a spack tutorial.

Take a look a the repo to see how it is accomplished using spack CI pipelines,
and see the following markdown files at the root of the repository for
descriptions and documentation describing the workflow: ``DESCRIPTION.md``,
``DOCKERHUB_SETUP.md``, ``GITLAB_SETUP.md``, and ``UPDATING.md``.

.. _ci_environment_variables:

--------------------------------------------------
Environment variables affecting pipeline operation
--------------------------------------------------

Certain secrets and some other information should be provided to the pipeline
infrastructure via environment variables, usually for reasons of security, but
in some cases to support other pipeline use cases such as PR testing.  The
environment variables used by the pipeline infrastructure are described here.

^^^^^^^^^^^^^^^^^
AWS_ACCESS_KEY_ID
^^^^^^^^^^^^^^^^^

Optional.  Only needed when binary mirror is an S3 bucket.

^^^^^^^^^^^^^^^^^^^^^
AWS_SECRET_ACCESS_KEY
^^^^^^^^^^^^^^^^^^^^^

Optional.  Only needed when binary mirror is an S3 bucket.

^^^^^^^^^^^^^^^
S3_ENDPOINT_URL
^^^^^^^^^^^^^^^

Optional.  Only needed when binary mirror is an S3 bucket that is *not* on AWS.

^^^^^^^^^^^^^^^^^
CDASH_AUTH_TOKEN
^^^^^^^^^^^^^^^^^

Optional. Only needed in order to report build groups to CDash.

^^^^^^^^^^^^^^^^^
SPACK_SIGNING_KEY
^^^^^^^^^^^^^^^^^

Optional.  Only needed if you want ``spack ci rebuild`` to trust the key you
store in this variable, in which case, it will subsequently be used to sign and
verify binary packages (when installing or creating buildcaches).  You could
also have already trusted a key spack know about, or if no key is present anywhere,
spack will install specs using ``--no-check-signature`` and create buildcaches
using ``-u`` (for unsigned binaries).

