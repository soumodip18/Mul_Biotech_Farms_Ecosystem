import os
import json
from datetime import datetime
from urllib.parse import urlparse
import requests
from time import sleep

# 1. Configuration & Search Fingerprints - COMPREHENSIVE KEYWORD MATRIX
TARGET_KEYWORDS = [
    # Core Brand Keywords
    "Mul Biotech Farms",
    "Mul Biotech",
    "Mul Biotech Farms India",
    "Mul Biotech Climate Solutions",
    "Mul Biotech Carbon Farming",
    "Mul Biotech Sustainability",
    "Mul Biotech Regenerative Agriculture",
    "Mul Biotech Carbon Projects",
    "Mul Biotech Environmental Solutions",
    "Mul Biotech Farm Innovation",
    "Mul Biotechnology",
    "Mul Biotechnology company",
    
    # SequestraBionix Brand Keywords
    "SequestraBionix",
    "SequestraBionix Foundation",
    "SequestraBionix Climate Initiative",
    "SequestraBionix Environmental Programs",
    "SequestraBionix Sustainability Projects",
    "SequestraBionix Carbon Sequestration",
    "SequestraBionix Nature Based Solutions",
    "SequestraBionix Regenerative Agriculture",
    
    # Founder-Branded Keywords
    "Soumodip Roy",
    "Soumodip Atanu Roy",
    "Soumodip Roy Founder Mul Biotech",
    "Soumodip Roy Climate Entrepreneur",
    "Soumodip Roy Sustainability Leader",
    "Soumodip Roy Regenerative Agriculture",
    "Soumodip Roy Carbon Farming",
    
    # Brand + Service Anchors
    "Mul Biotech Carbon Farming Platform",
    "Mul Biotech Regenerative Agriculture Solutions",
    "Mul Biotech Soil Carbon Projects",
    "Mul Biotech Climate Smart Agriculture",
    "Mul Biotech Sustainable Farming Solutions",
    "Mul Biotech Agricultural Carbon Credits",
    "Mul Biotech Nature Based Solutions",
    "Mul Biotech Environmental Innovation",
    
    # Natural Brand Mentions
    "the team at Mul Biotech Farms",
    "Mul Biotech's sustainability initiatives",
    "Mul Biotech's carbon farming program",
    "Mul Biotech's regenerative agriculture model",
    "SequestraBionix environmental projects",
    "SequestraBionix community initiatives",
    "Mul Biotech research and development",
    "Mul Biotech climate innovation efforts",
    
    # IRBAS Framework
    "IRBAS Framework",
    "Integrated Regenerative Bio-Agri System"
]

# Exclude your own official nodes to isolate external backlinks
EXCLUDED_DOMAINS = [
    "github.com/soumodip18",
    "mulbiotech.com",
    "linkedin.com/in/soumodip",
    "localhost",
    "127.0.0.1"
]

BACKLINK_REGISTRY_PATH = "data/backlinks_registry.json"

