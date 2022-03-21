## P02 - Nearest Neighbor with UFO's
### Sharome Burton
### Description:

This notebook calculates the distance from each city provided in a data file to each other city by loading .csv and .geojson data files into geopandas geoseries spatial indices. It also calculates the average distance of the closest 100 UFO sightings to the city. New .json files are created by this script, storing the calculated information in an easily retrievable form.
<!-- <a href="https://gist.github.com/koulkoudakis/a36d00c830c5ba166335fe66d3afbf06"><img src="img/P01.jpg" width="800"></a> -->


### Files

|   #   | File            | Description                                        |
| :---: | --------------- | -------------------------------------------------- |
|   1   | `P02_SB.ipynby`  | Notebook showing process of creating required files     |
|   2   | `cities.geojson` | Contains info and geospatial data of cities     |
|   3   | `ufo_data.csv`  | Contains geospatial info on thousands of UFO sightings       |
|   4   | `CityDistanceFile.json`  | Output file. Contains distances between cities      |
|   5   | `UFOAvgDistanceFile.json` | Output file. Contains average distance between city and 100 closest UFO sightings|

### Instructions

- Head to <a href ="https://colab.research.google.com/drive/15RnaTYS7WQjFzzb90uILeiiwg5dPEV57?usp=sharing"> Google Colab notebook for this project (P02_SB.ipynby) </a>
- Upload .json and .csv files to working directory on Google Colab
- Runtime -> Run all
- Alternatively, just view the output from my previous session of the notebook
