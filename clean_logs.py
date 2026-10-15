#
## This script reads a raw weather station log "environmental_raw.txt" line-by-line, removes broken records,
## converts valid temperatures from Fahrenheit to Celsius, and writes the cleaned data 
## to a "environmental_clean.csv" file while printing how many invalid lines were skipped.
#

# Function to convert temperature in Farenheit to Celcius.

def celsius_converter(f_temp):
    fahrenheit = float(f_temp)
    celsius = (fahrenheit - 32) * 5 / 9
    return round(celsius, 2)

# Function to clean the raw data. 

def parse_and_clean(line):

    if not line.strip():
        return None

##Splitting by delimiter |.
    parts = line.split("|")

## For missing data or delimiters.
    if len(parts) != 5:
        return None

    cleaned_parts = []

    for part in parts:
        cleaned_parts.append(part.strip())

## Assigning variables.
    timestamp = cleaned_parts[0]
    station_id = cleaned_parts[1]
    temperature = cleaned_parts[2]
    humidity = cleaned_parts[3]
    sensor_status = cleaned_parts[4]

## Removing broken records.
    if (
        not timestamp
        or not station_id
        or not temperature
        or not humidity
        or not sensor_status
    ):
        return None

    if sensor_status != "ACTIVE":
        return None

    if temperature == "ERROR" or temperature == "N/A":
        return None

    return timestamp, station_id, temperature, humidity, sensor_status


# Assigning names for input and output files.
input_file = "environmental_raw.txt"
output_file = "environmental_clean.csv"


# Adding skipped lines counter.
skipped_lines = 0

# Writing resilts to an output .csv file.
with open(input_file, "r") as infile, open(output_file, "w") as outfile:

    outfile.write("Timestamp,StationID,Temp(C),Humidity(%),Sensor_Status\n")

    for line in infile:

        cleaned = parse_and_clean(line)
        
## Counting skipped lines.
        if cleaned is None:
            skipped_lines += 1
            continue

        timestamp, station_id, temperature, humidity, sensor_status = cleaned

        temperature_c = celsius_converter(temperature)

        outfile.write(
            f"{timestamp},{station_id},{temperature_c},"
            f"{humidity},{sensor_status}\n"
        )

# Printing count of skipped lines.
print(f"Corrupted lines skipped: {skipped_lines}")
