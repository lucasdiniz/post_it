#!python3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os, sys

browser = 0

def start_browser(path_to_chrome_driver):

    global browser

    os.environ["LANG"] = "en_US.UTF-8"

    browser = webdriver.Chrome(path_to_chrome_driver)


def quit_browser():
    # close the tab
    browser.quit()


def open_site_in_new_tab(site_url):
    #open tab
    browser.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 't') 

    # Load a page 
    browser.get(site_url)


def make_login(user_login, user_password):

    browser.find_element_by_name('log').send_keys(user_login)
    browser.find_element_by_name('pwd').send_keys(user_password)
    browser.find_element_by_name('wp-submit').click()


def click_on_new_post():
    browser.get('https://wordpress.com/post')
    

def give_name_to_post(post_name):
    browser.find_element_by_class_name('editor-title__input').send_keys(post_name)


def write_html_to_post(html_content):
    browser.find_element_by_link_text('HTML').click()
    browser.find_element_by_id('tinymce-1').send_keys(html_content)
    browser.find_element_by_link_text('Visual').click()


def add_tags_to_post(tag_list):

    button_add_category = browser.find_element_by_class_name('editor-categories-tags__accordion')
    button_add_category.click()

    for tag in tag_list:

        tag_text_box = browser.find_element_by_class_name('token-field__input')

        tag_text_box.send_keys(tag)
        tag_text_box.send_keys(Keys.ENTER)


def add_category_to_post(post_category):
    



if __name__ == "__main__":

    start_browser('/Users/lucasdiniz/Desktop/ProjetoPython/chromedriver')

    open_site_in_new_tab('https://wordpress.com/wp-login.php')

    make_login('lucazdinis@gmail.com', 'kong1029')

    click_on_new_post()

    give_name_to_post("Test Title")

    write_html_to_post('teste')

    add_tags_to_post(["tag1", "tag2", "tag3"])

    add_categories_to_post("teste")

    # quit_browser()




