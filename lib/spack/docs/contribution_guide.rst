.. Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
   Spack Project Developers. See the top-level COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. _contribution-guide:

==================
Contribution Guide
==================

This guide is intended for developers or administrators who want to
contribute a new package, feature, or bugfix to Spack.
It assumes that you have at least some familiarity with Git VCS and Github.
The guide will show a few examples of contributing workflows and discuss
the granularity of pull-requests (PRs). It will also discuss the tests your
PR must pass in order to be accepted into Spack.

First, what is a PR? Quoting `Bitbucket's tutorials <https://www.atlassian.com/git/tutorials/making-a-pull-request/>`_:

  Pull requests are a mechanism for a developer to notify team members that
  they have **completed a feature**. The pull request is more than just a
  notification—it’s a dedicated forum for discussing the proposed feature.

Important is **completed feature**. The changes one proposes in a PR should
correspond to one feature/bugfix/extension/etc. One can create PRs with
changes relevant to different ideas, however reviewing such PRs becomes tedious
and error prone. If possible, try to follow the **one-PR-one-package/feature** rule.

--------
Branches
--------

Spack's ``develop`` branch has the latest contributions. Nearly all pull
requests should start from ``develop`` and target ``develop``.

There is a branch for each major release series. Release branches
originate from ``develop`` and have tags for each point release in the
series. For example, ``releases/v0.14`` has tags for ``0.14.0``,
``0.14.1``, ``0.14.2``, etc. versions of Spack. We backport important bug
fixes to these branches, but we do not advance the package versions or
make other changes that would change the way Spack concretizes
dependencies. Currently, the maintainers manage these branches by
cherry-picking from ``develop``. See :ref:`releases` for more
information.

----------------------
Continuous Integration
----------------------

Spack uses `Github Actions <https://docs.github.com/en/actions>`_ for Continuous Integration
testing. This means that every time you submit a pull request, a series of tests will
be run to make sure you didn't accidentally introduce any bugs into Spack. **Your PR
will not be accepted until it passes all of these tests.** While you can certainly wait
for the results of these tests after submitting a PR, we recommend that you run them
locally to speed up the review process.

.. note::

   Oftentimes, CI will fail for reasons other than a problem with your PR.
   For example, apt-get, pip, or homebrew will fail to download one of the
   dependencies for the test suite, or a transient bug will cause the unit tests
   to timeout. If any job fails, click the "Details" link and click on the test(s)
   that is failing. If it doesn't look like it is failing for reasons related to
   your PR, you have two options. If you have write permissions for the Spack
   repository, you should see a "Restart workflow" button on the right-hand side. If
   not, you can close and reopen your PR to rerun all of the tests. If the same
   test keeps failing, there may be a problem with your PR. If you notice that
   every recent PR is failing with the same error message, it may be that an issue
   occurred with the CI infrastructure or one of Spack's dependencies put out a
   new release that is causing problems. If this is the case, please file an issue.


We currently test against Python 2.7 and 3.6-3.10 on both macOS and Linux and
perform 3 types of tests:

.. _cmd-spack-unit-test:

^^^^^^^^^^
Unit Tests
^^^^^^^^^^

Unit tests ensure that core Spack features like fetching or spec resolution are
working as expected. If your PR only adds new packages or modifies existing ones,
there's very little chance that your changes could cause the unit tests to fail.
However, if you make changes to Spack's core libraries, you should run the unit
tests to make sure you didn't break anything.

Since they test things like fetching from VCS repos, the unit tests require
`git <https://git-scm.com/>`_, `mercurial <https://www.mercurial-scm.org/>`_,
and `subversion <https://subversion.apache.org/>`_ to run. Make sure these are
installed on your system and can be found in your ``PATH``. All of these can be
installed with Spack or with your system package manager.

To run *all* of the unit tests, use:

.. code-block:: console

   $ spack unit-test

These tests may take several minutes to complete. If you know you are
only modifying a single Spack feature, you can run subsets of tests at a
time.  For example, this would run all the tests in
``lib/spack/spack/test/architecture.py``:

.. code-block:: console

   $ spack unit-test lib/spack/spack/test/architecture.py

And this would run the ``test_platform`` test from that file:

.. code-block:: console

   $ spack unit-test lib/spack/spack/test/architecture.py::test_platform

