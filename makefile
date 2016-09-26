# to do
# convert census-tracts .shp to topojson, and merge topojson with ia-tracts

# topojson
data/processed/maps/2014-tracts.json: data/processed/maps/tracts.json data/processed/populations/ia-tracts-2014.csv
	topojson -e data/processed/populations/ia-tracts-2014.csv \
	--id-property GEOID,FIPS \
	-p hisp_pop=+hisp_pop,hisp_perc=+hisp_perc,total_pop=+tototal_pop,name=Name \
	-o data/processed/maps/2014-tracts.json \
	-- \
	data/processed/maps/tracts.json

# OGR2OGR (shp -> geojson)
data/processed/maps/tracts.json: data/external/maps/tracts/tl_2014_19_tract.shp
	ogr2ogr -f GeoJSON \
	data/processed/maps/tracts.json \
	data/external/maps/tracts/tl_2014_19_tract.shp

# Download census tracts.zip



#===| Data Processing |===#

# Create the counties data
data/processed/populations/ia-hisp-counties.csv: src/format-counties.py
	python src/format-counties.py

# Prepare census tract data from american community survey results
data/processed/populations/ia-tracts-2014.csv: data/external/census-tracts/ACS_14_5YR_DP05.csv src/format-tracts.py
	python src/format-tracts.py
