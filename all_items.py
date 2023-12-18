from bs4 import BeautifulSoup
import requests
import json
import csv

url = 'https://hlopok-opt.ru/'

people_groups_urls = []
all_links = []
to_json = []
number_for_group = 0
group_of_people_in_numbers = {1: 'мальчики', 2: 'девочки', 3: 'малыши', 4: 'женская одежда'}

req = requests.get(url)
soup = BeautifulSoup(req.text, 'lxml')
items = soup.find_all(class_='subs')
for item in items:
    item = item.findPrevious().get('href')
    if item != 'javascript:void(0);':
        people_groups_urls.append('https://hlopok-opt.ru/' + item + '?filter%5Bpage%5D=1')
print(people_groups_urls)

with open('goods.csv', 'w', newline='') as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerow(
        (
         'группа людей',
         'ссылка на товар',
         'артикул',
         'цена',
         'размеры в наличии',
         'состав товара'
        )
    )

for one_group_url in people_groups_urls:
    i = 1
    number_for_group += 1

    while 1:
        one_group_url = one_group_url[0:-1] + str(i)
        print('one_gr', one_group_url)
        req = requests.get(one_group_url)
        soup = BeautifulSoup(req.text, 'lxml')
        goods = soup.find_all(class_='name')
        if goods == []:
            break
        i += 1

        for good in goods:
            good = 'https://hlopok-opt.ru' + str(good.get('href'))
            all_links.append(good)

            url = good
            req = requests.get(url)
            soup = BeautifulSoup(req.text, 'lxml')
            print(good)
            vendor_code = soup.find(class_='data').find('b').text
            print(vendor_code)
            price = soup.find(class_='num').text
            print(price)
            sizes = str(soup.find_all(class_='inner')[2])
            sizes = sizes.replace('<br/>', ' ')
            sizes = sizes.replace('<div class="inner">', '')
            sizes = sizes.replace('</div>', '')
            sizes = sizes.strip()
            print(sizes)
            description = soup.find_all(class_='inner')[1].text
            print(description)
            print()

            to_json.append(
                {
                    'группа людей': group_of_people_in_numbers[number_for_group],
                    'ссылка на товар': good,
                    'артикул': vendor_code,
                    'цена': price,
                    'размеры в наличии': sizes,
                    'состав товара': description
                }
            )

            with open('goods.csv', 'a', newline='') as file:
                writer = csv.writer(file, delimiter=';')
                writer.writerow(
                    (
                        group_of_people_in_numbers[number_for_group],
                        good,
                        vendor_code,
                        price,
                        sizes.strip,
                        description
                    )
                )

with open('goods.json', 'w', encoding='utf-8') as file:
    json.dump(to_json, file, indent=4, ensure_ascii=False)





