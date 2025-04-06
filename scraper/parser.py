from .flight_page import FlightPage


def parse_flight_info(html: str) -> dict:
    page = FlightPage(html)

    try:
        ticket = page.get_ticket()
        if ticket is None:
            return {"error": "No flights matching the search criteria. Please search the inputs."}

        departure = page.get_departure_card()
        arrival = page.get_arrival_card()

        flight_number = ticket.select_one(
            '.ticket__FlightNumberContainer-sc-1rrbl5o-4 div:nth-of-type(1)'
        ).text.strip()

        airline = ticket.select_one(
            '.ticket__FlightNumberContainer-sc-1rrbl5o-4 div:nth-of-type(2)'
        ).text.strip()

        if not flight_number or not airline:
            raise ValueError("There are no flights matching the search criteria.")

        routes = ticket.select('.route-with-plane__Route-sc-154xj1h-1')
        from_code = routes[0].select_one('a').text.strip()
        from_city = routes[0].select_one('.Yjlkn').text.strip()
        to_code = routes[-1].select_one('a').text.strip()
        to_city = routes[-1].select_one('.Yjlkn').text.strip()

        status_container = ticket.select_one('.ticket__StatusContainer-sc-1rrbl5o-17')
        arrival_status = status_container.select_one('div:nth-of-type(1)').text.strip()
        timing_status = status_container.select_one('div:nth-of-type(2)').text.strip()

        flight_info = {
            "flight_number": flight_number,
            "airline": airline,
            "from": {
                "code": from_code,
                "city": from_city
            },
            "to": {
                "code": to_code,
                "city": to_city
            },
            "status": {
                "arrival": arrival_status,
                "timing": timing_status
            },
            "departure": {
                "airport_code": departure.select_one('a.ticket__AirportLink-sc-1rrbl5o-10').text.strip(),
                "city": departure.select('div.text-helper__TextHelper-sc-8bko4a-0')[1].text.strip(),
                "airport_name": departure.select('div.text-helper__TextHelper-sc-8bko4a-0')[2].text.strip(),
                "date": departure.select_one('div.cPBDDe').text.strip(),
                "scheduled_time": departure.select('div.kbHzdx')[0].text.strip(),
                "actual_time": departure.select('div.kbHzdx')[1].text.strip(),
                "terminal": departure.select('div.ticket__TGBValue-sc-1rrbl5o-16')[0].text.strip(),
                "gate": departure.select('div.ticket__TGBValue-sc-1rrbl5o-16')[1].text.strip(),
            },
            "arrival": {
                "airport_code": arrival.select_one('a.ticket__AirportLink-sc-1rrbl5o-10').text.strip(),
                "city": arrival.select('div.text-helper__TextHelper-sc-8bko4a-0')[1].text.strip(),
                "airport_name": arrival.select('div.text-helper__TextHelper-sc-8bko4a-0')[2].text.strip(),
                "date": arrival.select_one('div.cPBDDe').text.strip(),
                "scheduled_time": arrival.select('div.kbHzdx')[0].text.strip(),
                "actual_time": arrival.select('div.kbHzdx')[1].text.strip(),
                "terminal": arrival.select('div.ticket__TGBValue-sc-1rrbl5o-16')[0].text.strip(),
                "gate": arrival.select('div.ticket__TGBValue-sc-1rrbl5o-16')[1].text.strip(),
            }
        }

        return flight_info

    except Exception as e:
        return {"error": str(e)}