This allows you to develop iteratively: make a change, test that change,
make another change, test that change, etc.  We use `pytest
<http://pytest.org/>`_ as our tests framework, and these types of
arguments are just passed to the ``pytest`` command underneath. See `the
pytest docs
<https://doc.pytest.org/en/latest/how-to/usage.html#specifying-which-tests-to-run>`_
for more details on test selection syntax.

``spack unit-test`` has a few special options that can help you
understand what tests are available.  To get a list of all available
unit test files, run:

.. command-output:: spack unit-test --list
   :ellipsis: 5

To see a more detailed list of available unit tests, use ``spack
unit-test --list-long``:

.. command-output:: spack unit-test --list-long
   :ellipsis: 10

And to see the fully qualified names of all tests, use ``--list-names``:

.. command-output:: spack unit-test --list-names
   :ellipsis: 5

You can combine these with ``pytest`` arguments to restrict which tests
you want to know about.  For example, to see just the tests in
``architecture.py``:

.. command-output:: spack unit-test --list-long lib/spack/spack/test/architecture.py

You can also combine any of these options with a ``pytest`` keyword
search.  See the `pytest usage docs
<https://doc.pytest.org/en/latest/how-to/usage.html#specifying-which-tests-to-run>`_
for more details on test selection syntax. For example, to see the names of all tests that have "spec"
or "concretize" somewhere in their names:

.. command-output:: spack unit-test --list-names -k "spec and concretize"

By default, ``pytest`` captures the output of all unit tests, and it will
print any captured output for failed tests. Sometimes it's helpful to see
your output interactively, while the tests run (e.g., if you add print
statements to a unit tests).  To see the output *live*, use the ``-s``
argument to ``pytest``:

.. code-block:: console

   $ spack unit-test -s --list-long lib/spack/spack/test/architecture.py::test_platform

Unit tests are crucial to making sure bugs aren't introduced into
Spack. If you are modifying core Spack libraries or adding new
functionality, please add new unit tests for your feature, and consider
strengthening existing tests.  You will likely be asked to do this if you
submit a pull request to the Spack project on GitHub.  Check out the
`pytest docs <http://pytest.org/>`_ and feel free to ask for guidance on
how to write tests!

.. note::

   You may notice the ``share/spack/qa/run-unit-tests`` script in the
   repository.  This script is designed for CI.  It runs the unit
   tests and reports coverage statistics back to Codecov. If you want to
   run the unit tests yourself, we suggest you use ``spack unit-test``.

^^^^^^^^^^^^
Style Tests
^^^^^^^^^^^^

Spack uses `Flake8 <http://flake8.pycqa.org/en/latest/>`_ to test for
`PEP 8 <https://www.python.org/dev/peps/pep-0008/>`_ conformance and
`mypy <https://mypy.readthedocs.io/en/stable/>` for type checking. PEP 8 is
a series of style guides for Python that provide suggestions for everything
from variable naming to indentation. In order to limit the number of PRs that
were mostly style changes, we decided to enforce PEP 8 conformance. Your PR
needs to comply with PEP 8 in order to be accepted, and if it modifies the
spack library it needs to successfully type-check with mypy as well.

Testing for compliance with spack's style is easy. Simply run the ``spack style``
command:

.. code-block:: console

   $ spack style

``spack style`` has a couple advantages over running the tools by hand:

#. It only tests files that you have modified since branching off of
   ``develop``.

#. It works regardless of what directory you are in.

#. It automatically adds approved exemptions from the ``flake8``
   checks. For example, URLs are often longer than 80 characters, so we
   exempt them from line length checks. We also exempt lines that start
   with "homepage", "url", "version", "variant", "depends_on", and
   "extends" in ``package.py`` files.  This is now also possible when directly
   running flake8 if you can use the ``spack`` formatter plugin included with
   spack.

More approved flake8 exemptions can be found
`here <https://github.com/spack/spack/blob/develop/.flake8>`_.

If all is well, you'll see something like this:

.. code-block:: console

   $ run-flake8-tests
   Dependencies found.
   =======================================================
   flake8: running flake8 code checks on spack.

   Modified files:

     var/spack/repos/builtin/packages/hdf5/package.py
     var/spack/repos/builtin/packages/hdf/package.py
     var/spack/repos/builtin/packages/netcdf/package.py
   =======================================================
   Flake8 checks were clean.

However, if you aren't compliant with PEP 8, flake8 will complain:

