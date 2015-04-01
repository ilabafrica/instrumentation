#!/bin/bash
stty -F /dev/ttyS0 19200 parenb
cat /dev/ttyS0 >| /var/www/celtac/celtac-results.txt
