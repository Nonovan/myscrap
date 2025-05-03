import asyncio, aiohttp, json
from bs4 import BeautifulSoup


async def generate_urls(queue: asyncio.Queue):
    for number in range(1, 21):
        url = f"https://sandbox.oxylabs.io/products?page={number}"
        # Put the URLs into a queue.
        await queue.put(url)

async def save_products(products):
    with open("products.json", "w") as f:
        json.dump(products, f, indent=4)

async def scrape(
        queue: asyncio.Queue,
        session: aiohttp.ClientSession,
        semaphore: asyncio.Semaphore,
        all_products: list
    ):
    while not queue.empty():
        url = await queue.get() # Retrieve the next URL from the queue.
        async with semaphore:
            async with session.get(url) as r:
                content = await r.text()
                soup = BeautifulSoup(content, "html.parser")
                products = []
                for product in soup.select(".product-card"):
                    title = product.select_one("h4").text
                    link = product.select_one(".card-header").get("href")
                    price = product.select_one(".price-wrapper").text
                    product_info = {
                        "Title": title,
                        "Link": "https://sandbox.oxylabs.io" + link,
                        "Price": price
                    }
                    products.append(product_info)
                all_products.extend(products)
            queue.task_done() # Mark the URL as done.

async def main():
    queue = asyncio.Queue()
    all_products = []
    # Limit to 5 concurrent requests if the website uses rate limiting.
    semaphore = asyncio.Semaphore(5)
    await generate_urls(queue)
    # Create a single aiohttp Session for multiple requests.
    async with aiohttp.ClientSession() as session:
        # Create a single scraping task.
        scrape_task = asyncio.create_task(scrape(queue, session, semaphore, all_products))
        await queue.join()
        await scrape_task
    await save_products(all_products)


if __name__ == "__main__":
    asyncio.run(main())