.. code-block:: console

   var/spack/repos/builtin/packages/netcdf/package.py:26: [F401] 'os' imported but unused
   var/spack/repos/builtin/packages/netcdf/package.py:61: [E303] too many blank lines (2)
   var/spack/repos/builtin/packages/netcdf/package.py:106: [E501] line too long (92 > 79 characters)
   Flake8 found errors.

Most of the error messages are straightforward, but if you don't understand what
they mean, just ask questions about them when you submit your PR. The line numbers
will change if you add or delete lines, so simply run ``spack style`` again
to update them.

.. tip::

   Try fixing flake8 errors in reverse order. This eliminates the need for
   multiple runs of ``spack style`` just to re-compute line numbers and
   makes it much easier to fix errors directly off of the CI output.


^^^^^^^^^^^^^^^^^^^
Documentation Tests
^^^^^^^^^^^^^^^^^^^

Spack uses `Sphinx <http://www.sphinx-doc.org/en/stable/>`_ to build its
documentation. In order to prevent things like broken links and missing imports,
we added documentation tests that build the documentation and fail if there
are any warning or error messages.

Building the documentation requires several dependencies:

* sphinx
* sphinxcontrib-programoutput
* sphinx-rtd-theme
* graphviz
* git
* mercurial
* subversion

All of these can be installed with Spack, e.g.

.. code-block:: console

   $ spack install py-sphinx py-sphinxcontrib-programoutput py-sphinx-rtd-theme graphviz git mercurial subversion

.. warning::

   Sphinx has `several required dependencies <https://github.com/spack/spack/blob/develop/var/spack/repos/builtin/packages/py-sphinx/package.py>`_.
   If you're using a ``python`` from Spack and you installed
   ``py-sphinx`` and friends, you need to make them available to your
   ``python``. The easiest way to do this is to run:

   .. code-block:: console

      $ spack load py-sphinx py-sphinx-rtd-theme py-sphinxcontrib-programoutput

   so that all of the dependencies are added to PYTHONPATH.  If you see an error message
   like:

   .. code-block:: console

      Extension error:
      Could not import extension sphinxcontrib.programoutput (exception: No module named sphinxcontrib.programoutput)
      make: *** [html] Error 1

   that means Sphinx couldn't find ``py-sphinxcontrib-programoutput`` in your
   ``PYTHONPATH``.

Once all of the dependencies are installed, you can try building the documentation:

.. code-block:: console

   $ cd path/to/spack/lib/spack/docs/
   $ make clean
   $ make

If you see any warning or error messages, you will have to correct those before your PR
is accepted. If you are editing the documentation, you should be running the
documentation tests to make sure there are no errors. Documentation changes can result
in some obfuscated warning messages. If you don't understand what they mean, feel free
to ask when you submit your PR.

.. _spack-builders-and-pipelines:

^^^^^^^^^
GitLab CI
^^^^^^^^^

""""""""""""""""""
Build Cache Stacks
""""""""""""""""""

Spack welcomes the contribution of software stacks of interest to the community. These
stacks are used to test package recipes and generate publicly available build caches.
Spack uses GitLab CI for managing the orchestration of build jobs.

GitLab Entry Point
~~~~~~~~~~~~~~~~~~

Add stack entrypoint to the ``share/spack/gitlab/cloud_pipelines/.gitlab-ci.yml``. There
are two stages required for each new stack, the generation stage and the build stage.

The generate stage is defined using the job template ``.generate`` configured with
environment variables defining the name of the stack in ``SPACK_CI_STACK_NAME`` and the
platform (``SPACK_TARGET_PLATFORM``) and architecture (``SPACK_TARGET_ARCH``) configuration,
and the tags associated with the class of runners to build on.

.. note::

    The ``SPACK_CI_STACK_NAME`` must match the name of the directory containing the
    stacks ``spack.yaml``.


.. note::

    The platform and architecture variables are specified in order to select the
    correct configurations from the generic configurations used in Spack CI. The
    configurations currently available are:

    * ``.cray_rhel_zen4``
    * ``.cray_sles_zen4``
    * ``.darwin_aarch64``
    * ``.darwin_x86_64``
    * ``.linux_aarch64``
    * ``.linux_icelake``
    * ``.linux_neoverse_n1``
    * ``.linux_neoverse_v1``
    * ``.linux_neoverse_v2``
    * ``.linux_power``
    * ``.linux_skylake``
    * ``.linux_x86_64``
    * ``.linux_x86_64_v4``

    New configurations can be added to accommodate new platforms and architectures.


