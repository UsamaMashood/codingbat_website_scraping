from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
from selenium import webdriver
from time import sleep
import os

if 'codingbat_python_solutions' not in  os.listdir():
    os.mkdir('codingbat_python_solutions')

path = os.path.join(os.getcwd(), 'codingbat_python_solutions')


fake_user = UserAgent()
link = 'https://codingbat.com/python'
data = requests.get(link, headers = { 'fake-user' : fake_user.chrome }, timeout = 3)

soup = BeautifulSoup(data.text, 'lxml')
link = 'https://codingbat.com/'
catagory_links = [link + temp_link.a['href'] for temp_link in soup.find_all('div', class_ = 'summ')]

for catagory_link in catagory_links[2:]:
    questions_data = requests.get(catagory_link, headers = { 'fake-user' : fake_user.chrome })
    questions_soup = BeautifulSoup(questions_data.text, 'lxml')
    div_data = questions_soup.find_all('div', class_ = 'indent')
    questions_links = [link + temp_link['href'] for temp_link in div_data[0].table.find_all('a')]

    for question_link in questions_links:
        driver  =  webdriver.Chrome('chromedriver.exe')
        driver.get(question_link)
        try:
            solution_button =  driver.find_element_by_xpath('//button[@class="gray"]')
            solution_button.click()
            question_soup = BeautifulSoup(driver.page_source, 'lxml')
            question_solution = question_soup.find('div', id='results')
            solution = '\n\nSOLUTION : \n' + question_solution.pre.text
        except:
            question_soup = BeautifulSoup(driver.page_source, 'lxml')
            solution = '\n\nSOLUTION : \nsolution does not exsist'
        driver.close()
        file_data = question_soup.find('div', class_ = 'indent')
        file_names =  file_data.find_all('span')
        folder_name = file_names[0].text
        filename =os.path.join(path, folder_name +'/'+ file_names[1].text  +'.txt')
        if folder_name not in os.listdir(path):
            os.mkdir(os.path.join(path, folder_name))
        question_data = question_soup.find('div', class_ = 'minh')
        question_statement = 'QUESTION : \n' + question_data.p.text
        with open(filename, 'a') as wf:
            wf.write(question_statement)
            wf.write(solution)
