#! /bin/bash
printf '%s\n' "$(date) ${BASH_SOURCE[0]}"

export tpl="openmpi"
export versions="3.1.3 3.1.2 3.1.1 3.1.0 3.0.3 3.0.2 3.0.1 3.0.0 2.1.5 2.1.4 2.1.3 2.1.2 2.1.1 2.1.0"
export arch=$(spack arch)

for v in ${versions}; do
    echo ""
    echo "spack install ${tpl} @ ${v} % ${gcc_system_compiler} arch=${arch}"
          spack install ${tpl} @ ${v} % ${gcc_system_compiler} arch=${arch}

          spack clean --all
done

date

