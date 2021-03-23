.. Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
   Spack Project Developers. See the top-level COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. _pipelines:

=========
Pipelines
=========

Spack provides commands that support generating and running automated build
pipelines designed for Gitlab CI.  At the highest level it works like this:
provide a spack environment describing the set of packages you care about,
and include within that environment file a description of how those packages
should be mapped to Gitlab runners.  Spack can then generate a ``.gitlab-ci.yml``
file containing job descriptions for all your packages that can be run by a
properly configured Gitlab CI instance.  When run, the generated pipeline will
build and deploy binaries, and it can optionally report to a CDash instance
regarding the health of the builds as they evolve over time.

------------------------------
Getting started with pipelines
------------------------------

It is fairly straightforward to get started with automated build pipelines.  At
a minimum, you'll need to set up a Gitlab instance (more about Gitlab CI
`here <https://about.gitlab.com/product/continuous-integration/>`_) and configure
at least one `runner <https://docs.gitlab.com/runner/>`_.  Then the basic steps
for setting up a build pipeline are as follows:

#. Create a repository on your gitlab instance
#. Add a ``spack.yaml`` at the root containing your pipeline environment (see
   below for details)
#. Add a ``.gitlab-ci.yml`` at the root containing two jobs (one to generate
   the pipeline dynamically, and one to run the generated jobs), similar to
   this one:

   .. code-block:: yaml

      stages: [generate, build]

      generate-pipeline:
        stage: generate
        tags:
          - <custom-tag>
        script:
          - spack env activate --without-view .
          - spack ci generate
            --output-file "${CI_PROJECT_DIR}/jobs_scratch_dir/pipeline.yml"
        artifacts:
          paths:
            - "${CI_PROJECT_DIR}/jobs_scratch_dir/pipeline.yml"

      build-jobs:
        stage: build
        trigger:
          include:
            - artifact: "jobs_scratch_dir/pipeline.yml"
              job: generate-pipeline
          strategy: depend


#. Add any secrets required by the CI process to environment variables using the
   CI web ui
#. Push a commit containing the ``spack.yaml`` and ``.gitlab-ci.yml`` mentioned above
   to the gitlab repository

The ``<custom-tag>``, above, is used to pick one of your configured runners to
run the pipeline generation phase (this is implemented in the ``spack ci generate``
command, which assumes the runner has an appropriate version of spack installed
and configured for use).  Of course, there are many ways to customize the process.
You can configure CDash reporting on the progress of your builds, set up S3 buckets
to mirror binaries built by the pipeline, clone a custom spack repository/ref for
use by the pipeline, and more.

While it is possible to set up pipelines on gitlab.com, the builds there are
limited to 60 minutes and generic hardware.  It is also possible to
`hook up <https://about.gitlab.com/blog/2018/04/24/getting-started-gitlab-ci-gcp>`_
Gitlab to Google Kubernetes Engine (`GKE <https://cloud.google.com/kubernetes-engine/>`_)
or Amazon Elastic Kubernetes Service (`EKS <https://aws.amazon.com/eks>`_), though those
topics are outside the scope of this document.

Spack's pipelines are now making use of the
`trigger <https://docs.gitlab.com/12.9/ee/ci/yaml/README.html#trigger>`_ syntax to run
dynamically generated
`child pipelines <https://docs.gitlab.com/12.9/ee/ci/parent_child_pipelines.html>`_.
Note that the use of dynamic child pipelines requires running Gitlab version
``>= 12.9``.

-----------------------------------
Spack commands supporting pipelines
-----------------------------------

Spack provides a command ``ci`` with two sub-commands: ``spack ci generate`` generates
a pipeline (a .gitlab-ci.yml file) from a spack environment, and ``spack ci rebuild``
checks a spec against a remote mirror and possibly rebuilds it from source and updates
the binary mirror with the latest built package.  Both ``spack ci ...`` commands must
be run from within the same environment, as each one makes use of the environment for
different purposes.  Additionally, some options to the commands (or conditions present
in the spack environment file) may require particular environment variables to be
set in order to function properly.  Examples of these are typically secrets
needed for pipeline operation that should not be visible in a spack environment
file.  These environment variables are described in more detail
:ref:`ci_environment_variables`.

