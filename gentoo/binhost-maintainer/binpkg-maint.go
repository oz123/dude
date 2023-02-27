package _main

import (
	"fmt"
	"log"
	"os"
	"path/filepath"
	"strings"
)

var BINPKG = "/var/cache/binpkgs/x11-drivers/nvidia-drivers"

func main() {

	packages := make([]string, 2)

	versions := make(map[string]string)
	err := filepath.Walk(BINPKG,
		func(file string, info os.FileInfo, err error) error {
			if err != nil {
				return err
			}
			if info.IsDir() {
				if len(packages) >= 2 {
					fmt.Println("Latest Packages: ", packages[len(packages)-2:])
				}
				packages = packages[:0]
			} else {
				packages = append(packages, file)
				fmt.Println(file)
				package_version := strings.Split(filepath.Base(file), "-")
				versions[package_version[0]] = package_version[len(package_version)-1]
			}
			return nil
		})
	if err != nil {
		log.Println(err)
	}

	fmt.Println("Versions: ", versions)
}

// https://stackoverflow.com/questions/73318049/how-do-i-test-a-function-which-uses-filepath-walk

// when walking the directory of an ebuild we need to filter ebuild versions and keep the latest N packages
// of an ebuild

// e.g.:

// given the following directory structure:

///var/cache/binpkgs/x11-drivers/nvidia-drivers/nvidia-drivers-515.86.01-1.xpak
///var/cache/binpkgs/x11-drivers/nvidia-drivers/nvidia-drivers-515.86.01-2.xpak
///var/cache/binpkgs/x11-drivers/nvidia-drivers/nvidia-drivers-515.86.01-3.xpak
///var/cache/binpkgs/x11-drivers/nvidia-drivers/nvidia-drivers-515.86.01-4.xpak
///var/cache/binpkgs/x11-drivers/nvidia-drivers/nvidia-drivers-515.86.01-5.xpak
///var/cache/binpkgs/x11-drivers/nvidia-drivers/nvidia-drivers-515.86.01-6.xpak
///var/cache/binpkgs/x11-drivers/nvidia-drivers/nvidia-drivers-515.86.01-7.xpak
///var/cache/binpkgs/x11-drivers/nvidia-drivers/nvidia-drivers-515.86.01-8.xpak
///var/cache/binpkgs/x11-drivers/nvidia-drivers/nvidia-drivers-525.60.13-1.xpak
///var/cache/binpkgs/x11-drivers/nvidia-drivers/nvidia-drivers-525.60.13-2.xpak

// we want to keep the latest 2 versions of each ebuild:

///var/cache/binpkgs/x11-drivers/nvidia-drivers/nvidia-drivers-515.86.01-7.xpak
///var/cache/binpkgs/x11-drivers/nvidia-drivers/nvidia-drivers-515.86.01-8.xpak
///var/cache/binpkgs/x11-drivers/nvidia-drivers/nvidia-drivers-525.60.13-1.xpak
///var/cache/binpkgs/x11-drivers/nvidia-drivers/nvidia-drivers-525.60.13-2.xpak

//    var re = regexp.MustCompile(`(?m)(?P<ebuild>[\w*-]+)-(?P<version>[\d+\.*]+)-(?P<packageversion>\d.)xpak`)
