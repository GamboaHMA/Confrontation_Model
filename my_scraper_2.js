import axios from 'axios'
import Cheerio, { html } from 'cheerio';
import puppeteer from 'puppeteer';

(async () => {
    var htmls = GetPlayresHTMLs();
    const browser = await puppeteer.launch({headless: false});
    const page = await browser.newPage();

    for (var html of htmls){
        await page.setDefaultNavigationTimeout(100000);
        await page.goto(html);

        (await page).waitForSelector('button[class=tab-anchor]');

        const button = await page.evaluate(() => {
            const buttons_ = document.querySelectorAll('button[class=tab-anchor]');
            buttons_.forEach(button => {
                const span_text = button.querySelector('span.tab-text');
                if(span_text && span_text.innerText == 'Results'){
                    button.click();
                };
            });

            const contents_wrappers = document.querySelectorAll('.tabs-container-content');
            contents_wrappers.forEach(content_wrapper => {
                const button = content_wrapper.querySelector('button[class=btn-link]');
                button.click();


            });

            return null;
        });

        //(await page).waitForSelector('.tabs-container-content', {visible: true, timeout: 100000});

        //const contents_wrappers = await page.evaluate(() => {
        //    const contents_wrappers_ = document.querySelectorAll('.tabs-container-content');
        //    contents_wrappers_.forEach(content_wrapper => {
        //        const button = content_wrapper.querySelector('button[class=btn-link]');
        //        button.click();
        //        return contents_wrappers_;
        //    });
                     
        //});

        //(await page).waitForSelector('.tabs-container-content', {visible: true, timeout: 10000});
        //await page.evaluate(() => {
        //    const contents_wrappers = document.querySelectorAll('.tabs-container-content');
        //    contents_wrappers.forEach(content_wrapper => {
        //        const button = content_wrapper.querySelector('button[class=btn-link]');
        //        button.click();
        //        return;
        //    });
        //});
        
    };
    
    console.log('hello world');
  
})();

function GetPlayresHTMLs(){
    const htmls= ['https://uww.org/athletes-results/zou-wanhao-25552-profile'];
    return htmls;
};
  