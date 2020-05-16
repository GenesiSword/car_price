# car_price
Web Scraping and predicting car price with use of neural network.

car_price repository allows to:
- Scrap data from famous Polish website with cars offers. The following variables about car can be obtain:
  year of production,
  capacity,
  mileage,
  fuel type,
  car brand name,
  car name.
  
- Export these data to .csv file.
- Based on scraped data create ANN algorithm to predict car price.
- Predict car price for given values of variables.

To run and manage program correctly is used mainbody.py file with GUI structure.
Precise description of modules use can be found in docstrings and "#" comments.

Project include following files:
- cardata.py -> Module reponsible for calculations.
- mainbody.py -> GUI structure.
- webminer.py -> Module responsible for scraping data from website.
- requirements.txt -> File with additional packages names needed to run scripts correctly.
