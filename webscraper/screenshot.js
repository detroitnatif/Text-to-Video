import puppeteer from 'puppeteer'

(async () => {

    const browser = await puppeteer.launch({
        headless: headless ? 'new' : false,
    });

    const page = await browser.newPage();

    await page.setViewport(
        {
            width: 1200,
            height: 1200,
            deviceScaleFactor: 1,
        }
    );

    page.goto('https://en.wikipedia.org/Sam_altman');

    browser.close();
}
)();