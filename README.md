# amazon-products-scraper
a rudimentary python script to generate a list of amazon products based on selenium and beautifulsoup
I made this for a game I was intending to make

The idea is to run this on a headless server and let it gather amazon product links, prices, and images.

How it works:

1) Picks a random product category
2) Gets links of all products on that page
3) Saves it to csv file
4) Opens one link randomly
5) Repeat from step 2


You will need to import your own broser session keys. 
