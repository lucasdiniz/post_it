#coding:utf-8
#!python3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os, sys

class WordpressPoster:

    def __init__(self):
        self.browser = None
   
    def start_browser(self, path_to_chrome_driver):

        os.environ["LANG"] = "en_US.UTF-8"

        self.browser = webdriver.Chrome(path_to_chrome_driver)


    def quit_browser(self):
        # close the tab
        self.browser.quit()


    def open_site_in_new_tab(self, site_url):
        #open tab
        self.browser.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 't') 

        # Load a page 
        self.browser.get(site_url)


    def make_login(self, user_login, user_password):

        MAX_WAIT_TIME = 5 #5seg

        login_text_box = WebDriverWait(self.browser, MAX_WAIT_TIME).until(
        EC.element_to_be_clickable((By.NAME, "log")))

        login_text_box.send_keys(user_login)

        password_text_box = self.browser.find_element_by_name('pwd')
        password_text_box.send_keys(user_password)

        button_submit_login = self.browser.find_element_by_name('wp-submit')
        button_submit_login.click()


    def click_on_new_post(self):
        post_url = 'https://wordpress.com/post'
        self.browser.get(post_url)
        

    def give_name_to_post(self, post_name):
        title_text_box = self.browser.find_element_by_class_name('editor-title__input')
        title_text_box.send_keys(post_name)


    def write_html_to_post(self, html_content):
        button_html_mode = self.browser.find_element_by_link_text('HTML')
        button_html_mode.click()

        html_text_box = self.browser.find_element_by_id('tinymce-1');
        html_text_box.send_keys(html_content)

        button_visual_mode = self.browser.find_element_by_link_text('Visual')
        button_visual_mode.click()


    def add_tags_to_post(self, tag_list):

        button_add_category = self.browser.find_element_by_class_name('editor-categories-tags__accordion')
        button_add_category.click()

        for tag in tag_list:

            tag_text_box = self.browser.find_element_by_class_name('token-field__input')

            tag_text_box.send_keys(tag)
            tag_text_box.send_keys(Keys.ENTER)


    def add_category_to_post(self, post_category):

        if self.category_already_exists(post_category):
            existing_checkbox = self.browser.find_element_by_xpath("//span[contains(@class, 'term-tree-selector__label') and translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖØÙÚÛÜÝÞŸŽŠ‌​Œ', 'abcdefghijklmnopqrstuvwxyzàáâãäåæçèéêëìíîïðñòóôõöøùúûüýþÿžš‌​œ')='%s']" % post_category.lower())
            existing_checkbox.click()

        else:
            button_add_category = self.browser.find_element_by_class_name('gridicons-folder')
            button_add_category.click()

            category_text_box = self.browser.find_element_by_xpath("//input[@placeholder='New Category Name']")
            category_text_box.send_keys(post_category)
            category_text_box.send_keys(Keys.ENTER)


    def category_already_exists(self, post_category):
      
        category_checkboxes = self.browser.find_elements_by_xpath("//span[contains(@class, 'term-tree-selector__label')]")

        for checkbox in category_checkboxes:
            if checkbox.text.lower() == post_category.lower():
                return True

        return False
            

    def add_featured_image(self, image_url):

        MAX_WAIT_TIME = 10 #10sec

        button_add_image = WebDriverWait(self.browser, MAX_WAIT_TIME).until(
        EC.element_to_be_clickable((By.XPATH, "//span[contains(@class, 'accordion__title') and text()='Featured Image']")))
      
        button_add_image.click()


        button_set_image = self.browser.find_element_by_xpath("//span[contains(@class, 'editor-drawer-well__button') and text()='Set Featured Image']")
        button_set_image.click()

        button_set_image_url = self.browser.find_element_by_xpath("//button[contains(@class, 'button is-desktop') and text()='Add via URL']")
        button_set_image_url.click()

        url_text_box = self.browser.find_element_by_xpath("//input[@placeholder='https://']")
        url_text_box.send_keys(image_url)

        button_submit_image_url = self.browser.find_element_by_xpath("//button[contains(@class, 'button is-primary') and text()='Upload']")
        button_submit_image_url.click()


        button_send_image = self.browser.find_element_by_xpath("//span[contains(@class, 'dialog__button-label') and text()='Set Featured Image']")
        button_send_image.click()


    def send_post(self):

        MAX_WAIT_TIME = 10 #10sec

        button_publish_post = WebDriverWait(self.browser, MAX_WAIT_TIME).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'editor-ground-control__publish-button') and text()='Publish']")))

        button_publish_post.click()



    def get_post_url(self):

        MAX_WAIT_TIME = 10

        final_url = WebDriverWait(self.browser, MAX_WAIT_TIME).until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'notice__action')]")))

        return final_url.get_attribute("href")



    #Publishs and returns the URL of the new post
    def publish_new_post(self,
        user_login,user_password, 
        post_title, post_html_content, post_tags, post_category, post_image_link,
        path_to_chrome_driver=os.path.dirname(os.path.realpath(__file__)) + '/chromedriver_folder/chromedriver.exe', 
        wordpress_login_link='https://wordpress.com/wp-login.php'
        ):

        self.start_browser(path_to_chrome_driver)

        self.open_site_in_new_tab(wordpress_login_link)

        self.make_login(user_login, user_password)

        self.click_on_new_post()

        self.add_featured_image(post_image_link)

        self.give_name_to_post(post_title)

        self.write_html_to_post(post_html_content)

        self.add_tags_to_post(post_tags)

        self.add_category_to_post(post_category)

        self.send_post()

        post_url = self.get_post_url()

        self.quit_browser()

        return post_url

    

if __name__ == "__main__":

    #Example of usage
    wordpress_poster = WordpressPoster()
    post_url = wordpress_poster.publish_new_post() #fill in the parameters
    print post_url








