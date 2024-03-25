"use strict";

import puppeteer from 'puppeteer'


const url = process.argv[2];

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

    await page.goto( url, {
        waitUntil: 'domcontentloaded'
    });

    await new Promise((resolve, reject) => {
        setTimeout(() => {
            resolve();
        }, 4000);
    });
    

    await page.screenshot({
        path: 'screenshot.jpg'
    });

    await browser.close();
}
)();