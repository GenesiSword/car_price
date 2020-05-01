"""
Extract data from given website and pass downloaded data to cardata.py.
"""

import time
import logging
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import cardata

logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
# logging.disable(logging.CRITICAL)


class Mining:
    """
    Extract data from given website.

    Methods:
        web_open()
        find_brand()
        find_vehicle()
        extract()
        search_results()

    Variables:
        self.driver -> defined web driver.
        self.second_data -> text version of data directly extracted from
                            website. Is passed the variable self.third_data.
        self.third_data -> data extracted from website.
        self.brand_name -> name of vehicle brand defined in mainbody.py.
        self.vehicle_name -> name of vehicle defined in mainbody.py.
    """
    def __init__(self,
                 driver=None,
                 second_data=None,
                 third_data=None,
                 brand_name=None,
                 vehicle_name=None,
                 source=None):
        self.driver = driver
        self.third_data = third_data
        self.second_data = second_data
        self.brand_name = brand_name
        self.vehicle_name = vehicle_name
        self.source = source

    def web_open(self):
        """
        Define web driver and website to download data from.
        """
        website = 'https://'+self.source
        self.driver = webdriver.Firefox()
        self.driver.get(website)

    def find_brand(self):
        """
        Enter defined vehicle brand name to the website.
        """
        element = self.driver.find_element_by_xpath(
            "//div[@class='advanced-search-"
            "box fblock  make filter-item search-area__field  ']")
        element.click()

        element2 = self.driver.find_element_by_xpath(
            "//input[@class='select2-search__field']")
        element2.send_keys(self.brand_name)
        element2.send_keys(Keys.ENTER)

    def find_vehicle(self):
        """
        Enter defined vehicle name to the website.
        """
        element3 = self.driver.find_element_by_xpath(
            "//div[@class='advanced-search-"
            "box fblock  model filter-item search-area__field']")
        element3.click()

        element4 = self.driver.find_element_by_xpath(
            "//input[@class='select2-search__field']")
        element4.send_keys(self.vehicle_name)
        element4.send_keys(Keys.ENTER)

    def extract(self):
        """
        Extract data from page. Is used in search_results() method.
        """

        # Wait for website.

        time.sleep(5)

        # Save data from website to the variable first_data.

        first_data = self.driver.find_elements_by_xpath("//article[@data-ad-id]")

        # Transform data from website element into list with
        # required elements.

        for offer in first_data:
            self.second_data.append(offer.text)

        for list_offer in self.second_data:
            self.third_data.append(list_offer.split("\n"))
            self.second_data = []

    def search_results(self):
        """
        Download data from pages with cars with brand and vehicle name
        defined in variables self.brand_name and self.vehicle_name
        in class Mining().
        """

        # Click search button.

        search_element = self.driver.find_element_by_xpath(
            "//button[@class='om-button search-area__button-submit']")
        search_element.click()
        
        # Define variables needed to download data from all pages.
        
        self.second_data = []
        self.third_data = []
        page = []
        
        # Wait for the page to be ready to download data from.
        
        time.sleep(5)
        
        # Extract number of pages to download data from.

        page_num_el = self.driver.find_elements_by_xpath("//span[@class='page']")

        # Check if there is more than one page of results.
        # If there is only one page - download data from one page.
        # If there is more - download data from all pages.

        # One page.

        if page_num_el == []:
            Mining.extract(self)

        # More than one page.

        else:
            page_num = [num_el.text for num_el in page_num_el]
            for number in page_num:
                if number != '...':
                    page.append(int(number))
                else:
                    pass

            page = max(page)

            for number2 in range(1, page):
                Mining.extract(self)

                # Click hyperlink to next page.

                number2 += 1
                number2str = str(number2)

                page_num2 = self.driver.find_element_by_xpath(
                    "//span[@class='page'][text()='"+number2str+"']")
                page_loc = self.driver.find_element_by_xpath("//ul[@class='om-pager rel']")
                y_cord = str(page_loc.location['y'] - 150)
                self.driver.execute_script("window.scrollTo(0, '"+y_cord+"')")

                page_num2.click()


def execute(self):
    """
    Function connected with mainbody.py module.
    Start to execute methods in class Mining()
    and pass downloaded data, brand and vehicle name
    to the module cardata.py.
    """

    # Execute methods in class Mining().

    webmin = Mining(brand_name=Mining.brand_name,
                    vehicle_name=Mining.vehicle_name,
                    source=Mining.source)
    webmin.web_open()
    webmin.find_brand()
    webmin.find_vehicle()
    webmin.search_results()

    # Pass downloaded data, brand and vehicle name to the module cardata.py.

    cardata.Collector.input_data = webmin.third_data
    cardata.Collector.car_brand_name = webmin.brand_name
    cardata.Collector.car_vehicle_name = webmin.vehicle_name
    cardata.Collector.collect(self)

    logging.debug('WebMining done')