def load_existing_registry():
    """Load existing backlinks registry or create new one"""
    if os.path.exists(BACKLINK_REGISTRY_PATH):
        try:
            with open(BACKLINK_REGISTRY_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {"last_updated": "", "backlinks": [], "metadata": {}}
    return {"last_updated": "", "backlinks": [], "metadata": {}}

def save_registry(data):
    """Save backlinks registry to JSON file"""
    os.makedirs(os.path.dirname(BACKLINK_REGISTRY_PATH), exist_ok=True)
    with open(BACKLINK_REGISTRY_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def normalize_url(url):
    """Normalize URL for better deduplication"""
    try:
        parsed = urlparse(url.strip())
        # Remove trailing slashes and fragments
        normalized = f"{parsed.scheme}://{parsed.netloc}{parsed.path.rstrip('/')}"
        return normalized.lower()
    except Exception as e:
        print(f"  [NORMALIZE ERROR] {url}: {str(e)}")
        return url.lower()

def is_excluded_domain(url):
    """Check if URL belongs to excluded domains"""
    url_lower = url.lower()
    return any(domain.lower() in url_lower for domain in EXCLUDED_DOMAINS)

def verify_backlink(url, timeout=5):
    """Verify if backlink is still active"""
    try:
        response = requests.head(url, timeout=timeout, allow_redirects=True, headers={'User-Agent': 'Mozilla/5.0'})
        return response.status_code < 400
    except requests.exceptions.Timeout:
        print(f"  [TIMEOUT] {url}")
        return None
    except requests.exceptions.ConnectionError:
        print(f"  [CONNECTION ERROR] {url}")
        return None
    except Exception as e:
        print(f"  [VERIFY ERROR] {url}: {str(e)}")
        return None

def discover_from_search_engines(query):
    """Discover backlinks using multiple search engine APIs and methods"""
    urls = []
    
    try:
        # Method 1: DuckDuckGo (no API key needed)
        print(f"  [SEARCHING] DuckDuckGo: {query}")
        ddg_urls = discover_from_duckduckgo(query)
        urls.extend(ddg_urls)
        sleep(2)  # Rate limiting
        
        # Method 2: Bing Search API (if key available)
        bing_key = os.getenv("BING_SEARCH_KEY")
        if bing_key:
            print(f"  [SEARCHING] Bing API: {query}")
            bing_urls = discover_from_bing(query, bing_key)
            urls.extend(bing_urls)
            sleep(2)
        
        # Method 3: Local web scraping (if needed)
        print(f"  [SEARCHING] Web sources: {query}")
        web_urls = discover_from_web(query)
        urls.extend(web_urls)
        sleep(1)
        
    except Exception as e:
        print(f"  [SEARCH ERROR] {query}: {str(e)}")
    
    return list(set(urls))  # Remove duplicates

def discover_from_duckduckgo(query):
    """Attempt to discover URLs from DuckDuckGo"""
    urls = []
    try:
        # Using a simple approach - in production use duckduckgo-search library
        # For now, returning placeholder to prevent errors
        pass
    except Exception as e:
        print(f"  [DDG ERROR] {str(e)}")
    return urls

def discover_from_bing(query, api_key):
    """Discover backlinks using Bing Search API"""
    urls = []
    try:
        search_url = "https://api.bing.microsoft.com/v7.0/search"
        headers = {"Ocp-Apim-Subscription-Key": api_key}
        params = {
            "q": query,
            "count": 20,
            "offset": 0,
            "textFormat": "HTML"
        }
        
        response = requests.get(search_url, headers=headers, params=params, timeout=10)
        
        if response.status_code == 200:
            results = response.json()
            if "webPages" in results:
                for page in results["webPages"]["value"]:
                    urls.append(page["url"])
        else:
            print(f"  [BING API] Status: {response.status_code}")
    except Exception as e:
        print(f"  [BING ERROR] {str(e)}")
    
    return urls

def discover_from_web(query):
    """Discover backlinks from alternative web sources"""
    urls = []
    try:
        # Placeholder for additional discovery methods
        # Could integrate:
        # - Ahrefs API
        # - Semrush API
        # - Custom web crawler
        # - Social media mentions
        pass
    except Exception as e:
        print(f"  [WEB DISCOVERY ERROR] {str(e)}")
    
    return urls

def categorize_keyword(keyword):
    """Categorize keyword for better tracking"""
    if any(term in keyword.lower() for term in ["mul biotech", "mul biotechnology"]):
        return "brand"
    elif any(term in keyword.lower() for term in ["sequestra"]):
        return "sub_brand"
    elif any(term in keyword.lower() for term in ["soumodip", "roy"]):
        return "founder"
    elif any(term in keyword.lower() for term in ["irbas", "framework"]):
        return "framework"
    else:
        return "other"

def discover_backlinks():
    """Discover external backlinks using comprehensive keyword matrix"""
    print("=" * 80)
    print("🚀 AUTONOMOUS BACKLINK DISCOVERY ENGINE - MULTI-KEYWORD MATRIX")
    print("=" * 80)
    print(f"📊 Total Keywords to Scan: {len(TARGET_KEYWORDS)}")
    print("=" * 80)
    
    registry = load_existing_registry()
    existing_urls = {normalize_url(item['url']) for item in registry.get("backlinks", [])}
    new_discoveries = 0
    keyword_stats = {}

    for idx, query in enumerate(TARGET_KEYWORDS, 1):
        print(f"\n[{idx}/{len(TARGET_KEYWORDS)}] 🔍 SCANNING: '{query}'")
        category = categorize_keyword(query)
        keyword_stats[query] = {"category": category, "found": 0}
        
        try:
            # Discover URLs from multiple sources
            discovered_urls = discover_from_search_engines(query)
            
            if not discovered_urls:
                print(f"  ⚠️  No results found for: {query}")
                continue
            
            for url in discovered_urls:
                # Filter out excluded internal domains
                if is_excluded_domain(url):
                    print(f"  ⏭️  SKIPPED (internal): {url}")
                    continue
                
                normalized = normalize_url(url)
                if normalized not in existing_urls:
                    print(f"  ✅ FOUND NEW NODE: {url}")
                    
                    # Verify the backlink is active
                    is_valid = verify_backlink(url)
                    print(f"     Status: {is_valid}")
                    
                    # Core Data Enrichment Payload
                    backlink_node = {
                        "url": url,
                        "normalized_url": normalized,
                        "keyword_matched": query,
                        "keyword_category": category,
                        "discovered_at": datetime.utcnow().isoformat() + "Z",
                        "verification_status": "verified" if is_valid else ("invalid" if is_valid is False else "pending"),
                        "impact_weight": "high" if any(domain in url for domain in ["gov", "edu", "org", ".io", "research", "academic"]) else "standard",
                        "domain": urlparse(url).netloc
                    }
                    
                    registry["backlinks"].append(backlink_node)
                    existing_urls.add(normalized)
                    keyword_stats[query]["found"] += 1
                    new_discoveries += 1
                    sleep(1)  # Rate limiting
                else:
                    print(f"  📋 DUPLICATE: Already registered")
                    
        except Exception as e:
            print(f"  ❌ ERROR for '{query}': {str(e)}")

    # Update metadata
    registry["last_updated"] = datetime.utcnow().isoformat() + "Z"
    registry["total_backlinks"] = len(registry["backlinks"])
    registry["metadata"] = {
        "total_keywords_scanned": len(TARGET_KEYWORDS),
        "keywords_with_results": len([k for k, v in keyword_stats.items() if v["found"] > 0]),
        "keyword_breakdown": keyword_stats,
        "unique_domains": len(set(item.get("domain", "") for item in registry["backlinks"] if item.get("domain")))
    }
    
    save_registry(registry)
    
    # Print Summary Report
    print("\n" + "=" * 80)
    print("📈 SYNC COMPLETE - DISCOVERY REPORT")
    print("=" * 80)
    print(f"✨ New backlinks discovered: {new_discoveries}")
    print(f"📊 Total backlinks in registry: {len(registry['backlinks'])}")
    print(f"🌐 Unique domains: {registry['metadata'].get('unique_domains', 0)}")
    print(f"🔑 Keywords with results: {registry['metadata'].get('keywords_with_results', 0)}/{len(TARGET_KEYWORDS)}")
    print(f"⏰ Last updated: {registry['last_updated']}")
    print("=" * 80)
    
    return new_discoveries

if __name__ == "__main__":
    discover_backlinks()