The build stage is defined as a trigger job that consumes the GitLab CI pipeline generated in
the generate stage for this stack. Build stage jobs use the ``.build`` job template which
handles the basic configuration.

An example entry point for a new stack called ``my-super-cool-stack``

.. code-block:: yaml

    .my-super-cool-stack:
      extends: [ ".linux_x86_64_v3" ]
      variables:
        SPACK_CI_STACK_NAME: my-super-cool-stack
        tags: [ "all", "tags", "your", "job", "needs"]

    my-super-cool-stack-generate:
      extends: [ ".generate", ".my-super-cool-stack" ]
      image: my-super-cool-stack-image:0.0.1

    my-super-cool-stack-build:
      extends: [ ".build", ".my-super-cool-stack" ]
      trigger:
        include:
          - artifact: jobs_scratch_dir/cloud-ci-pipeline.yml
            job: my-super-cool-stack-generate
        strategy: depend
      needs:
        - artifacts: True
          job: my-super-cool-stack-generate


Stack Configuration
~~~~~~~~~~~~~~~~~~~

The stack configuration is a spack environment file with two additional sections added.
Stack configurations should be located in ``share/spack/gitlab/cloud_pipelines/stacks/<stack_name>/spack.yaml``.

The ``ci`` section is generally used to define stack specific mappings such as image or tags.
For more information on what can go into the ``ci`` section refer to the docs on pipelines.

The ``cdash`` section is used for defining where to upload the results of builds. Spack configures
most of the details for posting pipeline results to
`cdash.spack.io <https://cdash.spack.io/index.php?project=Spack+Testing>`_. The only
requirement in the stack configuration is to define a ``build-group`` that is unique,
this is usually the long name of the stack.

An example stack that builds ``zlib``.

.. code-block:: yaml

    spack:
      view: false
      packages:
        all:
          require: ["%gcc", "target=x86_64_v3"]
      specs:
      - zlib

      ci:
        pipeline-gen
        - build-job:
            image: my-super-cool-stack-image:0.0.1

      cdash:
        build-group: My Super Cool Stack

.. note::

    The ``image`` used in the ``*-generate`` job must match exactly the ``image`` used in the ``build-job``.
    When the images do not match the build job may fail.


"""""""""""""""""""
Registering Runners
"""""""""""""""""""

Contributing computational resources to Spack's CI build farm is one way to help expand the
capabilities and offerings of the public Spack build caches. Currently, Spack utilizes linux runners
from AWS, Google, and the University of Oregon (UO).

Runners require three key peices:
* Runner Registration Token
* Accurate tags
* OIDC Authentication script
* GPG keys


Minimum GitLab Runner Version: ``16.1.0``
`Intallation instructions <https://docs.gitlab.com/runner/install/>`_

Registration Token
~~~~~~~~~~~~~~~~~~

The first step to contribute new runners is to open an issue in the `spack infrastructure <https://github.com/spack/spack-infrastructure/issues/new?assignees=&labels=runner-registration&projects=&template=runner_registration.yml>`_
project. This will be reported to the spack infrastructure team who will guide users through the process
of registering new runners for Spack CI.

The information needed to register a runner is the motivation for the new resources, a semi-detailed description of
the runner, and finallly the point of contact for maintaining the software on the runner.

The point of contact will then work with the infrastruture team to obtain runner registration token(s) for interacting with
with Spack's GitLab instance. Once the runner is active, this point of contact will also be responsible for updating the
GitLab runner software to keep pace with Spack's Gitlab.

Tagging
~~~~~~~

In the initial stages of runner registration it is important to **exclude** the special tag ``spack``. This will prevent
the new runner(s) from being picked up for production CI jobs while it is configured and evaluated. Once it is determined
that the runner is ready for production use the ``spack`` tag will be added.

Because gitlab has no concept of tag exclustion, runners that provide specialized resource also require specialized tags.
For example, a basic CPU only x86_64 runner may have a tag ``x86_64`` associated with it. However, a runner containing an
CUDA capable GPU may have the tag ``x86_64-cuda`` to denote that it should only be used for packages that will benefit from
a CUDA capable resource.

OIDC
~~~~

Spack runners use OIDC authentication for connecting to the appropriate AWS bucket
which is used for coordinating the communication of binaries between build jobs. In
order to configure OIDC authentication, Spack CI runners use a python script with minimal
dependencies. This script can be configured for runners as seen here using the ``pre_build_script``.

