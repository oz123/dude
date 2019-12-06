"""
Script to build all bumped mate versions
"""

import subprocess as sp

packages = """
app-editors/pluma/pluma-1.23.2.ebuild
app-text/atril/atril-1.23.1.ebuild
dev-libs/libmateweather/libmateweather-1.23.0.ebuild
dev-python/python-caja/python-caja-1.23.0.ebuild
mate-base/caja/caja-1.23.2.ebuild
mate-base/libmatekbd/libmatekbd-1.23.0.ebuild
mate-base/mate-applets/mate-applets-1.23.0.ebuild
mate-base/mate-common/mate-common-1.23.3.ebuild
mate-base/mate-control-center/mate-control-center-1.23.2.ebuild
mate-base/mate-desktop/mate-desktop-1.23.2.ebuild
mate-base/mate-menus/mate-menus-1.23.0.ebuild
mate-base/mate-panel/mate-panel-1.23.2.ebuild
mate-base/mate-session-manager/mate-session-manager-1.23.0.ebuild
mate-base/mate-settings-daemon/mate-settings-daemon-1.23.2.ebuild
mate-extra/caja-dropbox/caja-dropbox-1.23.0.ebuild
mate-extra/caja-extensions/caja-extensions-1.23.0.ebuild
mate-extra/mate-calc/mate-calc-1.23.0.ebuild
mate-extra/mate-media/mate-media-1.23.1.ebuild
mate-extra/mate-polkit/mate-polkit-1.23.0.ebuild
mate-extra/mate-power-manager/mate-power-manager-1.23.1.ebuild
mate-extra/mate-screensaver/mate-screensaver-1.23.1.ebuild
mate-extra/mate-sensors-applet/mate-sensors-applet-1.23.0.ebuild
mate-extra/mate-user-guide/mate-user-guide-1.23.1.ebuild
mate-extra/mate-user-share/mate-user-share-1.23.0.ebuild
mate-extra/mate-utils/mate-utils-1.23.1.ebuild
media-gfx/eom/eom-1.23.1.ebuild
media-libs/libmatemixer/libmatemixer-1.23.0.ebuild
x11-misc/mate-notification-daemon/mate-notification-daemon-1.23.0.ebuild
x11-misc/mozo/mozo-1.23.0.ebuild
x11-terms/mate-terminal/mate-terminal-1.23.0.ebuild
x11-themes/mate-backgrounds/mate-backgrounds-1.23.0.ebuild
x11-themes/mate-icon-theme/mate-icon-theme-1.23.2.ebuild
x11-wm/marco/marco-1.23.1.ebuild
"""

for package in packages.split():
    packagedir, ebuild = package.rsplit("/", 1)
    sp.Popen("git add %s" % ebuild,cwd=packagedir, shell=True)
    sp.Popen("repoman manifest", cwd=packagedir, shell=True, stdout=sp.PIPE).wait()
    p = sp.Popen("sudo ebuild %s clean package" % ebuild, cwd=packagedir, shell=True)
    code = p.wait()
    if code:
        break
    version = ebuild.rsplit("-", 1)[-1].rsplit(".", 1)[0]
    p = sp.Popen("repoman commit -S -m \"%s: bump to version %s\"" % (packagedir, version), cwd=packagedir, shell=True)
    code = p.wait()
    if code:
        break
    input("Waiting for you to continue ...")
