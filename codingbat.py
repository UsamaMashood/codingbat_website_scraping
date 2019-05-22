from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
from openpyxl import Workbook

wb= Workbook()
questions_sheet = wb.active
questions_sheet.title = 'python questions'

head = ['Heading', 'Question Statement', 'Example']
questions_sheet.append(head)

fake_user = UserAgent()
link = 'https://codingbat.com/python'
data = requests.get(link, headers = { 'fake-user' : fake_user.chrome }, timeout = 3)

soup = BeautifulSoup(data.text, 'lxml')
link = 'https://codingbat.com/'
catagory_links = [link + temp_link.a['href'] for temp_link in soup.find_all('div', class_ = 'summ')]

for catagory_link in catagory_links:
    questions_data = requests.get(catagory_link, headers = { 'fake-user' : fake_user.chrome })
    questions_soup = BeautifulSoup(questions_data.text, 'lxml')
    div_data = questions_soup.find_all('div', class_ = 'indent')
    questions_links = [link + temp_link['href'] for temp_link in div_data[0].table.find_all('a')]

    for question_link in questions_links:
        store_data = []
        question_data = requests.get(question_link, headers={'fake-user': fake_user.chrome})
        question_soup = BeautifulSoup(question_data.text, 'lxml')
        question_data = question_soup.find('div', class_ = 'minh')
        heading = question_soup.find_all('span', class_ = 'h2')
        heading = heading[1].text
        question_statement = question_data.p.text
        examples = [str(example.string) for example in question_data.next_siblings if example.string]
        store_data.append(heading)
        store_data.append(question_statement)
        store_data.append('\n'.join(examples))
        questions_sheet.append(store_data)



wb.save('Coding_Bat.xlsx')