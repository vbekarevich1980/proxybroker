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
            row = '%s:%d\n' % (proxy.host, proxy.port)
            f.write(row)
            print(row)



def main():
    proxies = asyncio.Queue()
    broker = Broker(proxies)
    tasks = asyncio.gather(broker.find(types=['CONNECT:80'], limit=0),
                           save(proxies, filename='CONNECT_80_proxies.txt'))
    loop = asyncio.get_event_loop()
    loop.run_until_complete(tasks)


if __name__ == '__main__':
    main()