.. _cmd-spack-ci:

^^^^^^^^^^^^^^^^^^
``spack ci``
^^^^^^^^^^^^^^^^^^

Super-command for functionality related to generating pipelines and executing
pipeline jobs.

.. _cmd-spack-ci-generate:

^^^^^^^^^^^^^^^^^^^^^
``spack ci generate``
^^^^^^^^^^^^^^^^^^^^^

Concretizes the specs in the active environment, stages them (as described in
:ref:`staging_algorithm`), and writes the resulting ``.gitlab-ci.yml`` to disk.

Using ``--prune-dag`` or ``--no-prune-dag`` configures whether or not jobs are
generated for specs that are already up to date on the mirror.   If enabling
DAG pruning using ``--prune-dag``, more information may be required in your
``spack.yaml`` file, see the :ref:`noop_jobs` section below regarding
``service-job-attributes``.

The ``--optimize`` argument is experimental and runs the generated pipeline
document through a series of optimization passes designed to reduce the size
of the generated file.

The ``--dependencies`` is also experimental and disables what in Gitlab is
referred to as DAG scheduling, internally using the ``dependencies`` keyword
rather than ``needs`` to list dependency jobs.  The drawback of using this option
is that before any job can begin, all jobs in previous stages must first
complete.  The benefit is that Gitlab allows more dependencies to be listed
when using ``dependencies`` instead of ``needs``.

The optional ``--output-file`` argument should be an absolute path (including
file name) to the generated pipeline, and if not given, the default is
``./.gitlab-ci.yml``.

.. _cmd-spack-ci-rebuild:

^^^^^^^^^^^^^^^^^^^^
``spack ci rebuild``
^^^^^^^^^^^^^^^^^^^^

This sub-command is responsible for ensuring a single spec from the release
environment is up to date on the remote mirror configured in the environment,
and as such, corresponds to a single job in the ``.gitlab-ci.yml`` file.

Rather than taking command-line arguments, this sub-command expects information
to be communicated via environment variables, which will typically come via the
``.gitlab-ci.yml`` job as ``variables``.

------------------------------------
A pipeline-enabled spack environment
------------------------------------

Here's an example of a spack environment file that has been enhanced with
sections describing a build pipeline:

.. code-block:: yaml

   spack:
     definitions:
     - pkgs:
       - readline@7.0
     - compilers:
       - '%gcc@5.5.0'
     - oses:
       - os=ubuntu18.04
       - os=centos7
     specs:
     - matrix:
       - [$pkgs]
       - [$compilers]
       - [$oses]
     mirrors:
       cloud_gitlab: https://mirror.spack.io
     gitlab-ci:
       mappings:
         - match:
             - os=ubuntu18.04
           runner-attributes:
             tags:
               - spack-kube
             image: spack/ubuntu-bionic
         - match:
             - os=centos7
           runner-attributes:
             tags:
               - spack-kube
             image: spack/centos7
     cdash:
       build-group: Release Testing
       url: https://cdash.spack.io
       project: Spack
       site: Spack AWS Gitlab Instance

Hopefully, the ``definitions``, ``specs``, ``mirrors``, etc. sections are already
familiar, as they are part of spack :ref:`environments`.  So let's take a more
in-depth look some of the pipeline-related sections in that environment file
that might not be as familiar.

The ``gitlab-ci`` section is used to configure how the pipeline workload should be
generated, mainly how the jobs for building specs should be assigned to the
configured runners on your instance.  Each entry within the list of ``mappings``
corresponds to a known gitlab runner, where the ``match`` section is used
in assigning a release spec to one of the runners, and the ``runner-attributes``
section is used to configure the spec/job for that particular runner.

