"""
pridect.py  —  Load the trained XGBoost model and extract features from a raw URL.

Functions:
    extract_features(url: str) -> dict   — Parse a URL into numeric features
    predict_url(url: str) -> dict        — Run the model on the extracted features
"""

import pickle
import os
import re
from urllib.parse import urlparse, parse_qs
import numpy as np

# ── Load Model & Feature Names ──────────────────────────────
_DIR = os.path.dirname(__file__)
_MODEL_PATH = os.path.join(_DIR, "xgb_phishing_model.pkl")
_FEATURES_PATH = os.path.join(_DIR, "feature_names.pkl")

with open(_MODEL_PATH, "rb") as f:
    _model = pickle.load(f)

with open(_FEATURES_PATH, "rb") as f:
    _feature_names = pickle.load(f)


# ── Sensitive Words List ─────────────────────────────────────
SENSITIVE_WORDS = [
    "login", "signin", "sign-in", "log-in", "verify", "update",
    "account", "secure", "banking", "confirm", "password", "suspend",
    "authenticate", "wallet", "security", "ebayisapi", "webscr",
]


def extract_features(url: str) -> dict:
    """
    Extract the same 48 numeric features that the model was trained on,
    purely from the URL string.

    Note ─ Some features in the original CSV came from HTML content analysis
    (e.g. InsecureForms, ExtFavicon).  Since we only have the URL at
    prediction time, we set those features to 0 (neutral/unknown).
    """
    parsed = urlparse(url if "://" in url else f"http://{url}")

    hostname = parsed.hostname or ""
    path = parsed.path or ""
    query = parsed.query or ""
    full = url

    # ── URL-level counts ──
    num_dots = full.count(".")
    subdomain_level = max(0, hostname.count(".") - 1)
    path_level = path.strip("/").count("/") if path.strip("/") else 0
    url_length = len(full)
    num_dash = full.count("-")
    num_dash_host = hostname.count("-")
    at_symbol = 1 if "@" in full else 0
    tilde = 1 if "~" in full else 0
    num_underscore = full.count("_")
    num_percent = full.count("%")

    # Query components
    qc = parse_qs(query)
    num_query_components = len(qc)
    num_ampersand = query.count("&")
    num_hash = full.count("#")

    num_numeric = sum(c.isdigit() for c in full)
    no_https = 0 if parsed.scheme == "https" else 1

    # Random-looking string detection (high numeric ratio in hostname)
    char_count = len(hostname.replace(".", ""))
    digit_count = sum(c.isdigit() for c in hostname)
    random_string = 1 if char_count > 0 and (digit_count / char_count) > 0.4 else 0

    # IP address instead of domain
    ip_pattern = re.compile(r"^\d{1,3}(\.\d{1,3}){3}$")
    ip_address = 1 if ip_pattern.match(hostname) else 0

    domain_in_subdomains = 1 if subdomain_level > 1 else 0
    domain_in_paths = 1 if re.search(r"\.\w{2,6}/", path) else 0
    https_in_hostname = 1 if "https" in hostname.lower() else 0
    hostname_length = len(hostname)
    path_length = len(path)
    query_length = len(query)
    double_slash = 1 if "//" in path else 0

    # Sensitive words count
    lower_url = full.lower()
    num_sensitive = sum(1 for w in SENSITIVE_WORDS if w in lower_url)

    embedded_brand = 0  # Would need brand list + NLP, set neutral

    # ── HTML-derived features (not available from URL alone → set to 0) ──
    pct_ext_hyperlinks = 0.0
    pct_ext_resource_urls = 0.0
    ext_favicon = 0
    insecure_forms = 0
    relative_form_action = 0
    ext_form_action = 0
    abnormal_form_action = 0
    pct_null_self_redirect = 0.0
    freq_domain_mismatch = 0
    fake_link_status_bar = 0
    right_click_disabled = 0
    popup_window = 0
    submit_info_to_email = 0
    iframe_or_frame = 0
    missing_title = 0
    images_only_form = 0

    # ── Ratio/RT features (simplified) ──
    subdomain_level_rt = 1 if subdomain_level >= 3 else 0
    url_length_rt = 1 if url_length > 75 else 0
    pct_ext_resource_rt = 0
    abnormal_ext_form_r = 0
    ext_meta_script_link_rt = 0
    pct_ext_null_redirect_rt = 0

    features = {
        "NumDots": num_dots,
        "SubdomainLevel": subdomain_level,
        "PathLevel": path_level,
        "UrlLength": url_length,
        "NumDash": num_dash,
        "NumDashInHostname": num_dash_host,
        "AtSymbol": at_symbol,
        "TildeSymbol": tilde,
        "NumUnderscore": num_underscore,
        "NumPercent": num_percent,
        "NumQueryComponents": num_query_components,
        "NumAmpersand": num_ampersand,
        "NumHash": num_hash,
        "NumNumericChars": num_numeric,
        "NoHttps": no_https,
        "RandomString": random_string,
        "IpAddress": ip_address,
        "DomainInSubdomains": domain_in_subdomains,
        "DomainInPaths": domain_in_paths,
        "HttpsInHostname": https_in_hostname,
        "HostnameLength": hostname_length,
        "PathLength": path_length,
        "QueryLength": query_length,
        "DoubleSlashInPath": double_slash,
        "NumSensitiveWords": num_sensitive,
        "EmbeddedBrandName": embedded_brand,
        "PctExtHyperlinks": pct_ext_hyperlinks,
        "PctExtResourceUrls": pct_ext_resource_urls,
        "ExtFavicon": ext_favicon,
        "InsecureForms": insecure_forms,
        "RelativeFormAction": relative_form_action,
        "ExtFormAction": ext_form_action,
        "AbnormalFormAction": abnormal_form_action,
        "PctNullSelfRedirectHyperlinks": pct_null_self_redirect,
        "FrequentDomainNameMismatch": freq_domain_mismatch,
        "FakeLinkInStatusBar": fake_link_status_bar,
        "RightClickDisabled": right_click_disabled,
        "PopUpWindow": popup_window,
        "SubmitInfoToEmail": submit_info_to_email,
        "IframeOrFrame": iframe_or_frame,
        "MissingTitle": missing_title,
        "ImagesOnlyInForm": images_only_form,
        "SubdomainLevelRT": subdomain_level_rt,
        "UrlLengthRT": url_length_rt,
        "PctExtResourceUrlsRT": pct_ext_resource_rt,
        "AbnormalExtFormActionR": abnormal_ext_form_r,
        "ExtMetaScriptLinkRT": ext_meta_script_link_rt,
        "PctExtNullSelfRedirectHyperlinksRT": pct_ext_null_redirect_rt,
    }

    return features


def predict_url(url: str) -> dict:
    """
    Run the full pipeline:  URL → features → XGBoost → result dict.

    Returns:
        {
            "url": str,
            "is_phishing": bool,
            "confidence": float,      # 0.0 – 1.0
            "features": dict           # raw feature values (for debugging)
        }
    """
    features = extract_features(url)

    # Build input array in the same column order the model expects
    input_array = np.array([[features[f] for f in _feature_names]])

    # Probability of class 1 (phishing)
    proba = _model.predict_proba(input_array)[0]
    phishing_prob = float(proba[1])
    is_phishing = phishing_prob >= 0.5

    return {
        "url": url,
        "is_phishing": is_phishing,
        "confidence": round(phishing_prob if is_phishing else (1 - phishing_prob), 4),
        "features": features,
    }
