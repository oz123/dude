package main

import (
	"fmt"
	"regexp"
)

func main() {
	var re = regexp.MustCompile(`(?m)(?P<ebuild>[\w*-]+)-(?P<version>[\d+\.*]+)-(?P<packageversion>\d.)xpak`)
	var str = `nvidia-drivers-515.86.01-1.xpak`

	for i, match := range re.FindAllString(str, -1) {
		fmt.Println(match, "found at index", i)
	}
}
