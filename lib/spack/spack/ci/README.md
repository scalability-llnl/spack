# Spack CI generators

This document describes how the ci module can be extended to provide novel
ci generators.  The module currently has only a single generator for gitlab.
The unit-tests for the ci module define a small custom generator for testing
purposes as well.

The process of generating a pipeline involves creating a ci-enabled spack
environment, activating it, and running `spack ci generate`, possibly with
arguments describing things like where the output should be written.

Internally pipeline generation is broken into two components: general and
ci platform specific.

## General pipeline functionality

General pipeline functionality includes building a pipeline graph (really,
a forest), pruning it in a variety of ways, and gathering attributes for all
the generated spec build jobs from the spack configuration.

All of the above functionality is defined in the `__init__.py` of the top-level
ci module, and should be roughly the same for pipelines generated for any
platform.

## CI platform specific functionality

Functionality specific to CI platforms (e.g. gitlab, gha, etc.) should be
defined in a dedicated module.  In order to define a generator for a new
platform, there are only a few requirements:

1. add a file under `ci` in which you define a generator method decorated with
the `@generator` attribute. .

1. import it from `lib/spack/spack/ci/__init__.py`, so that your new generator
is registered.

1. the generator method must take as arguments PipelineDag, SpackCIConfig,
and PipelineOptions objects, in that order.

1. the generator method must produce an output file containing the
generated pipeline.
