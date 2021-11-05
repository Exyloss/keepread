#!/bin/sh
echo "$1" | sed 's/.*secret=\([^&]*\).*/\1/' | awk -F '%' '{print $1}' | mintotp 2>/dev/null
