import scrapy
import logging
from time import sleep
from selenium import webdriver
from scrapy.selector import Selector
from selenium.common.exceptions import *
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.remote_connection import LOGGER
from selenium.webdriver.support import expected_conditions as condicao_esperada

def iniciar_driver():
    chrome_options = Options()
    LOGGER.setLevel(logging.WARNING)
    arguments = ['--lang=pt-BR', '--window-size=1920, 1080', '--headless']
    # '--headless' = Roda em segundo plano sem abrir a janela

    for argument in arguments:
        chrome_options.add_argument(argument)

    caminho_padrao_para_download = 'E:\\Storage\\Desktop'

    chrome_options.add_experimental_option("prefs", {
        'download.default_directory': caminho_padrao_para_download,
        'download.directory_upgrade': True,
        'download.prompt_for_download': False,
        "profile.default_content_setting_values.notifications": 2,
        "profile.default_content_setting_values.automatic_downloads": 1,
    })
    driver = webdriver.Chrome(options=chrome_options)

    
    wait = WebDriverWait(
        driver,
        10,
        poll_frequency=1,
        ignored_exceptions=[
            NoSuchElementException,
            ElementNotVisibleException,
            ElementNotSelectableException
        ]
    )

    return driver, wait

class F1RacesSpider(scrapy.Spider):
    name = 'f1racesbot'

    def start_requests(self):
        urls = ['https://f1races.netlify.app/']

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, meta={'proximo_url': url})

    def parse(self, response):
        driver, wait = iniciar_driver()
        driver.get(response.meta['proximo_url'])
        sleep(10)
        response_webdriver = Selector(text=driver.page_source)

        for corrida in response_webdriver.xpath('//div[@class="sc-bZQynM llbHfj"]'):
            yield {
                'Grand Prix': corrida.xpath('./div[1]/text()').get(),
                'Local': corrida.xpath('./div[2]/text()').get(),
                'Piloto': corrida.xpath('.//a/text()').get(),
                'Tempo': corrida.xpath('./div[4]/text()').get()
            }
        driver.close()