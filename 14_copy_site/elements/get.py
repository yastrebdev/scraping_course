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