import re

_HTTP_PREFIX = re.compile(r"^https?:.*")


def sniff_gs(uri: str) -> bool:
    """Returns True if `uri` appears to be a Google Storage, GS, URI."""
    return uri.startswith("gs:") if uri else False


def sniff_http(uri: str) -> bool:
    """Returns True if `uri` appears to be a HTTP or HTTPS URI."""
    return not _HTTP_PREFIX.match(uri) is None if uri else False


def sniff_local(uri: str) -> bool:
    """Returns True if `uri` appears to be a local filesystem path."""
    return not sniff_s3(uri) and not sniff_http(uri) and not sniff_gs(uri)


def sniff_s3(uri: str) -> bool:
    """Returns True if `uri` appears to be an AWS S3 URI."""
    return uri.startswith("s3:") if uri else False
