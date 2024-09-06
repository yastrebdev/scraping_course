import re


def get_post_content(*, block):
    try:
        post_content = block.find('div', id='post')
        return post_content
    except Exception as _ex:
        print(_ex)
        print('================================')
        print('[INFO] Не нашли блок с ID "post" :(')
        return None


def get_post_title(*, block):
    try:
        post_title = block.find('h1', class_='single-title').text.strip()
        return post_title
    except Exception as _ex:
        print(_ex)
        print('================================')
        print('[INFO] Не нашли блок с CLASS "single-title" :(')
        return 'Untitled'


def get_post_info(*, block):
    try:
        post_info = block.find('div', class_='info')
        return post_info
    except Exception as _ex:
        print(_ex)
        print('================================')
        print('[INFO] Не нашли блок с CLASS "info" :(')
        return None


def get_post_author(*, block):
    try:
        post_author = block.find('a', class_='author').text.strip()
        return  post_author
    except Exception as _ex:
        print(_ex)
        print('================================')
        print('[INFO] Не нашли блок с CLASS "author" :(')
        return 'Аноним'


def get_post_date(*, block):
    try:
        block_data = block.find('div', class_='post__date-inner')
        if block_data:
            post_date = block_data.find(class_='post__date').text.strip()
            return post_date
        else:
            return '00.00.0000'
    except Exception as _ex:
        print(_ex)
        print('================================')
        print('[INFO] Не нашли блок с CLASS "post__date" :(')
        return '00.00.0000'


def get_post_theme(*, block):
    try:
        post_theme = block.find('ol', class_='breadcrumbs').find_all('li')[-1].find('span').text.strip()
        return  post_theme
    except Exception as _ex:
        print(_ex)
        print('================================')
        print('[INFO] Не нашли блок с CLASS "breadcrumbs" :(')
        return 'Без темы'


def get_post_other_urls(*, block):
    other_urls_list = []

    post_links = block.find('div', class_='text').find_all('a')
    post_source = block.find('div', class_='text').find_all('p')[-1].text

    if post_source.count('Источник:'):
        other_urls_list.append(post_source.split(': ')[1])

    for link in post_links:
        if isinstance(link, str):
            other_urls_list.append(f'https://{link}')
            continue

        url = link['href']
        if url[0] == '#' or re.search(r'hi-news|hinews', url):
            continue
        else:
            other_urls_list.append(url)

    return other_urls_list


def get_tags(*, block):
    post_tags_list = []
    try:
        post_tags = block.find('div', class_='tags').find_all('a', {'rel': 'tag'})
        for tag in post_tags:
            tag_text = tag.text
            post_tags_list.append(tag_text)
        return post_tags_list
    except Exception as _ex:
        print(_ex)
        print('================================')
        print('[INFO] Не нашли блок с CLASS "tags" :(')
        return ['']