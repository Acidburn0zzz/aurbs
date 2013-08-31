- pacman -S devtools rsync python-setuptools python-simplejson python-yaml python-pymongo python-flask pyalpm
- yaourt -S python-flup-hg
- run `make install`
- set PACKAGER in `/etc/makepkg.conf`
- modify `/etc/aurbs.yml` to define you pkgs and archs
- make sure that mongodb is running
- run `aurbs.py` to build pkgs


For the UI:
- for better performance configure your webserver to allow x-sendfile or manually serve
  /var/lib/aurbs/aurstaging to /aurstaging
- same reason, for the public repo: if you want to serve it on another url, specify that url in config
- sample config for lighttpd: `templates/lighttpd.conf.sample`
