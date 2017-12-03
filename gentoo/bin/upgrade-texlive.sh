#!/bin/bash

# helper script to upgrade qt packages

set -e
set +x

INSTALLED_QT_PACKAGES=$(eix --only-names -IC dev-texlive)
echo $INSTALLED_QT_PACKAGES
quickpkg ${INSTALLED_QT_PACKAGES}
emerge -Ca ${INSTALLED_QT_PACKAGES} && emerge -av1 ${INSTALLED_QT_PACKAGES}
