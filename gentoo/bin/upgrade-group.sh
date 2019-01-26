#!/bin/bash

# helper script to upgrade package group

set -e
set +x

GROUP_NAME=$1
INSTALLED_GROUP_PACKAGES=$(eix --only-names -IC ${GROUP_NAME})
echo $INSTALLED_GROUP_PACKAGES
quickpkg ${INSTALLED_GROUP_PACKAGES}
emerge -Ca ${INSTALLED_GROUP_PACKAGES} && emerge -av1 ${INSTALLED_GROUP_PACKAGES}
