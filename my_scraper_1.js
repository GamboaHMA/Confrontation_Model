
import {parse} from 'node-html-parser';
import puppeteer from 'puppeteer';
import axios from 'axios';
import Cheerio, { html } from 'cheerio';

async function GetStyleUrlsFromCompetition(competition_url){
  const categories_lists = {
    "fs": ['57 kg','65 kg','74 kg','86 kg','97 kg','125 kg'],
    "gr": ['60 kg','67 kg','77 kg','87 kg','97 kg','130 kg'],
    "ww": ['50 kg','53 kg','57 kg','62 kg','68 kg','76 kg']
  };

  const {data: htmlString} = await axios.get(competition_url);
  const $ = Cheerio.load(htmlString);
  //const dom = new JSDOM(htmlString);
  //const document = dom.window.document;

  const styles_urls = {};

  $('li').each((index, element) => {
    var liElement = $(element);
    var aElement = liElement.children('a');
    if(aElement != null){
      var aDataValue = aElement.attr('data-value') !== undefined;
      if (aDataValue){
        aDataValue = aElement.attr('data-value');
        if (Object.keys(categories_lists).includes(aDataValue)){
          styles_urls[aDataValue] = aElement.attr('href')  //dataValue en este caso es la categoria
        }
      }
    }
  });

  return [styles_urls, categories_lists];
}

async function GetCategoriesUrlsFromStyle(style_url, categories_lists){
  const style = style_url[0];
  const url = style_url[1];
  var {data: htmlString} = await axios.get(style_url[1]);
  const $ = Cheerio.load(htmlString);

  const categories_urls = {};

  $('li').each((index, element) => {
    var liElement = $(element);
    var aElement = liElement.children('a');
    if (aElement != null){
      var aDataValue = aElement.attr('data-variable') !== undefined;
      if (aDataValue){
        aDataValue = aElement.attr('data-variable');
        var category = aElement.text();
        if (aDataValue == "weightcategory" && categories_lists[style].includes(category)){
          categories_urls[category] = aElement.attr('href');
        }
      }
    }
  })

  return categories_urls;
}

async function GetClashesFromCategory(category_url){
  const {data: htmlString} = await axios.get(category_url);
  const $ = Cheerio.load(htmlString);

  const clashes = [];

  $('h3').each((index, element) => {
    var h3Element = $(element);
    var a_arr = h3Element.children('a');
    if (a_arr != null){
      if (a_arr.length == 2){
        var clash = a_arr[0].textContent() + element.text() + a_arr[1].text();
        clashes.push(clash);
      }
    }
     
  })
  return null;
}

(async () => {
  var htmlString = "https://uww.org/event/zagreb-open-1/results";
  const [styles_urls, categories_lists] = await GetStyleUrlsFromCompetition(htmlString);
  
  const results_for_styles = [];

  for (let [style, s_url] of Object.entries(styles_urls)){
    htmlString = s_url;
    var categories_urls = await GetCategoriesUrlsFromStyle([style, htmlString], categories_lists);

    for (let [category, c_url] of Object.entries(categories_urls)){
      clashes = GetClashesFromCategory(category);
      results_for_styles.push([style, ])
    }
    //iterar por las categorias
    
  }
  //const {data: htmlString } = await axios.get('https://cms.uww.org/event/pan-american-championships-7?section=results&tab&sport=gr', {timeout: 60000});

  // Extract the content of an element (e.g., h1)
  const dom = new JSDOM(htmlString);
  const document = dom.window.document;
  //const text = await page.evaluate(element => element.textContent, element);

  const listItems = document.querySelectorAll('li')

  listItems.forEach(element => {
    if (element.classList.contains('active')){

    }
  });
  
  const itemsArray = Array.from(listItems).map((element) => element.textContent);

})();

console.log('hello world')
