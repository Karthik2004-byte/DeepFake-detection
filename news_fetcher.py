import requests

def get_deepfake_news():
    """
    Fetches the latest news articles related to deepfakes and AI deepfake detection.
    
    Returns:
        list: A list of dictionaries, each containing:
            - title (str): Article title
            - summary (str): Short description of the article
            - link (str): URL to the full article
            - image_url (str): URL of the article image (if available)
    """
    api_key = '449082e8348340c7bfdc2ee74575f756'  # Replace with your actual NewsAPI key
    url = (
        'https://newsapi.org/v2/everything?'
        'q=deepfake+OR+"AI+deepfake"+OR+"deepfake+detection"&'
        f'apiKey={api_key}&'
        'language=en&'
        'sortBy=publishedAt&'
        'pageSize=20'
    )

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise error for bad status codes
        articles = response.json().get('articles', [])

        news = []
        for article in articles:
            news.append({
                'title': article.get('title'),
                'summary': article.get('description'),
                'link': article.get('url'),
                'image_url': article.get('urlToImage')
            })

        return news

    except requests.RequestException as e:
        print(f"Error fetching news: {e}")
        return []
