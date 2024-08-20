import re


url_pattern = r'(http(s)?://\S+)'
url_replacement_string = r'<a href="\1" target="_blank">\1</a>'
hashtag_pattern = r'#(\w+)'
hashtag_replacement_string = r'<a href="\1">#\1</a>'


def get_hashtags(text):
    tags = re.findall(hashtag_pattern, text)
    return tags


def embed_links(text):
    # Add hrefs to inline url strings
    text = re.sub(url_pattern, url_replacement_string, text)

    # Add hrefs to hashtags
    text = re.sub(hashtag_pattern, hashtag_replacement_string, text)

    return text