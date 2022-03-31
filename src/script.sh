#!/bin/bash 

cd src/
timeloop-mapper arch/ARA_arch.yaml map/mapper.yaml prob/{0}.yaml -o output/ >/dev/null 2>&1
exit 1