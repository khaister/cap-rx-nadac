# The National Average Drug Acquisition Cost (NADAC) comparison dataset
# tracks per unit drug price changes over time. Please write a short
# Python program to retrieve this data and report on the 10 largest per
# unit price increases and 10 largest per unit price decreases with
# effective dates in 2022. Duplicate description, price change entries
# should be eliminated. The program should be implemented in Python
# without using pandas and should run successfully on CoderPad. The
# solution should be performant and memory efficient.
#
# The program output should be formatted as follows:
#
# Top 10 NADAC per unit price increases of 2022:
# $1261.36: STELARA 90 MG/ML SYRINGE
# $594.44: SIMPONI 50 MG/0.5 ML PEN INJEC
# ...
#
# Top 10 NADAC per unit price decreases of 2022:
# -$61.36: PROAIR DIGIHALER 90 MCG INHALR
# -$56.64: SKYRIZI 150 MG/ML PEN
# ...
#
# More information about the dataset can be found here:
# https://data.medicaid.gov/dataset/a217613c-12bc-5137-8b3a-ada0e4dad1ff
# and in appendix 6 here:
# https://www.medicaid.gov/medicaid-chip-program-information/by-topics/prescription-drugs/ful-nadac-downloads/nadacmethodology.pdf
#
# Your program should request the dataset from
# https://download.medicaid.gov/data/nadac-comparison-02-01-2023.csv
# and can expect the data to be in this csv format:
#
# NDC Description,NDC,Old NADAC Per Unit,New NADAC Per Unit,Classification for Rate Setting,Percent Change,Primary Reason,Start Date,End Date,Effective Date
# AMOXICILLIN 200 MG/5 ML SUSP,00093416073,0.03051,0.02509,G,-17.76,Survey Rate,12/14/2022,12/21/2022,12/21/2022
# IBUPROFEN 200 MG SOFTGEL,00536114730,0.07853,0.08730,G,11.17,Survey Rate,12/14/2022,12/21/2022,12/21/2022
# ACETAMINOPHEN 325 MG TABLET,00904671960,0.02468,0.02209,G,-10.49,Survey Rate,12/14/2022,12/21/2022,12/21/2022

import contextlib
import csv
from decimal import Decimal

import requests


def format_dollar_amount(amount: Decimal):
    if amount < 0:
        return f"-${abs(amount)}"
    return f"${amount}"


def parse_nadac_data(chunk_size: int):
    """
    Parse NADAC Weekly Comparison data.

    :param chunk_size: int, size of the chunk in byte to read from the stream
    :return: dict, NDC Description to per unit price change
    """
    url = "https://download.medicaid.gov/data/nadac-comparison-02-01-2023.csv"

    with contextlib.closing(requests.get(url, stream=True)) as stream:
        data = {}

        lines = (line.decode('utf-8') for line in stream.iter_lines(chunk_size))
        reader = csv.reader(lines, delimiter=',', quotechar='"')
        for row in reader:
            # skip header
            if row[0] == "NDC Description":
                continue

            # calculate per unit price change
            description = row[0]
            old_nadac = Decimal(row[2])
            new_nadac = Decimal(row[3])
            unit_price_change = new_nadac - old_nadac

            # update data
            data.update({description: unit_price_change})

        return data


def print_top_10s(data: dict):
    """Print top 10 price increases and decreases."""
    data_by_price_change = sorted(data.items(), key=lambda x: x[1], reverse=True)
    top_10_increases = data_by_price_change[:10]
    top_10_decreases = data_by_price_change[-10:]

    print("Top 10 NADAC per unit price increases of 2023:")
    for description, price_change in top_10_increases:
        print(f"{format_dollar_amount(price_change)}: {description}")

    print("\nTop 10 NADAC per unit price decreases of 2023:")
    for description, price_change in top_10_decreases:
        print(f"{format_dollar_amount(price_change)}: {description}")


if __name__ == "__main__":
    chunk_size = 1024 * 1024 * 10  # 10MB
    data = parse_nadac_data(chunk_size)
    print_top_10s(data)