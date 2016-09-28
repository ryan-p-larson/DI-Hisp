#===| Mapping |===#

#create topojson with the county populations embedded
#data/processed/maps/county-populations.json: data/processed/maps/counties.json data/processed/populations/ia-hisp-counties.csv
#	topojson



data/processed/maps/counties.json:
	ogr2ogr -f GeoJSON \
	-where "STATEFP IN ('19')" \
	data/processed/maps/counties.json \
	data/external/maps/counties/tl_2014_us_county.shp

# Create census tracts hispanic population
data/processed/maps/2014-tracts.json: data/processed/maps/tracts.json data/processed/populations/ia-tracts-2014.csv
	topojson -e data/processed/populations/ia-tracts-2014.csv \
	--id-property GEOID,FIPS \
	-p hisp_pop=+hisp_pop,hisp_perc=+hisp_perc,total_pop=+tototal_pop,name=Name \
	-o data/processed/maps/2014-tracts.json \
	-- \
	data/processed/maps/tracts.json

# Create census tracts GeoJSON
data/processed/maps/tracts.json: data/external/maps/tracts/tl_2014_19_tract.shp
	ogr2ogr -f GeoJSON \
	data/processed/maps/tracts.json \
	data/external/maps/tracts/tl_2014_19_tract.shp



# Download census tracts.zip
# download census counties


#===| Data Processing |===#

#create the election data
data/processed/elections/election.csv data/processed/elections/election-populations.csv: src/format-elections.py
	python src/format-elections.py

# Create the counties data
data/processed/populations/ia-hisp-counties.csv: src/format-counties.py
	python src/format-counties.py

# Prepare census tract data from american community survey results
data/processed/populations/ia-tracts-2014.csv: data/external/census-tracts/ACS_14_5YR_DP05.csv src/format-tracts.py
	python src/format-tracts.py
