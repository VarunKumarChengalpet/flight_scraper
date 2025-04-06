from bs4 import BeautifulSoup

class FlightPage:
    def __init__(self, html: str):
        self.soup = BeautifulSoup(html, "html.parser")

    def get_ticket(self):
        return self.soup.select_one('.ticket__Header-sc-1rrbl5o-1')

    def get_departure_card(self):
        return self.soup.select('div.ticket__TicketCard-sc-1rrbl5o-7')[0]

    def get_arrival_card(self):
        return self.soup.select('div.ticket__TicketCard-sc-1rrbl5o-7')[1]