.. code-block:: toml

    [[runners]]
      pre_build_script = """
      echo 'Executing Spack pre-build setup script'

      for cmd in "${PY3:-}" python3 python; do
        if command -v > /dev/null "$cmd"; then
          export PY3="$(command -v "$cmd")"
          break
        fi
      done

      if [ -z "${PY3:-}" ]; then
        echo "Unable to find python3 executable"
        exit 1
      fi

      $PY3 -c "import urllib.request;urllib.request.urlretrieve('https://raw.githubusercontent.com/spack/spack-infrastructure/main/scripts/gitlab_runner_pre_build/pre_build.py', 'pre_build.py')"
      $PY3 pre_build.py > envvars

      . ./envvars
      rm -f envvars
      unset GITLAB_OIDC_TOKEN
      """

GPG Keys
~~~~~~~~

Runners that may be utilized for ``protected`` CI require the registration of an intermediate signing key that
can be used to sign packages. For more information on package signing read :ref:`key_architecture`.

--------
Coverage
--------

Spack uses `Codecov <https://codecov.io/>`_ to generate and report unit test
coverage. This helps us tell what percentage of lines of code in Spack are
covered by unit tests. Although code covered by unit tests can still contain
bugs, it is much less error prone than code that is not covered by unit tests.

Codecov provides `browser extensions <https://github.com/codecov/sourcegraph-codecov>`_
for Google Chrome and Firefox. These extensions integrate with GitHub
and allow you to see coverage line-by-line when viewing the Spack repository.
If you are new to Spack, a great way to get started is to write unit tests to
increase coverage!

Unlike with CI on Github Actions Codecov tests are not required to pass in order for your
PR to be merged. If you modify core Spack libraries, we would greatly
appreciate unit tests that cover these changed lines. Otherwise, we have no
way of knowing whether or not your changes introduce a bug. If you make
substantial changes to the core, we may request unit tests to increase coverage.

.. note::

   If the only files you modified are package files, we do not care about
   coverage on your PR. You may notice that the Codecov tests fail even though
   you didn't modify any core files. This means that Spack's overall coverage
   has increased since you branched off of develop. This is a good thing!
   If you really want to get the Codecov tests to pass, you can rebase off of
   the latest develop, but again, this is not required.


-------------
Git Workflows
-------------

Spack is still in the beta stages of development. Most of our users run off of
the develop branch, and fixes and new features are constantly being merged. So
how do you keep up-to-date with upstream while maintaining your own local
differences and contributing PRs to Spack?

^^^^^^^^^
Branching
^^^^^^^^^

The easiest way to contribute a pull request is to make all of your changes on
new branches. Make sure your ``develop`` is up-to-date and create a new branch
off of it:

.. code-block:: console

   $ git checkout develop
   $ git pull upstream develop
   $ git branch <descriptive_branch_name>
   $ git checkout <descriptive_branch_name>

Here we assume that the local ``develop`` branch tracks the upstream develop
branch of Spack. This is not a requirement and you could also do the same with
remote branches. But for some it is more convenient to have a local branch that
tracks upstream.

Normally we prefer that commits pertaining to a package ``<package-name>`` have
a message ``<package-name>: descriptive message``. It is important to add
descriptive message so that others, who might be looking at your changes later
(in a year or maybe two), would understand the rationale behind them.

Now, you can make your changes while keeping the ``develop`` branch pure.
Edit a few files and commit them by running:

.. code-block:: console

   $ git add <files_to_be_part_of_the_commit>
   $ git commit --message <descriptive_message_of_this_particular_commit>

Next, push it to your remote fork and create a PR:

.. code-block:: console

   $ git push origin <descriptive_branch_name> --set-upstream

GitHub provides a `tutorial <https://help.github.com/articles/about-pull-requests/>`_
on how to file a pull request. When you send the request, make ``develop`` the
destination branch.

If you need this change immediately and don't have time to wait for your PR to
be merged, you can always work on this branch. But if you have multiple PRs,
another option is to maintain a Frankenstein branch that combines all of your
other branches:

.. code-block:: console

   $ git co develop
   $ git branch <your_modified_develop_branch>
   $ git checkout <your_modified_develop_branch>
   $ git merge <descriptive_branch_name>

This can be done with each new PR you submit. Just make sure to keep this local
branch up-to-date with upstream ``develop`` too.

^^^^^^^^^^^^^^
Cherry-Picking
^^^^^^^^^^^^^^

What if you made some changes to your local modified develop branch and already
committed them, but later decided to contribute them to Spack? You can use
cherry-picking to create a new branch with only these commits.

