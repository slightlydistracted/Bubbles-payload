#!/data/data/com.termux/files/usr/bin/bash
date -s "$(curl -s --head http://google.com | grep ^Date: | sed 's/Date: //g')"
