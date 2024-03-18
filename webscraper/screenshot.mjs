import puppeteer from 'puppeteer'

(async () => {

    const browser = await puppeteer.launch({
        headless: false,
        executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
    });


    const page = await browser.newPage();

    await page.setViewport(
        {
            width: 1200,
            height: 1200,
            deviceScaleFactor: 1,
        }
    );

    await page.goto('https://www.accuweather.com/en/fr/paris/623/weather-forecast', {
        waitUntil: 'networkidle0'
    });

    await page.screenshot({
        path: 'screenshot.jpg'
    });

    await browser.close();
}
)();