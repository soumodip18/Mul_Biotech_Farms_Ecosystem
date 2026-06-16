import os
import json
from datetime import datetime
from urllib.parse import urlparse
import requests
from time import sleep

# 1. Configuration & Search Fingerprints
TARGET_KEYWORDS = [
    "Soumodip Atanu Roy",
    "Mul Biotech Farms",
    "SequestraBionix",
    "IRBAS Framework", 
    "Mul Biotechnology",
    "Integrated Regenerative Bio-Agri System"
]

# Exclude your own official nodes to isolate external backlinks
EXCLUDED_DOMAINS = [
    "github.com/soumodip18",
    "mulbiotech.com",
    "linkedin.com"
]

BACKLINK_REGISTRY_PATH = "data/backlinks_registry.json"

def load_existing_registry():
    """Load existing backlinks registry or create new one"""
    if os.path.exists(BACKLINK_REGISTRY_PATH):
        try:
            with open(BACKLINK_REGISTRY_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {"last_updated": "", "backlinks": []}
    return {"last_updated": "", "backlinks": []}

def save_registry(data):
    """Save backlinks registry to JSON file"""
    os.makedirs(os.path.dirname(BACKLINK_REGISTRY_PATH), exist_ok=True)
    with open(BACKLINK_REGISTRY_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def normalize_url(url):
    """Normalize URL for better deduplication"""
    parsed = urlparse(url.strip())
    # Remove trailing slashes and fragments
    normalized = f"{parsed.scheme}://{parsed.netloc}{parsed.path.rstrip('/')}"
    return normalized.lower()

def is_excluded_domain(url):
    """Check if URL belongs to excluded domains"""
    url_lower = url.lower()
    return any(domain.lower() in url_lower for domain in EXCLUDED_DOMAINS)

def verify_backlink(url, timeout=5):
    """Verify if backlink is still active"""
    try:
        response = requests.head(url, timeout=timeout, allow_redirects=True)
        return response.status_code < 400
    except Exception as e:
        print(f"  [VERIFY FAILED] {url}: {str(e)}")
        return None

def discover_backlinks():
    """Discover external backlinks using multiple search approaches"""
    print("=" * 70)
    print("Initializing Autonomous Backlink Discovery Engine...")
    print("=" * 70)
    
    registry = load_existing_registry()
    existing_urls = {normalize_url(item['url']) for item in registry.get("backlinks", [])}
    new_discoveries = 0

    for query in TARGET_KEYWORDS:
        print(f"\n[SCANNING] Footprint for: '{query}'")
        
        try:
            # Using Bing Search API alternative (more reliable than google-search)
            search_url = f"https://api.bing.microsoft.com/v7.0/search"
            headers = {
                "Ocp-Apim-Subscription-Key": os.getenv("BING_SEARCH_KEY", "demo-key")
            }
            
            params = {
                "q": query,
                "count": 20,
                "offset": 0
            }
            
            # Fallback: Parse results from a simple HTTP request
            # Note: For production, use a proper API with authentication
            print(f"  [STATUS] Searching for: {query}")
            
            # Local backlink discovery (you can add more sources)
            discovered_urls = discover_from_web(query)
            
            for url in discovered_urls:
                # Filter out excluded internal domains
                if is_excluded_domain(url):
                    print(f"  [SKIPPED] Internal domain: {url}")
                    continue
                
                normalized = normalize_url(url)
                if normalized not in existing_urls:
                    print(f"  [FOUND NEW NODE] -> {url}")
                    
                    # Verify the backlink is active
                    is_valid = verify_backlink(url)
                    
                    # Core Data Enrichment Payload
                    backlink_node = {
                        "url": url,
                        "normalized_url": normalized,
                        "keyword_matched": query,
                        "discovered_at": datetime.utcnow().isoformat() + "Z",
                        "verification_status": "verified" if is_valid else ("invalid" if is_valid is False else "pending"),
                        "impact_weight": "high" if any(domain in url for domain in ["gov", "edu", "org", ".io"]) else "standard"
                    }
                    
                    registry["backlinks"].append(backlink_node)
                    existing_urls.add(normalized)
                    new_discoveries += 1
                    sleep(1)  # Rate limiting
                else:
                    print(f"  [DUPLICATE] Already registered: {url}")
                    
        except Exception as e:
            print(f"  [ERROR] Search execution failed for '{query}': {str(e)}")

    registry["last_updated"] = datetime.utcnow().isoformat() + "Z"
    registry["total_backlinks"] = len(registry["backlinks"])
    save_registry(registry)
    
    print("\n" + "=" * 70)
    print(f"✓ Sync Complete!")
    print(f"  - New backlinks discovered: {new_discoveries}")
    print(f"  - Total backlinks in registry: {len(registry['backlinks'])}")
    print(f"  - Last updated: {registry['last_updated']}")
    print("=" * 70)
    
    return new_discoveries

def discover_from_web(query):
    """Fallback web discovery method (placeholder for real implementation)"""
    # This is a placeholder - in production you'd use:
    # - Bing Search API
    # - Semrush API
    # - Ahrefs data
    # - DuckDuckGo
    # - Custom web crawlers
    
    urls = []
    try:
        # Example: You could add alternative sources here
        # For now, returning empty to prevent errors
        pass
    except Exception as e:
        print(f"  [WEB DISCOVERY] Error: {str(e)}")
    
    return urls

if __name__ == "__main__":
    discover_backlinks()
