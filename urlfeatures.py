"""Turn a URL (text only, nothing is opened) into a row of numbers for the model."""
import math
import re
from urllib.parse import urlsplit

from extra_features import extra
from settings import MAX_URL_LENGTH

KEYWORDS = ["login", "signin", "verify", "secure", "account", "update", "bank", "confirm",
            "password", "paypal", "wallet", "billing"]
SHORTENERS = {"bit.ly", "tinyurl.com", "goo.gl", "t.co", "ow.ly", "is.gd", "buff.ly", "rebrand.ly", "cutt.ly"}
IP_RE = re.compile(r"^\d{1,3}(\.\d{1,3}){3}$")


def check_url(text):
    """Return (clean_url, error). error is None when the address can be analysed."""
    url = (text or "").strip()
    if not url:
        return None, "Enter a web address."
    if len(url) > MAX_URL_LENGTH:
        return None, f"The address is longer than {MAX_URL_LENGTH} characters."
    if re.search(r"\s", url):
        return None, "The address must not contain spaces."
    if not url.lower().startswith(("http://", "https://")):
        return None, "Write the full address starting with http:// or https://"
    try:
        parts = urlsplit(url)
        parts.port          # raises ValueError for a broken port
    except ValueError:
        return None, "This is not a valid web address."
    if not parts.hostname:
        return None, "The address has no host name."
    return url, None


def entropy(text):
    """Shannon entropy of the characters: higher means a more random-looking text."""
    if not text:
        return 0.0
    total = len(text)
    counts = {}
    for ch in text:
        counts[ch] = counts.get(ch, 0) + 1
    return -sum(c / total * math.log2(c / total) for c in counts.values())


def extract(url):
    """url must already pass check_url. Returns a dict {feature name: number}."""
    parts = urlsplit(url)
    host = (parts.hostname or "").lower()
    labels = host.split(".")
    lower = url.lower()
    digits = sum(ch.isdigit() for ch in url)
    f = {
        "url_length": len(url),
        "host_length": len(host),
        "path_length": len(parts.path),
        "query_length": len(parts.query),
        "dots_in_host": host.count("."),
        "hyphens_in_host": host.count("-"),
        "digits_in_url": digits,
        "digit_ratio": round(digits / len(url), 4),
        "special_chars": sum(not ch.isalnum() and ch not in "./:-" for ch in url),
        "slashes": url.count("/"),
        "query_params": (parts.query.count("&") + 1) if parts.query else 0,
        "has_at": int("@" in url),
        "is_https": int(lower.startswith("https://")),
        "ip_host": int(bool(IP_RE.match(host))),
        "subdomains": max(0, len(labels) - 2),
        "has_port": int(parts.port is not None),
        "punycode": int("xn--" in host),
        "keywords": sum(lower.count(k) for k in KEYWORDS),
        "shortener": int(host in SHORTENERS),
        "double_slash_in_path": int("//" in parts.path),
        "tld_length": len(labels[-1]),
        "host_entropy": round(entropy(host), 3),
        "longest_label": max(len(x) for x in labels),
    }
    more = extra(url, parts) or {}
    for name, value in more.items():
        if name in f:
            raise ValueError(f"extra_features.py: the feature name '{name}' already exists.")
        try:
            f[name] = float(value)
        except (TypeError, ValueError):
            raise ValueError(f"extra_features.py: the value of '{name}' is not a number.")
    return f


def feature_names():
    return list(extract("http://example.com/").keys())
