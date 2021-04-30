% Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
% Spack Project Developers. See the top-level COPYRIGHT file for details.
%
% SPDX-License-Identifier: (Apache-2.0 OR MIT)

%=============================================================================-
% Display Results
%
% This section determines what parts of the model are printed at the end
%==============================================================================

% Spec-related functions.
% Used to build the result of the solve.
#show node/1.
#show depends_on/3.
#show version/2.
#show variant_value/3.
#show node_platform/2.
#show node_os/2.
#show node_target/2.
#show node_compiler/2.
#show node_compiler_version/3.
#show node_flag/3.
#show node_flag_compiler_default/1.
#show node_flag_source/2.
#show no_flags/2.
#show external_spec_selected/2.

% names of optimization criteria
#show opt_criterion/2.
