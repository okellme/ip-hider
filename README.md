# IP Hider

A Python command-line tool that hides your real IP address by routing requests through free public proxy servers. Built for privacy and to demonstrate practical networking skills — fetching, testing, and rotating through live proxies automatically.

## Features

- Check your real, current IP address
- Fetch a live list of free public proxies
- Automatically test proxies to find working ones
- Route requests through a working proxy to mask your real IP
- Automatic proxy rotation if a proxy fails mid-use
- Simple menu-driven interface

## Tech Stack

- Python 3
- `requests` library for HTTP requests and proxy routing
- ProxyScrape API (free) for live proxy lists
- ipify API (free) for IP address lookups

## Setup

1. Clone this repository
2. Install dependencies:
