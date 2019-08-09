import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.http import Request

carDetails = {"car_details": []}
spiderFinished  = []

def authentication_failed(response):
    # TODO: Check the contents of the response and return True if it failed
    # or False if it succeeded.
    print(response)
    pass

class LoginSpider(scrapy.Spider):
    name = 'anpr'

    start_urls = [
        'https://totalcarcheck.co.uk/Account/Login',
    ]
    
    def parse(self, response):
        return scrapy.FormRequest.from_response(
            response,
            formdata={'UserName': '-', 'Password': '-'},
            callback=self.after_login
        )

    def after_login(self, response):
        if authentication_failed(response):
            self.logger.error("Login failed")
            return

        url = 'https://totalcarcheck.co.uk/FreeCheck?regno=F-----L'
        yield Request(url, callback=self.parse_check_np)
    
    def parse_check_np(self, response):
        # Check MOT
        for tr in response.xpath('//tr').getall():
            if 'certLabel' in tr and 'MOT Status' in tr:
                motCheck = tr.split("<span")[1].split("</span>")[0].split('>')[1]
                motValid = 'false'

                if 'Expires:' in motCheck or 'First MOT due' in motCheck:
                    motValid = 'true'

                carDetails['car_details'].append({
                    "MOT": [{
                        "valid": motValid,
                        "details": motCheck
                    }]
                })
            elif 'certLabel' in tr and 'Road Tax Status' in tr:
                taxCheck = tr.split("<span")[1].split("</span>")[0].split('>')[1]
                taxValid = 'false'

                if 'Expires:' in taxCheck:
                    taxValid = 'true'

                carDetails['car_details'].append({
                    "Tax": [{
                        "valid": taxValid,
                        "details": taxCheck
                    }]
                })
        
        print(carDetails)
        spiderFinished.append = 'True'

def carDetailsANPR():
    process = CrawlerProcess()
    d = process.crawl(LoginSpider)
    process.start()

    itterations = 0
    while str(spiderFinished).find('True') >= 0:
        print('Spider Running')

    print('Spider Finished')
    return carDetails