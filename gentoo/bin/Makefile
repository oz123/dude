.PHONY: install clean uninstall
PREFIX ?= /
DEST ?= ${PREFIX}usr/local/bin/

PROGRAMS = "pkg-kernel.sh" \
	   "clean-kernel.sh" \
	   "pkg_version" \
	   "run-in-chroot.sh" \
	   "tar-snapshot.sh" \
	   "upgrade-kernel.sh"


install: $(PROGRAMS)

define PROGRAM_template =
 	$(1): $$($(1))
		install -m 755 -o root -g root $(1) $(DEST)
endef

$(foreach prog,$(PROGRAMS),$(eval $(call PROGRAM_template,$(prog))))

uninstall: clean

clean:
	@$(foreach p,$(PROGRAMS), echo removing $(p) $(shell rm -fv $(DEST)$(p));)
