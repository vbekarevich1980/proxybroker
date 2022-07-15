"""Gather proxies from the providers without
   checking and save them to a file."""

import asyncio
from proxybroker import Broker


async def save(proxies, filename):
    """Save proxies to a file."""
    with open(filename, 'w') as f:
        while True:
            proxy = await proxies.get()
            if proxy is None:
                break
            #print(f"{proxy.host}:{proxy.port}")
            f.write('%s:%d\n' % (proxy.host, proxy.port))
            f.flush()


def main():
    proxies = asyncio.Queue()
    broker = Broker(proxies)
    tasks = asyncio.gather(broker.grab(types=['HTTP', 'HTTPS'], limit=0),
                           save(proxies, filename='HTTP_HTTPS_proxies.txt'))#'/var/www/html/HTTP_HTTPS_proxies.txt'))
    loop = asyncio.get_event_loop()
    loop.run_until_complete(tasks)


if __name__ == '__main__':
    main()