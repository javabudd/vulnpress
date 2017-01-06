#!/bin/bash
set -eo pipefail

echo "net.ipv6.conf.all.disable_ipv6 = 1" >> /etc/sysctl.d/disableipv6.conf
echo "net.ipv6.conf.default.disable_ipv6 = 1" >> /etc/sysctl.d/disableipv6.conf