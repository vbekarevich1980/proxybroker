"""Find 10 working HTTP(S) proxies and save them to a file."""

import asyncio
from proxybroker import Broker


async def save(proxies, filename):
    """Save proxies to a file."""
    with open(filename, 'w') as f:
        while True:
            proxy = await proxies.get()
            if proxy is None:
                break
            proto = 'http'
            row = '%s://%s:%d\n' % (proto, proxy.host, proxy.port)
            print(row)
            f.write(row)


def main():
    proxies = asyncio.Queue()
    broker = Broker(proxies)
    tasks = asyncio.gather(broker.find(types=['HTTP'], limit=0),
                           save(proxies, filename='HTTP_proxies.txt'))
    loop = asyncio.get_event_loop()
    loop.run_until_complete(tasks)


if __name__ == '__main__':
    main()