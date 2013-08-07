#!/usr/bin/env sh

CHASSINAT=/Users/ssp/Downloads/edfu/Chassinat/


for nr in $(seq 5 8); do
	sh -c "echo '<images>\n<volume>$nr</volume>'; cd $CHASSINAT; ls -1 $nr* | sed -e 's_\(.*\)_<image>\1</image>_g'; echo '</images>';" >  pages$nr.xml
done
