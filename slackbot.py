#!/bin/zsh
function json_escape(){
	echo -n "$1" | python -c 'import json,sys; print json.dumps(sys.stdin.read())'
}
function json_escape_file() {
	cat $1 | python -c 'import json,sys; print json.dumps(sys.stdin.read())'
}

SLACK_URL="https://hooks.slack.com/services/bla/bla/bla"

if [[ -t 0 ]]; then

	while True; do
		read -r MESSAGE &&
		echo -n "sending..." &&
		PAYLOAD="payload={\"text\": $(json_escape $MESSAGE), \"channel\": \"#$2\", \"username\": \"$1\", \"icon_emoji\": \"$3\"}" &&
		curl -X POST --data-urlencode "$PAYLOAD" $SLACK_URL &&
		echo
	done

else

	echo -n "sending..." &&
	PAYLOAD="payload={\"text\": $(json_escape_file /dev/stdin), \"channel\": \"#$2\", \"username\": \"$1\", \"icon_emoji\": \"$3\"}" &&
	curl -X POST --data-urlencode "$PAYLOAD" $SLACK_URL &&
	echo

fi
