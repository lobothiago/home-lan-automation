
set -e
# trap 'catch' ERR

# catch() {
#   rm .dockerignore
# }

# make tools scripts
HELPERS="$(dirname $0)"

# running in ci
CI="${CI_PIPELINE_IID:-}"

# option
DOCKERFILE=

# option
TAG=''

# option
LATEST=''

# option
BUILD_ARGS=''

# option
IMAGE_PATH=''

# option
IGNORE_PATH=''

# optional
REGISTRY="${REGISTRY:-registry.gitlab.com}"

# optional
OUT_DIR="${OUT_DIR:-dist}"

usage() {
  echo "Usage: $(basename $0) [options]                                  "
  echo "  -f \`Dockerfile\` path.                                        "
  echo "  -h Display this help message.                                  "
  echo "  -o Build output directory.                                     "
  echo "  -r Container registry.                                         "
  echo "  -p Image path in registry.                                     "
  echo "  -t Image tag.                                                  "
  echo "  -l Publish as latest.                                          "
  echo "  -a Build arg. May be specified multiple times.                 "
  echo "  -i Path to Docker Ignore.                 "
  echo "                                                                 "
  echo "Builds the specified image using Docker (with BuildKit).         "
  echo "                                                                 "
  echo "Default registry:                                                "
  echo "                                                                 "
  echo "  $REGISTRY"
  echo "                                                                 "
  echo "Use \`-r\` to override registry. CI supplies the appropriate     "
  echo "registry credentials automatically. For non-CI usage,            "
  echo "specify REGISTRY_USER and REGISTRY_PASSWORD env vars.            "
}

while getopts ":hlf:t:r:n:p:o:a:i:" opt; do
  case "$opt" in
    h )
      usage
      exit 0
      ;;
	  f ) DOCKERFILE="$OPTARG";;
		t ) TAG="$OPTARG";;
    l ) LATEST="latest";;
    a ) BUILD_ARGS="$BUILD_ARGS --build-arg $OPTARG";;
    r ) REGISTRY="$OPTARG";;
    p ) IMAGE_PATH="$OPTARG";;
    o ) OUT_DIR="$OPTARG";;
    i ) IGNORE_PATH="$OPTARG";;
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

if [ -z "$DOCKERFILE" ]; then
  echo "Missing -f option" 1>&2
  usage
  exit 1
fi

if [ -z "$TAG" ]; then
  echo "Missing -t option" 1>&2
  usage
  exit 1
fi

if [ -z "$IMAGE_PATH" ]; then
  echo "Missing -p option" 1>&2
  usage
  exit 1
fi

if ! command -v docker >/dev/null 2>&1; then
  echo 'docker not found' 1>&2
  echo "PATH: $PATH" 1>&2
  exit 1
fi

# namespace of image
NS="$REGISTRY/$IMAGE_PATH"

if [ -n "$IGNORE_PATH" ]; then
  cp $IGNORE_PATH .dockerignore
fi
# version or latest tag?
if [ -n "$LATEST" ]; then
  if [ -n "$CI" ]; then
    docker pull "$NS:$TAG"
  fi

  docker tag "$NS:$TAG" "$NS:latest"

  if [ -n "$CI" ]; then
    docker push "$NS:latest"
  fi
else
  DOCKER_BUILDKIT=1 docker build $BUILD_ARGS --build-arg BUILDKIT_INLINE_CACHE=1 \
    --tag "$NS:$TAG" \
    --file $DOCKERFILE \
    .
  if [ -n "$IGNORE_PATH" ]; then
    rm .dockerignore
  fi
  if [ -n "$CI" ]; then
    docker push "$NS:$TAG"
  fi
fi
