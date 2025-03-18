package main

import (
	"encoding/csv"
	"fmt"
	"log"
	"os"
	"sync"

	"github.com/gocolly/colly"
)

type Product struct {
	Url, Image, Name, Price string
}

func main() {

	var products []Product

	var visitedUrls sync.Map

	c := colly.NewCollector(
		colly.AllowedDomains("www.scrapingcourse.com"),
	)

	c.OnRequest(func(r *colly.Request) {
		fmt.Println("Visiting: ", r.URL)
	})

	c.OnError(func(_ *colly.Response, err error) {
		fmt.Println("Something went wrong: ", err)
	})

	c.OnResponse(func(r *colly.Response) {
		fmt.Println("Page visited: ", r.Request.URL)
	})

	c.OnHTML("li.product", func(e *colly.HTMLElement) {

		product := Product{}

		product.Url = e.ChildAttr("a", "href")
		product.Image = e.ChildAttr("img", "src")
		product.Name = e.ChildText(".product-name")
		product.Price = e.ChildText(".price")

		products = append(products, product)

	})

	c.OnHTML("a.next", func(e *colly.HTMLElement) {

		nextPage := e.Attr("href")

		if _, found := visitedUrls.Load(nextPage); !found {
			fmt.Println("scraping:", nextPage)
			visitedUrls.Store(nextPage, struct{}{})
			e.Request.Visit(nextPage)
		}
	})

	c.OnScraped(func(r *colly.Response) {

		file, err := os.Create("products.csv")
		if err != nil {
			log.Fatalln("Failed to create output CSV file", err)
		}
		defer file.Close()

		writer := csv.NewWriter(file)

		headers := []string{
			"Url",
			"Image",
			"Name",
			"Price",
		}

		writer.Write(headers)

		for _, product := range products {
			record := []string{
				product.Url,
				product.Image,
				product.Name,
				product.Price,
			}

			writer.Write(record)
		}

		defer writer.Flush()

		fmt.Println(r.Request.URL, " scraped!")
	})

	c.Visit("https://www.scrapingcourse.com/ecommerce")
}
