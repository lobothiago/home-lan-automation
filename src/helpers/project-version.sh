#!/usr/bin/env bash

set -eo pipefail

debug() {
  if [ ! -z ${MODULE_DEBUG} ]; then echo "$1"; fi
}

# optional
PREVIOUS=

# optional
NO_LOCAL=

usage() {
  echo "Usage: $(basename $0) [options]                             "
  echo "  -p Calculate previous version instead of current version. "
  echo "  -n No local suffix even if not in CI.                     "
  echo "  -h Display this help message.                             "
  echo "                                                            "
  echo "Calculates the version of the project.                      "
}

while getopts ":hnp" opt; do
  case "$opt" in
    h )
      usage
      exit 0
      ;;
    n ) NO_LOCAL="y";;
	  p ) PREVIOUS="y";;
		\? )
      echo "Unknown option: $OPTARG" 1>&2
      usage
  		exit 1
	    ;;
    : )
      echo "Invalid option: $OPTARG requires an argument" 1>&2
			usage
      exit 1
      ;;
  esac
done
shift $((OPTIND -1))

# looking for previous version?
if [ -n "$PREVIOUS" ]; then
  TAGS="$(git tag)"
  if [ -z "${TAGS}" ]; then
      # no tags yet
      VERSION="0.0.0"
  else
      # start at latest version tag
      VERSION="$(git describe --tags $(git rev-list --tags --max-count=1))"
  fi

  debug "previous version: $VERSION"
  echo "$VERSION"
  exit 0
fi

# running in ci or locally?
#
# this is a gitlab specific test,
# would need to be extended to support
# jenkins too
#
# calculating the version shouldn't really
# be any different between local and ci builds,
# but some reason, normal git queries when executed in a
# gitlab pipeline fail. i've attempted to switch from
# git fetch to git clone, but that doesn't solve the
# problem. instead, i've switched to a slightly different
# flow for local vs ci build version (other than a
# VERSION file already being present.
#
CI="${CI_PIPELINE_IID}"

# output: semver of build
VERSION=""

# VERSION file already exists?
if [ -f VERSION ]; then
  debug 'getting version from VERSION file...'
  VERSION="$(cat VERSION)"
else
	# not specified in VERSION so need to do
	# the calculation

	# current running branch or empty if a tag
	CURRENT=""
	if [ ! -z "$CI" ]; then
		# is CI
		if [ -z "$CI_COMMIT_TAG" ]; then
			CURRENT="$CI_COMMIT_REF_NAME"
		fi
	else
		# is local
		# get the branch name or nothing if a tag
		CURRENT="$(git symbolic-ref -q --short HEAD || echo '')"
	fi

	debug "current branch: \"$CURRENT\""

	# is tag?
	#
	#   just use the tag as it is
	#
	if [ -z "$CURRENT" ]; then
		debug 'getting version for tag...'
		VERSION="$(git describe --tags --exact-match)"
	#
	# is mainline?
	#
	#   release build - need to calculate the version
	#   based on the last tag, if any. looks for git commit
	#   log annotations specifying major, minor, patch increment,
	#   or none/skip-ci. defaults to "none" if not specified
	#   in commit logs.
	#
	elif [[ "$CURRENT" == "master" || "$CURRENT" == "main" ]]; then
		debug 'getting version for mainline...'
		TAGS="$(git tag)"
		if [ -z "${TAGS}" ]; then
			# no tags yet
			VERSION="0.0.0"
		else
			# start at latest version tag
			VERSION="$(git describe --tags $(git rev-list --tags --max-count=1))"
		fi
		debug "latest version: $VERSION"
		# need to increment major, minor, or patch
		V_BITS=(${VERSION//./ })
		V_MAJOR=${V_BITS[0]}
		V_MINOR=${V_BITS[1]}
		V_PATCH=${V_BITS[2]}
		debug "major: $V_MAJOR minor: $V_MINOR patch: $V_PATCH"
		# temp space to store last commit msg
		# to be scanned for explicit increment part
		INCREMENT_LOG=$(mktemp /tmp/gitlab-versioning.XXXXXXXXXX)
		git log -1 --pretty=%B > $INCREMENT_LOG
		debug "$INCREMENT_LOG"
		debug "$(cat $INCREMENT_LOG)"
		# which part, if any?
		if grep -Eq 'semver:(\s*)(breaking|major)' $INCREMENT_LOG; then
			debug 'major increment directive found'
			V_MAJOR=$((V_MAJOR+1))
			V_MINOR='0'
			V_PATCH='0'
		elif grep -Eq 'semver:(\s*)(feature|minor)' $INCREMENT_LOG; then
			debug 'minor increment directive found'
			V_MINOR=$((V_MINOR+1))
			V_PATCH='0'
		elif grep -Eq 'semver:(\s*)(fix|patch)' $INCREMENT_LOG; then
			debug 'patch increment directive found'
			V_PATCH=$((V_PATCH+1))
		elif grep -Eq 'semver:(\s*)(none|skip[\s-]*ci)' $INCREMENT_LOG; then
			debug 'none directive found'
		fi
		# build the full string of the new version
		V_NEW="$V_MAJOR.$V_MINOR.$V_PATCH"
		# all done
		VERSION="$V_NEW"
	#
	# is branch?
	#
	#   develop build - need to calulate the version:
	#
	#     [semver]-[branch]-[commit]
	#
	#   semver is the semantic version of the closest tag,
	#   if any.
	#
	#   branch is a normalized version of branch name.
	#   things like `/` are replaced with `-`, etc.
	#
	#   commit is the commit sha.
	#
	else
		debug 'getting version for branch...'
		TAGS="$(git tag)"
		if [ -z "${TAGS}" ]; then
			# no tags yet
			VERSION="0.0.0"
		else
			# use closest tag
			VERSION="$(git describe --always --tags --long --dirty | sed 's/-.*//g')"
			if [ -z "$VERSION" ] || [[ ! "$VERSION" =~ [0-9]*\.[0-9]*\.[0-9]* ]]; then
				VERSION='0.0.0'
			fi
		fi
		# suffix version w/ branch and sha (REF_SLUG and SHA respectively)
		REF_SLUG=''
		if [ ! -z "$CI" ]; then
			REF_SLUG="$CI_COMMIT_REF_SLUG"
		else
			REF_SLUG="$(git rev-parse --abbrev-ref HEAD | sed 's/[\/_]/-/g')"
		fi
		COMMIT_SHA="$(git rev-parse HEAD)"
		VERSION="$VERSION-${REF_SLUG}-${COMMIT_SHA}"
	fi
fi

# if build happening NOT in CI, ie locally, tack on
# a local suffix - minimizes unintended overwrites
if [[ -z "$CI" && -z "$NO_LOCAL" ]]; then
  debug 'local build'
  VERSION="${VERSION}-local"
fi

debug "calced version: $VERSION"
echo "$VERSION"
