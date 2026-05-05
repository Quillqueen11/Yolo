# WORDPRESS PUBLISHER SKILL

## Purpose
Publish articles to WordPress site via REST API.

---

## Setup

```python
WP_CONFIG = {
    "url": "https://yourdomain.com",
    "username": "admin",
    "password": "app_password",    # Application password, NOT login password
    "api_base": "/wp-json/wp/v2"
}
```

### Get Application Password
1. Login ke WordPress Dashboard
2. Users → Edit Profile
3. Scroll ke "Application Passwords"
4. Generate new password
5. Copy the password (looks like: `xxxx xxxx xxxx xxxx xxxx xxxx`)

---

## Basic Functions

### 1. Post Article

```python
import requests
import base64

def wp_post(title, content, status="draft", tags=None, categories=None):
    """Post article to WordPress"""
    auth = base64.b64encode(
        f"{WP_CONFIG['username']}:{WP_CONFIG['password']}".encode()
    ).decode()
    
    headers = {
        "Authorization": f"Basic {auth}",
        "Content-Type": "application/json"
    }
    
    data = {
        "title": title,
        "content": content,
        "status": status,  # 'draft', 'publish', 'pending'
        "tags": tags or [],
        "categories": categories or [],
        "excerpt": content[:200] + "...",
        "meta": {
            "source": "Quill AI",
            "generated": True
        }
    }
    
    url = f"{WP_CONFIG['url']}{WP_CONFIG['api_base']}/posts"
    resp = requests.post(url, json=data, headers=headers)
    return resp.json()
```

### 2. Schedule Post

```python
from datetime import datetime, timedelta

def wp_schedule(title, content, publish_date):
    """Schedule article for future publishing"""
    data = {
        "title": title,
        "content": content,
        "status": "future",
        "date": publish_date.isoformat()
    }
    # ... same auth pattern
```

### 3. Update Post

```python
def wp_update(post_id, title=None, content=None):
    """Update existing post"""
    data = {}
    if title: data["title"] = title
    if content: data["content"] = content
    
    url = f"{WP_CONFIG['url']}{WP_CONFIG['api_base']}/posts/{post_id}"
    resp = requests.post(url, json=data, headers=headers)
    return resp.json()
```

### 4. Get Posts

```python
def wp_get_posts(status="publish", per_page=10):
    """Get published posts"""
    url = f"{WP_CONFIG['url']}{WP_CONFIG['api_base']}/posts"
    params = {"status": status, "per_page": per_page}
    resp = requests.get(url, params=params, headers=headers)
    return resp.json()
```

---

## Advanced Features

### Categories & Tags

```python
def wp_get_or_create_category(name):
    """Get category ID or create if not exists"""
    # Search
    url = f"{WP_CONFIG['url']}{WP_CONFIG['api_base']}/categories"
    resp = requests.get(url, params={"search": name}, headers=headers)
    items = resp.json()
    if items:
        return items[0]["id"]
    
    # Create
    resp = requests.post(url, json={"name": name}, headers=headers)
    return resp.json()["id"]
```

### Featured Image

```python
def wp_set_featured_image(post_id, image_url):
    """Set featured image for post"""
    # 1. Download image
    img_data = requests.get(image_url).content
    
    # 2. Upload to media library
    headers["Content-Disposition"] = "attachment; filename=featured.jpg"
    media_url = f"{WP_CONFIG['url']}{WP_CONFIG['api_base']}/media"
    media_resp = requests.post(media_url, data=img_data, headers=headers)
    media_id = media_resp.json()["id"]
    
    # 3. Set as featured image
    post_url = f"{WP_CONFIG['url']}{WP_CONFIG['api_base']}/posts/{post_id}"
    requests.post(post_url, json={"featured_media": media_id}, headers=headers)
```

### SEO Metadata

```python
def wp_set_seo(post_id, yoast_meta):
    """Set Yoast/RankMath SEO metadata"""
    data = {
        "meta": {
            "_yoast_wpseo_title": yoast_meta["title"],
            "_yoast_wpseo_metadesc": yoast_meta["description"],
            "_yoast_wpseo_focuskw": yoast_meta["focus_keyword"]
        }
    }
    url = f"{WP_CONFIG['url']}{WP_CONFIG['api_base']}/posts/{post_id}"
    requests.post(url, json=data, headers=headers)
```

---

## Complete Workflow

```python
def publish_article(article, schedule=None):
    """Full publish workflow"""
    
    # 1. Create post
    post = wp_post(
        title=article["title"],
        content=article["content"],
        status=schedule or "draft"
    )
    post_id = post.get("id")
    if not post_id:
        return {"error": "Failed to create post"}
    
    # 2. Set categories
    for cat in article.get("categories", []):
        cat_id = wp_get_or_create_category(cat)
        # Add category to post
    
    # 3. Set featured image
    if article.get("featured_image"):
        wp_set_featured_image(post_id, article["featured_image"])
    
    # 4. Set SEO (if Yoast/RankMath active)
    if article.get("seo"):
        wp_set_seo(post_id, article["seo"])
    
    return {
        "post_id": post_id,
        "url": f"{WP_CONFIG['url']}/?p={post_id}",
        "status": "scheduled" if schedule else "draft"
    }
```

---

## Quick Test

```bash
python3 -c "
from skills.wordpress_publisher import wp_post, WP_CONFIG
WP_CONFIG['url'] = 'https://yourdomain.com'
WP_CONFIG['username'] = 'admin'
WP_CONFIG['password'] = 'xxxx xxxx xxxx xxxx xxxx xxxx'

result = wp_post('Test Article', 'Hello world', status='draft')
print(result)
"
```

---

_When to use: When you need to publish articles to a WordPress site._