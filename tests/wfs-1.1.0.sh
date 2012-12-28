#!/bin/bash
: <<'END'
server='http://localhost:8080/wfs/fs_line/4.wfs?version=1.1.0'
filter=''
post=''
END




server='http://localhost:8080/?service=WFS&request=GetFeature&version=1.1.0&typeName=fs_polygon,fs_line&outputFormat=WFS&filter='
post=''
filter=$(cat <<EOF
(
<Filter>
    <BBOX>
        <PropertyName>geometry</PropertyName>
        <Envelope srsName="EPSG:4326">
            <lowerCorner>1.7969082858066 44.555248132086</lowerCorner>
            <upperCorner>14.650912192056 49.065808099499</upperCorner>
        </Envelope>
    </BBOX>
</Filter>)
(<Filter>
    <BBOX>
        <PropertyName>geometry</PropertyName>
        <Envelope srsName="EPSG:4326">
            <lowerCorner>1.7969082858066 044.555248132086</lowerCorner>
            <upperCorner>14.650912192056 49.065808099499</upperCorner>
        </Envelope>
    </BBOX>
</Filter>)
EOF
)









function urlencode () {
tab="`echo -en "\x9"`"
echo $tab
i="$@"
i=${i//%/%25}  ; i=${i//' '/%20} ; i=${i//$tab/%09}
i=${i//!/%21}  ; i=${i//\"/%22}  ; i=${i//#/%23}
i=${i//\$/%24} ; i=${i//\&/%26}  ; i=${i//\'/%27}
i=${i//(/%28}  ; i=${i//)/%29}   ; i=${i//\*/%2a}
i=${i//+/%2b}  ; i=${i//,/%2c}   ; i=${i//-/%2d}
i=${i//\./%2e} ; i=${i//\//%2f}  ; i=${i//:/%3a}
i=${i//;/%3b}  ; i=${i//</%3c}   ; i=${i//=/%3d}
i=${i//>/%3e}  ; i=${i//\?/%3f}  ; i=${i//@/%40}
i=${i//\[/%5b} ; i=${i//\\/%5c}  ; i=${i//\]/%5d}
i=${i//\^/%5e} ; i=${i//_/%5f}   ; i=${i//\~/%7e}
i=${i//\{/%7b} ; i=${i//|/%7c}   ; i=${i//\}/%7d}
echo "$i"
i=""
}




filter=$(echo $filter | tr -d '\n')
filter=$(urlencode $filter)
url=$(echo "${server}${filter}" | tr -d '\n')
response=$(curl --silent --write-out "\n%{http_code}\n" --data-urlencode "${post}" "${url}")

status_code=$(echo "$response" | sed -n '$p')
data=$(echo "$response" | sed '$d')

case "$status_code" in
    500)
        echo $data
        exit 1
        ;;
    *)
        echo "Status: ${status_code}"
        echo $data
        ;;
esac







