import re
import requests
import coloredlogs
import logging

from bs4 import BeautifulSoup
from requests.exceptions import ConnectionError

coloredlogs.install()


def prettify(text):
    return text.strip().replace('\n', '').replace(' ', '')


def remove_trash(text):
    trash = re.findall('\([+|-][0-9]+\)', text)
    for t in trash:
        text = text.replace(t, '')
    return text


def return_status(status_code):
    if status_code == "status-110" or status_code == "status_" or 'rgb(255, 255, 0)' in status_code:
        return "CHECK FAILED"
    elif status_code == 'status-101' or status_code == "status_up" or 'rgb(125, 252, 116)' in status_code:
        return "UP"
    elif status_code == 'status-102' or status_code == "status_corrupt" or 'rgb(81, 145, 255)' in status_code:
        return "CORRUPT"
    elif status_code == 'status-103' or status_code == "status_mumble" or 'rgb(255, 145, 20)' in status_code:
        return "MUMBLE"
    elif status_code == 'status-104' or status_code == "status_down" or 'rgb(255, 91, 91);' in status_code:
        return "DOWN"
    else:
        return "ERROR, UNKNOWN STATUS CODE"


def get_services(driver, soup):
    if driver:
        services = []
        # * Ждать, пока страница прогрузится
        while not services:
            services = driver.find_elements_by_class_name("service-name")
        return [service.strip() for service in services[0].text.split('\n')]
    elif soup:
        return [service.text for service in soup.findAll('th', 'service_name')]
    else:
        logging.critical("Something went wrong [get-services]")
        exit(1)


def init_patch(driver, soup):
    patch = {}
    services = get_services(driver, soup)
    for service in services:
        patch[service] = True
    return patch


def get_current_round(driver, soup):
    if soup:
        current_round = re.findall(
            '[0-9]+', soup.find('div', attrs={'id': 'round'}).text.strip())[0]
        return int(current_round)
    elif driver:
        current_round = 0
        # * Ждать пока страница прогрузится
        while int(current_round) == 0:
            current_round = driver.re(r'Round: (\d+)')[0]
        return int(current_round)
    else:
        logging.critical("Something went wrong [get-current-round]")
        exit(1)


def get_teams_info(driver, soup):
    if driver:
        teams_info = []
        # * Ждать, пока страница прогрузится
        while not teams_info:
            teams_info = driver.find_elements_by_class_name("row")[1:]
        teams = [{
            'name': team.text.split('\n')[1].strip(),
            'place': int(team.text.split('\n')[0].strip()),
            'score': float(team.text.split('\n')[3].strip()),
            'ip': team.text.split('\n')[2].strip(),
            'services': get_services_info_forcad(team, driver)
        } for team in teams_info]
        return teams
    elif soup:
        services = get_services(driver, soup)
        teams_html = soup.findAll('tr', attrs={'class': 'team'})[1:]
        teams = \
            [
                {
                    'name': team.find('div', 'team_name').text.strip(),
                    'place': int(remove_trash(team.find('td', 'place').text.strip())),
                    'score': float(team.find('td', 'score').text.strip()),
                    'ip': team.find('div', 'team_server').text.strip(),
                    'services': get_services_info_hackerdom(team, services)
                }
                for team in teams_html
            ]
        return teams
    else:
        logging.critical("Something went wrong [get-teams-info]")
        exit(1)


def get_services_info_forcad(team, driver):
    services = team.text.split('\n')[4:]
    statuses = get_status_info(driver, team)
    services_name = get_services(driver, None)
    services_info = [{
        "name": services_name[i % len(services)],
        "title": None,
        "sla": float(services[i * 3].split(':')[1].strip()[:-1]),
        "flag_points": float(services[i * 3 + 1].split(':')[1].strip()),
        "flags": {'got': int(services[i * 3 + 2].split('/')[0][1:]), 'lost':int(services[i * 3 + 2].split('/')[1][1:])},
        "status": statuses[services_name[i % len(services)]]
    } for i, _ in enumerate(services[::3])]
    return services_info


def get_services_info_hackerdom(soup, services):
    services_html = soup.findAll('td', 'team_service')
    services_status = [service['class'][1] for service in services_html]
    services_title = [service['title'].strip() if service['title']
                      else None for service in services_html]
    services_sla = [prettify(sla.find('div', 'param_value').text)
                    for sla in soup.findAll('div', 'sla')]
    services_fp = [prettify(fp.find('div', 'param_value').text)
                   for fp in soup.findAll('div', 'fp')]
    services_flags = [prettify(flags.find('div', 'param_value').text).split(
        '/') for flags in soup.findAll('div', 'flags')]
    services_flags = [[abs(int(i)) for i in flags] if len(flags) == 2 else [
        int(flags[0]), 0] for flags in services_flags]
    services_flags = [{'got': flags[0], 'lost': flags[1]}
                      for flags in services_flags]
    services_info = \
        [
            {
                'name': services[i % len(services)],
                'status': service_info[0],
                'sla': float(service_info[1][:-1]),
                'flag_points': float(service_info[2]),
                'flags': service_info[3],
                'title': service_info[4]
            }
            for i, service_info in enumerate(zip(services_status, services_sla, services_fp, services_flags, services_title))
        ]
    return services_info


def get_status_info(driver, team):
    services_name = get_services(driver, None)
    services = team.find_elements_by_class_name("service-cell")
    return {services_name[number % len(services)]: return_status(code.get_attribute("style")) for number, code in enumerate(services)}


def get_soup_by_address(address):
    if not address.startswith('http'):
        address = 'http://' + address
    try:
        html = requests.get(address)
        return BeautifulSoup(html.text, 'html.parser')

    except ConnectionError:
        logging.critical("Connection Error: " + address)
        exit(1)

    except Exception as e:
        logging.critical("Something went wrong: ".format(e))
        exit(1)
