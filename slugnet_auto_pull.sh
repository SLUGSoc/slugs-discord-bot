#!/bin/bash

function check_commit_id() {
	printf "Fetching master branch of remote repository...\n"
	git fetch || { printf "Unable to fetch from remote repository. Check connection with remote host.\n\n"; return; } # Fetch the most recent commit to the master branch from the remote repository
	remoteid=$(git log origin/master --format="%H" -n 1) || { printf "Unable to retrieve remote ID. Check connection with remote host.\n"; return; }
	localid=$(git log --format="%H" -n 1) || { printf "Unable to retrieve local ID. Try placing this file in a git repository.\n"; return; } # Assign the most recent commit hash from the remote and local branches to their respective variables

	if [ "$remoteid" == "$localid" ] # If the two hashes are equal, then there is no difference between remote and local repos, hence no change needs to be made
	then
		printf "Local master branch matches remote.\n\n"
		return
	else
		printf "Local master branch is behind, pulling from remote master branch...\n"
		git pull || printf "Unable to pull from remote repository. Check connection with remote host.\n" # If there is a difference, pull from the remote repository
		return
	fi
}

while [ TRUE ]; # Compares the commit IDs every 60 seconds
do
	check_commit_id
	sleep 60
done