import re
from bs4 import BeautifulSoup

with open('index.html', encoding='utf-8') as file:
    src = file.read()

soup = BeautifulSoup(src, 'lxml')

title = soup.title.text # or string

print(title)


# .find() .find_all()

page_h1 = soup.find('h1')
print(page_h1)

page_all_h1 = soup.find_all('h1')
for tag in page_all_h1:
    print(tag)

# user_name = soup.find('div', class_='user__name').text.strip()
# print(user_name)
# or
# user_name_block = soup.find('div', class_='user__name')
# user_name = user_name_block.find('span').text
# print(user_name)
# or
user_name = (soup.find('div', {'class': 'user__name', 'id': 'user_name'})
             .find('span').text)
print(user_name)

find_all_span_in_user_info = soup.find(class_='user__info').find_all('span')
print(find_all_span_in_user_info[-1].text)

social_link = soup.find(class_='social__networks').find('ul').find_all('a')
for link in social_link:
    text = link.text
    url = link.get('href')
    print(f'{text}: {url}')


# .find_parent() .find_parents()

# post_div = soup.find(class_='post__text').find_parent('div', 'user__post')
# print(post_div)

post_divs = soup.find(class_='post__text').find_parents()
print(post_divs)


# .next_element() .previous_element()

# next_el = (soup.find(class_='post__title').next_element
#            .next_element.text)
# print(next_el)
# or
next_el = soup.find(class_='post__title').find_next()
print(next_el)

# .find_next_sibling() .find_previous_sibling()

next_sib = soup.find(class_='post__title').find_next_sibling()
print(next_sib)

links = soup.find(class_='some__links').find_all('a')
for link in links:
    link_href = link.get('href') # or >>> link['href']
    link_data = link.get('data-attr') # or >>> link['data-attr']
    print(f'{link_data}: {link_href}')


find_by_text = soup.find(string=re.compile('Одежда'))
print(find_by_text)

find_all_clothes = soup.find_all(string=re.compile('([Оо]дежда)'))
print(find_all_clothes)