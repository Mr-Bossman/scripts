#!/bin/bash
URL=$1
OUTPUT=$2

#grab from the headers of the page in devtools
cf_clearance="RafnfzpA7FMtDQkeq20M0Azy_G.JgKTfcND4jqRxy6M-1712285623-1.0.1.1-SI2zo5k40pfq8bMN3dJoAq7aLDgbLH57BCBDCNx8lJ49qFSllgsXHBma56pWt.Hz3hQH1fLEFKKnxeU6tbZzgQ"
user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
mirror_server="oserver"

get_ctk_cmd() {
	curl $1 -s -w "%{stderr}%{http_code}\n" -H "cookie: cf_clearance=$cf_clearance" \
		-H "user-agent: $user_agent" | grep ctk | cut -d"'" -f2
}

get_ctk() {
	{ status=$(get_ctk_cmd $1 2>&1 >&3 3>&-); } 3>&1;
	if [[ "$status" != *"200"* ]]; then
		echo -e "curl $1 \nReturned status: $status."\
			"\nDid you set the Cloudflare clearance token?" 1>&2
		exit 1
	fi
}

get_server_cmd() {
	curl "https://kissanime.com.ru/ajax/anime/load_episodes_v2?s=$mirror_server" \
  		-s -w "%{stderr}%{http_code}\n" -H "cookie: cf_clearance=$cf_clearance" \
		-H "user-agent: $user_agent" --data-raw "episode_$id&ctk=$1" | \
		sed -r -e 's/\\//g' -e 's/.*src="([^")]+).*/\1/'
}

get_server() {
	id=$(echo $1 | grep -Po "id=\\d+")
	{ status=$(get_server_cmd $id $2 2>&1 >&3 3>&-); } 3>&1;
	if [[ "$status" != *"200"* ]]; then
		echo -e "curl" \
			"https://kissanime.com.ru/ajax/anime/load_episodes_v2?s=$mirror_server"\
			"\nReturned status: $status. \nDid you set the Cloudflare clearance"\
			"token?" 1>&2
		exit 1
	fi
}

get_m3u8_cmd(){
	curl $1 -s -w "%{stderr}%{http_code}\n" -H "referer: $2" \
		| grep m3u8 | sed -r -e 's/\\//g' -e 's/.*file\":\"([^"]+).*/\1/'
}

get_m3u8() {
	{ status=$(get_m3u8_cmd $1 $2 2>&1 >&3 3>&-); } 3>&1;
	if [[ "$status" != *"200"* ]]; then
		echo -e "curl $1\nReturned status: $status. \n"\
			"Did you set the Cloudflare clearance token?" 1>&2
		exit 1
	fi
}

get_m3u8_from_url() {
	#ctk=$(get_ctk $1)
	#err=$?;if [ $err -ne 0 ]; then exit $err; fi #exit if error
	#echo $ctk
	ctk="garbage"

	server=$(get_server $1 $ctk)
	err=$?;if [ $err -ne 0 ]; then exit $err; fi #exit if error
	#echo $server

	m3u8=$(get_m3u8 $server $1)
	err=$?;if [ $err -ne 0 ]; then exit $err; fi #exit if error
	echo $m3u8
}

get_episode_list_cmd() {
	curl $1 -s -w "%{stderr}%{http_code}\n" -H "cookie: cf_clearance=$cf_clearance" \
		-H "user-agent: $user_agent" | grep $1"/Episode" | \
		sed -r -e 's/.*href="([^"]+).*/\1/'
}

get_episode_list() {
	base_url=$(echo $1 | sed -e "s/\/$//g" -e"s/\/Episode.*//g")
	{ status=$(get_episode_list_cmd $base_url 2>&1 >&3 3>&-); } 3>&1;
	if [[ "$status" != *"200"* ]]; then
		echo -e "curl $1 \nReturned status: $status."\
			"\nDid you set the Cloudflare clearance token?" 1>&2
		exit 1
	fi
}

get_episode_id(){
	list=$(get_episode_list $1)
	err=$?;if [ $err -ne 0 ]; then exit $err; fi #exit if error
	for i in $list; do
		episode=$(echo $i | grep $URL)
		if [[ "$episode" != "" ]]; then
			echo $i
			exit
		fi
	done
}

get_all_episodes(){
	list=$(get_episode_list $1)
	err=$?;if [ $err -ne 0 ]; then exit $err; fi #exit if error
	for episode in $list; do
		episode_num=$(echo $episode | grep -Po "Episode-\\d+")
		m3u8=$(get_m3u8_from_url $episode)
		err=$?;if [ $err -ne 0 ]; then exit $err; fi #exit if error
		ffmpeg -i $m3u8 -c copy $2$episode_num.mp4
	done
}

#get_all_episodes $URL $OUTPUT
#exit
episode=$(get_episode_id $URL)
err=$?;if [ $err -ne 0 ]; then exit $err; fi #exit if error
m3u8=$(get_m3u8_from_url $episode)
err=$?;if [ $err -ne 0 ]; then exit $err; fi #exit if error
ffmpeg -i $m3u8 -c copy $OUTPUT
