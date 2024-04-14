set -e

# make tools scripts
HELPERS="$(dirname $0)"

# option
BUILD_META_PACKAGE=

# option
VERSION=''

usage() {
  echo "Usage: $(basename $0) [options]                              "
  echo "  -p Build meta package path for metadata module output.     "
  echo "  -v Version value to inject.                                "
  echo "  -h Display this help message.                              "
  echo "                                                             "
  echo "Creates/overwrites a Python build metadata module containing "
  echo "an 'version' attribute representing the build version.       "
}

while getopts ":hp:v:" opt; do
  case "$opt" in
    h )
      usage
      exit 0
      ;;
	  p ) BUILD_META_PACKAGE="$OPTARG";;
		v ) VERSION="$OPTARG";;
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

if [ -z "$BUILD_META_PACKAGE" ]; then
  echo "Missing -p option" 1>&2
  usage
  exit 1
fi

if [ -z "$VERSION" ]; then
  echo "Missing -v option" 1>&2
  usage
  exit 1
fi

BUILD_META_MODULE="$BUILD_META_PACKAGE/__build__.py"

echo "version = \"$VERSION\"" > $BUILD_META_MODULE
