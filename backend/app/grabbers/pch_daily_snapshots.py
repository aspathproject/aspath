import bs4, sys, urllib3, json, datetime, time, pytz
import cgi
import re
import gzip
from io import BytesIO, TextIOWrapper

# PCH Daily Snapshot grabber
# ==
# This module will perform a scraping process on Packet Clearing House website to fetch all available dataset links according to given parameters


# Grabber setup parameters

# Just consider datasets after 2009 where a format change occurred, honestly I don't know what they changed
# TODO: configure this parameter from driver options
START_FROM_YEAR = 2018


http = urllib3.PoolManager()

def get_available_years():
  available_years = []
  page = http.request('GET', 'https://www.pch.net/resources/Routing_Data/IPv4_daily_snapshots/')
  parsed_page = bs4.BeautifulSoup(page.data, features='lxml')
  folder_names = parsed_page.select('#resources-table > tbody > tr > td > a > strong')
  for folder in folder_names:
    if folder and folder.text.strip().isdecimal():
     year = int(folder.text.strip())
     if START_FROM_YEAR <= year:
       available_years.append(year)
  return available_years

def get_available_months(year):
  available_months = []
  page = http.request('GET', f"https://www.pch.net/resources/Routing_Data/IPv4_daily_snapshots/{year}/")
  parsed_page = bs4.BeautifulSoup(page.data, features='lxml')
  folder_names = parsed_page.select('#resources-table > tbody > tr > td > a > strong')
  for folder in folder_names:
    if folder and folder.text.strip().isdecimal():
     month = folder.text.strip()
     available_months.append(month)

  available_months.sort()
  return available_months

def collector_data_available(route_collector, year, month):
  page = http.request('GET', f"https://www.pch.net/resources/Routing_Data/IPv4_daily_snapshots/{year}/{month}/")
  parsed_page = bs4.BeautifulSoup(page.data, features='lxml')
  folder_names = parsed_page.select('#resources-table > tbody > tr > td > a > strong')
  for folder in folder_names:
    if folder and folder.text.strip() == route_collector:
      return True
  return False

def get_snapshot_links(route_collector, year, month):
  available_datasets = []
  page = http.request('GET', f"https://www.pch.net/resources/Routing_Data/IPv4_daily_snapshots/{year}/{month}/{route_collector}/")
  parsed_page = bs4.BeautifulSoup(page.data, features='lxml')
  file_names = parsed_page.select('#resources-table > tbody > tr > td > a')
  for file in file_names:
    if file:
     filename = file.text.strip()
     available_datasets.append(f"https://www.pch.net/resources/Routing_Data/IPv4_daily_snapshots/{year}/{month}/{route_collector}/{filename}")

  available_datasets.sort()
  return available_datasets

def get_all_dataset_links(route_collector_name):

  dataset_links = []
  years = get_available_years()
  print(f"Available years on PCH website: {years}")
  years.sort()

  for year in years:
    for month in get_available_months(year):
      print(f"checking {year}-{month}")
      if collector_data_available(route_collector_name, year, month):
        print(f"{route_collector_name} available in {year}-{month}")
        dataset_links.extend(get_snapshot_links(route_collector_name, year, month))
  return dataset_links

def get_cabase_link_list():
  with open('grabbers/cabase.json') as fh:
    return json.load(fh)

def download_dataset_link(link):
  file_content = http.request('GET', link)
  return file_content.data