Both the top-level ``gitlab-ci`` section as well as each ``runner-attributes``
section can also contain the following keys: ``image``, ``tags``, ``variables``,
``before_script``, ``script``, and ``after_script``.  If any of these keys are
provided at the ``gitlab-ci`` level, they will be used as the defaults for any
``runner-attributes``, unless they are overridden in those sections.  Specifying
any of these keys at the ``runner-attributes`` level generally overrides the
keys specified at the higher level, with a couple exceptions.  Any ``variables``
specified at both levels result in those dictionaries getting merged in the
resulting generated job, and any duplicate variable names get assigned the value
provided in the specific ``runner-attributes``.  If ``tags`` are specified both
at the ``gitlab-ci`` level as well as the ``runner-attributes`` level, then the
lists of tags are combined, and any duplicates are removed.

See the section below on using a custom spack for an example of how these keys
could be used.

There are other pipeline options you can configure within the ``gitlab-ci`` section
as well.

The ``bootstrap`` section allows you to specify lists of specs from
your ``definitions`` that should be staged ahead of the environment's ``specs`` (this
section is described in more detail below).  The ``enable-artifacts-buildcache`` key
takes a boolean and determines whether the pipeline uses artifacts to store and
pass along the buildcaches from one stage to the next (the default if you don't
provide this option is ``False``).

The optional ``cdash`` section provides information that will be used by the
``spack ci generate`` command (invoked by ``spack ci start``) for reporting
to CDash.  All the jobs generated from this environment will belong to a
"build group" within CDash that can be tracked over time.  As the release
progresses, this build group may have jobs added or removed. The url, project,
and site are used to specify the CDash instance to which build results should
be reported.

Take a look at the
`schema <https://github.com/spack/spack/blob/develop/lib/spack/spack/schema/gitlab_ci.py>`_
for the gitlab-ci section of the spack environment file, to see precisely what
syntax is allowed there.

.. _rebuild_index:

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Note about rebuilding buildcache index
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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
adding ``rebuild-index: False`` inside the ``gitlab-ci`` section of your
spack environment.  Spack will assign the job any runner attributes found
on the ``service-job-attributes``, if you have provided that in your
``spack.yaml``.

.. _noop_jobs:

^^^^^^^^^^^^^^^^^^^^^^^
Note about "no-op" jobs
^^^^^^^^^^^^^^^^^^^^^^^

If no specs in an environment need to be rebuilt during a given pipeline run
(meaning all are already up to date on the mirror), a single succesful job
(a NO-OP) is still generated to avoid an empty pipeline (which GitLab
considers to be an error).  An optional ``service-job-attributes`` section
can be added to your ``spack.yaml`` where you can provide ``tags`` and
``image`` or ``variables`` for the generated NO-OP job.  This section also
supports providing ``before_script``, ``script``, and ``after_script``, in
case you want to take some custom actions in the case of any empty pipeline.

Following is an example of this section added to a ``spack.yaml``:

.. code-block:: yaml

   spack:
     specs:
       - openmpi
     mirrors:
       cloud_gitlab: https://mirror.spack.io
     gitlab-ci:
       mappings:
         - match:
             - os=centos8
           runner-attributes:
             tags:
               - custom
               - tag
             image: spack/centos7
       service-job-attributes:
         tags: ['custom', 'tag']
         image:
           name: 'some.image.registry/custom-image:latest'
           entrypoint: ['/bin/bash']
         script:
           - echo "Custom message in a custom script"