First, check out your local modified develop branch:

.. code-block:: console

   $ git checkout <your_modified_develop_branch>

Now, get the hashes of the commits you want from the output of:

.. code-block:: console

   $ git log

Next, create a new branch off of upstream ``develop`` and copy the commits
that you want in your PR:

.. code-block:: console

   $ git checkout develop
   $ git pull upstream develop
   $ git branch <descriptive_branch_name>
   $ git checkout <descriptive_branch_name>
   $ git cherry-pick <hash>
   $ git push origin <descriptive_branch_name> --set-upstream

Now you can create a PR from the web-interface of GitHub. The net result is as
follows:

#. You patched your local version of Spack and can use it further.
#. You "cherry-picked" these changes in a stand-alone branch and submitted it
   as a PR upstream.

Should you have several commits to contribute, you could follow the same
procedure by getting hashes of all of them and cherry-picking to the PR branch.

.. note::

   It is important that whenever you change something that might be of
   importance upstream, create a pull request as soon as possible. Do not wait
   for weeks/months to do this, because:

   #. you might forget why you modified certain files
   #. it could get difficult to isolate this change into a stand-alone clean PR.

^^^^^^^^
Rebasing
^^^^^^^^

Other developers are constantly making contributions to Spack, possibly on the
same files that your PR changed. If their PR is merged before yours, it can
create a merge conflict. This means that your PR can no longer be automatically
merged without a chance of breaking your changes. In this case, you will be
asked to rebase on top of the latest upstream ``develop``.

First, make sure your develop branch is up-to-date:

.. code-block:: console

   $ git checkout develop
   $ git pull upstream develop

Now, we need to switch to the branch you submitted for your PR and rebase it
on top of develop:

.. code-block:: console

   $ git checkout <descriptive_branch_name>
   $ git rebase develop

Git will likely ask you to resolve conflicts. Edit the file that it says can't
be merged automatically and resolve the conflict. Then, run:

.. code-block:: console

   $ git add <file_that_could_not_be_merged>
   $ git rebase --continue

You may have to repeat this process multiple times until all conflicts are resolved.
Once this is done, simply force push your rebased branch to your remote fork:

.. code-block:: console

   $ git push --force origin <descriptive_branch_name>

^^^^^^^^^^^^^^^^^^^^^^^^^
Rebasing with cherry-pick
^^^^^^^^^^^^^^^^^^^^^^^^^

You can also perform a rebase using ``cherry-pick``. First, create a temporary
backup branch:

.. code-block:: console

   $ git checkout <descriptive_branch_name>
   $ git branch tmp

If anything goes wrong, you can always go back to your ``tmp`` branch.
Now, look at the logs and save the hashes of any commits you would like to keep:

.. code-block:: console

   $ git log

Next, go back to the original branch and reset it to ``develop``.
Before doing so, make sure that you local ``develop`` branch is up-to-date
with upstream:

.. code-block:: console

   $ git checkout develop
   $ git pull upstream develop
   $ git checkout <descriptive_branch_name>
   $ git reset --hard develop

Now you can cherry-pick relevant commits:

.. code-block:: console

   $ git cherry-pick <hash1>
   $ git cherry-pick <hash2>

Push the modified branch to your fork:

.. code-block:: console

   $ git push --force origin <descriptive_branch_name>

If everything looks good, delete the backup branch:

.. code-block:: console

   $ git branch --delete --force tmp

^^^^^^^^^^^^^^^^^^
Re-writing History
^^^^^^^^^^^^^^^^^^

Sometimes you may end up on a branch that has diverged so much from develop
that it cannot easily be rebased. If the current commits history is more of
an experimental nature and only the net result is important, you may rewrite
the history.

First, merge upstream ``develop`` and reset you branch to it. On the branch
in question, run:

.. code-block:: console

   $ git merge develop
   $ git reset develop

At this point your branch will point to the same commit as develop and
thereby the two are indistinguishable. However, all the files that were
previously modified will stay as such. In other words, you do not lose the
changes you made. Changes can be reviewed by looking at diffs:

.. code-block:: console

   $ git status
   $ git diff

The next step is to rewrite the history by adding files and creating commits:

.. code-block:: console

   $ git add <files_to_be_part_of_commit>
   $ git commit --message <descriptive_message>

After all changed files are committed, you can push the branch to your fork
and create a PR:

.. code-block:: console

   $ git push origin --set-upstream
