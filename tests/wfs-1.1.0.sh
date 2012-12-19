#!/bin/bash
server='http://localhost:8080/wfs/fs_line/4.wfs?version=1.1.0'
post=''

response=$(curl --silent --write-out "\n%{http_code}\n" -d "${post}" "${server}")

status_code=$(echo "$response" | sed -n '$p')
data=$(echo "$response" | sed '$d')

case "$status_code" in
    500)
        echo $data
        exit 1
        ;;
    *)
        echo 'other: $status_code'
        ;;
esac



echo before comment
: <<'END'

END
echo after comment