The example above illustrates how you can provide the attributes used to run
the NO-OP job in the case of an empty pipeline.  The only field for the NO-OP
job that might be generated for you is ``script``, but that will only happen
if you do not provide one yourself.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Assignment of specs to runners
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``mappings`` section corresponds to a list of runners, and during assignment
of specs to runners, the list is traversed in order looking for matches, the
first runner that matches a release spec is assigned to build that spec.  The
``match`` section within each runner mapping section is a list of specs, and
if any of those specs match the release spec (the ``spec.satisfies()`` method
is used), then that runner is considered a match.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Configuration of specs/jobs for a runner
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Once a runner has been chosen to build a release spec, the ``runner-attributes``
section provides information determining details of the job in the context of
the runner.  The ``runner-attributes`` section must have a ``tags`` key, which
is a list containing at least one tag used to select the runner from among the
runners known to the gitlab instance.  For Docker executor type runners, the
``image`` key is used to specify the Docker image used to build the release spec
(and could also appear as a dictionary with a ``name`` specifying the image name,
as well as an ``entrypoint`` to override whatever the default for that image is).
For other types of runners the ``variables`` key will be useful to pass any
information on to the runner that it needs to do its work (e.g. scheduler
parameters, etc.).  Any ``variables`` provided here will be added, verbatim, to
each job.

The ``runner-attributes`` section also allows users to supply custom ``script``,
``before_script``, and ``after_script`` sections to be applied to every job
scheduled on that runner.  This allows users to do any custom preparation or
cleanup tasks that fit their particular workflow, as well as completely
customize the rebuilding of a spec if they so choose.  Spack will not generate
a ``before_script`` or ``after_script`` for jobs, but if you do not provide
a custom ``script``, spack will generate one for you that assumes your
``spack.yaml`` is at the root of the repository, activates that environment for
you, and invokes ``spack ci rebuild``.

.. _staging_algorithm:

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Summary of ``.gitlab-ci.yml`` generation algorithm
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

All specs yielded by the matrix (or all the specs in the environment) have their
dependencies computed, and the entire resulting set of specs are staged together
before being run through the ``gitlab-ci/mappings`` entries, where each staged
spec is assigned a runner.  "Staging" is the name given to the process of
figuring out in what order the specs should be built, taking into consideration
Gitlab CI rules about jobs/stages.  In the staging process the goal is to maximize
the number of jobs in any stage of the pipeline, while ensuring that the jobs in
any stage only depend on jobs in previous stages (since those jobs are guaranteed
to have completed already).  As a runner is determined for a job, the information
in the ``runner-attributes`` is used to populate various parts of the job
description that will be used by Gitlab CI. Once all the jobs have been assigned
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

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Optional compiler bootstrapping
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Spack pipelines also have support for bootstrapping compilers on systems that
may not already have the desired compilers installed. The idea here is that
you can specify a list of things to bootstrap in your ``definitions``, and
spack will guarantee those will be installed in a phase of the pipeline before
your release specs, so that you can rely on those packages being available in
the binary mirror when you need them later on in the pipeline.  At the moment
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
     gitlab-ci:
       bootstrap:
         - name: compiler-pkgs
           compiler-agnostic: true
       mappings:
         # mappings similar to the example higher up in this description
         ...

The example above adds a list to the ``definitions`` called ``compiler-pkgs``
(you can add any number of these), which lists compiler packages that should
be staged ahead of the full matrix of release specs (in this example, only
readline).  Then within the ``gitlab-ci`` section, note the addition of a
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
local artifacts mirror) before the actual release specs are built. In this case,
the jobs corresponding to subsequent release specs are configured to
``install_missing_compilers``, so that if spack is asked to install a package
with a compiler it doesn't know about, it can be quickly installed from the
binary mirror first.

Since bootstrapping compilers is optional, those items can be left out of the
environment/stack file, and in that case no bootstrapping will be done (only the
specs will be staged for building) and the runners will be expected to already
have all needed compilers installed and configured for spack to use.

-------------------------------------
Using a custom spack in your pipeline
-------------------------------------

