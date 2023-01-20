#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
import urllib

import aiohttp
import asyncio
from bs4 import BeautifulSoup


def parse_url(s: str) -> str:
    """For a URL, returns the file name to save the results under.

    Will replace slashes with double underscores, as Python refuses to
    accept slashes in file names (even though they can be valid).

    """
    actual_url = urllib.parse.urlparse(s)
    file_name = (str(actual_url.path)).rstrip("/")
    path_has_extension = bool(os.path.splitext(file_name)[1])
    extension = os.path.splitext(file_name)[1] or ".html"
    out_name = (
        f'{actual_url.hostname}{file_name}{"" if path_has_extension else extension}'
    )
    return out_name.replace("/", "__")


async def download_url(url: str, metadata: bool) -> str:
    """ "
    Downloads content from a URL and stores it.

    Returns a string which can contain errors or info.

    If `metadata` is set, the returned string will contain details
    about the content fetched.
    """
    out_file_name = parse_url(url)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            rv = ""
            if metadata:
                rv += "------\n"
                rv += f"site: {url}\n"
                rv += f'content type: {resp.headers["Content-Type"]}\n'
            if resp.status != 200:
                rv += f"[error] request for {url} received HTTP {resp.status}\n"
            else:
                body = await resp.read()
                if metadata:
                    rv += f"saved to: {out_file_name}\n"
                    if "text/html" in resp.headers["Content-Type"]:
                        soup = BeautifulSoup(body, "html.parser")
                        rv += "html:\n"
                        rv += f"  title: {soup.title.string}\n"
                        rv += f'  links: {len(soup.find_all("a"))}\n'
                        rv += f'  images: {len(soup.find_all("img"))}\n'
                with open(out_file_name, "wb") as fp:
                    fp.write(body)
            return rv


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--metadata", action="store_true", help="print out additional metadata"
    )
    parser.add_argument("urls", nargs="+", metavar="url", help="the urls to fetch")
    args = parser.parse_args()

    downloads = [download_url(url, args.metadata) for url in args.urls]
    results = await asyncio.gather(*downloads)
    for r in results:
        if r:
            print(r.strip())


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
