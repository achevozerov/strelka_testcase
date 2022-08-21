import scrapy
import time
import logging

from strelka_testcase.items import HotelItem


class HotelsListSpider(scrapy.Spider):
    name = 'hotels_list_spider'

    start_urls = ['https://классификация-туризм.рф/displayAccommodation/index?Accommodation[FullName]=&Accommodation[Region]=Калужская+область&Accommodation[Key]=&Accommodation[OrganizationId]=&Accommodation[CertificateNumber]=&Accommodation[Inn]=&Accommodation[Ogrn]=&Accommodation[SolutionNumber]=&yt0=Найти']

    def parse(self, response):
        """
            Функция парсит ссылки на объекты на страницах и передаёт в функцию parse_hotel_page
        """
        hotels_links = response.css('a.object-title::attr(href)')
        yield from response.follow_all(hotels_links, self.parse_hotel_page)

        # Без этой заглушки response периодически отдаёт Too many requests
        time.sleep(0.3)

        next_page = response.css('.next a::attr(href)').get()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

    def parse_hotel_page(self, response):
        """
            Функция парсит страницы объектов и возвращает их параметры
        """
        # Сервис возвращает статус 200 и при этом отдаёт Too many requests, приходится обрабатывать вручную
        if response.css('title::text').get() is None:
            logging.error(response.text)
            time.sleep(60)
            yield from response.follow(response.url, self.parse_hotel_page)

        general_information = response.css('div.detail-fields')

        hotel = HotelItem()
        hotel['id'] = response.css('div.detail-field > span.detail-value::text').get()
        hotel['hotel'] = response.css('title::text').get()
        hotel['type'] = general_information.css('div.detail-field:nth-child(2) > span.detail-value::text').get()
        hotel['legal_entity_name'] = general_information.css('div.detail-field:nth-child(5) > span.detail-value::text').get()
        hotel['region'] = general_information.css('div.detail-field:nth-child(6) > span.detail-value::text').get()
        hotel['inn'] = general_information.css('div.detail-field:nth-child(7) > span.detail-value::text').get()
        hotel['ogrn'] = general_information.css('div.detail-field:nth-child(8) > span.detail-value::text').get()
        hotel['address'] = general_information.css('div.detail-field:nth-child(9) > span.detail-value::text').get()
        hotel['phone_number'] = general_information.css('div.detail-field:nth-child(10) > span.detail-value::text').get()
        hotel['email'] = general_information.css('div.detail-field:nth-child(12) > span.detail-value::text').get()
        hotel['site_url'] = general_information.css('div.detail-field:nth-child(13) > span.detail-value::text').get()
        hotel['classification'] = general_information.css('div.classification-info > div.detail-field:nth-child(1) > span.detail-value::text').get()

        yield hotel