If your runners will not have a version of spack ready to invoke, or if for some
other reason you want to use a custom version of spack to run your pipelines,
this section provides an example of how you could take advantage of
user-provided pipeline scripts to accomplish this fairly simply.  First, you
could use the GitLab user interface to create CI environment variables
containing the url and branch or tag you want to use (calling them, for
example, ``SPACK_REPO`` and ``SPACK_REF``), then refer to those in a custom shell
script invoked both from your pipeline generation job, as well as in your rebuild
jobs.  Here's the ``generate-pipeline`` job from the top of this document,
updated to invoke a custom shell script that will clone and source a custom
spack:

.. code-block:: yaml

   generate-pipeline:
     tags:
       - <some-other-tag>
   before_script:
     - ./cloneSpack.sh
   script:
     - spack env activate --without-view .
     - spack ci generate
       --output-file "${CI_PROJECT_DIR}/jobs_scratch_dir/pipeline.yml"
   after_script:
     - rm -rf ./spack
   artifacts:
     paths:
       - "${CI_PROJECT_DIR}/jobs_scratch_dir/pipeline.yml"

And the ``cloneSpack.sh`` script could contain:

.. code-block:: bash

   #!/bin/bash

   git clone ${SPACK_REPO}
   pushd ./spack
   git checkout ${SPACK_REF}
   popd

   . "./spack/share/spack/setup-env.sh"

   spack --version

Finally, you would also want your generated rebuild jobs to clone that version
of spack, so you would update your ``spack.yaml`` from above as follows:

.. code-block:: yaml

   spack:
     ...
     gitlab-ci:
       mappings:
         - match:
             - os=ubuntu18.04
           runner-attributes:
             tags:
               - spack-kube
             image: spack/ubuntu-bionic
             before_script:
               - ./cloneSpack.sh
             script:
               - spack env activate --without-view .
               - spack -d ci rebuild
             after_script:
               - rm -rf ./spack

Now all of the generated rebuild jobs will use the same shell script to clone
spack before running their actual workload.  Note in the above example the
provision of a custom ``script`` section.  The reason for this is to run
``spack ci rebuild`` in debug mode to get more information when builds fail.

Now imagine you have long pipelines with many specs to be built, and you
are pointing to a spack repository and branch that has a tendency to change
frequently, such as the main repo and it's ``develop`` branch.  If each child
job checks out the ``develop`` branch, that could result in some jobs running
with one SHA of spack, while later jobs run with another.  To help avoid this
issue, the pipeline generation process saves global variables called
``SPACK_VERSION`` and ``SPACK_CHECKOUT_VERSION`` that capture the version
of spack used to generate the pipeline.  While the ``SPACK_VERSION`` variable
simply contains the human-readable value produced by ``spack -V`` at pipeline
generation time, the ``SPACK_CHECKOUT_VERSION`` variable can be used in a
``git checkout`` command to make sure all child jobs checkout the same version
of spack used to generate the pipeline.  To take advantage of this, you could
simply replace ``git checkout ${SPACK_REF}`` in the example ``cloneSpack.sh``
script above with ``git checkout ${SPACK_CHECKOUT_VERSION}``.

On the other hand, if you're pointing to a spack repository and branch under your
control, there may be no benefit in using the captured ``SPACK_CHECKOUT_VERSION``,
and you can instead just clone using the project CI variables you set (in the
earlier example these were ``SPACK_REPO`` and ``SPACK_REF``).

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

Needed when binary mirror is an S3 bucket.

^^^^^^^^^^^^^^^^^^^^^
AWS_SECRET_ACCESS_KEY
^^^^^^^^^^^^^^^^^^^^^

Needed when binary mirror is an S3 bucket.

^^^^^^^^^^^^^^^
S3_ENDPOINT_URL
^^^^^^^^^^^^^^^

Needed when binary mirror is an S3 bucket that is *not* on AWS.

^^^^^^^^^^^^^^^^^
CDASH_AUTH_TOKEN
^^^^^^^^^^^^^^^^^

Needed in order to report build groups to CDash.

^^^^^^^^^^^^^^^^^
SPACK_SIGNING_KEY
^^^^^^^^^^^^^^^^^

Needed to sign/verify binary packages from the remote binary mirror.
