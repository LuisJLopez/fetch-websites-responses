import aiohttp
import asyncio
import time

from bottle import Bottle, route, run, template
from constants import URLS
from settings import DEBUG, HOST, PORT, RELOADER

app = Bottle()

async def get_request_data(url: str, session: aiohttp.ClientSession) -> dict:
    print(f"Requesting {url}")
    start = time.time()
    try:
        response = await session.request(method="GET", url=url, timeout=10)
    except aiohttp.ClientConnectorError:
        return {'url': url, 'status_code': response.status}
    end = time.time()
    response_time: float = round(end - start, 4)
    html: str = await response.text()
    print(f"Received response for {url} with status code: {response.status} in ~{response_time}s.")

    return {
        'url': url,
        'method': response.method,
        'html': html,
        'status_code': response.status,
        'response_time': response_time,
        'size': response.content_length,
    }


async def get_website_analytics(urls: set) -> list:
    async with aiohttp.ClientSession() as session:
        tasks: list = []

        for url in URLS:
            tasks.append(get_request_data(url=url, session=session))

        return await asyncio.gather(*tasks)


@app.route('/', method='GET')
@app.route('/<filter>', method='GET')
def main(filter='response_time'):
    data: list = asyncio.run(get_website_analytics(urls=URLS))
    sorted_data: list = sorted(data, key=lambda i: i[filter])

    return template('project/views/index.tlp', data=sorted_data)

run(app, host=HOST, port=PORT, debug=DEBUG, reloader=RELOADER)

if __name__ == "__main__":
    """Script requires Python 3.7+"""
    main()
