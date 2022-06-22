def proxy_image(url):
    if not url:
        return url
    
    return f"https://master-game-list.ekp.earnkeeper.io/image?url={url}"