import csv
import matplotlib.pyplot as plt
from numpy.polynomial import polynomial as poly
from utils import min_year, max_year, plot_linear_prediction


def parse_data(filename):
    data = {
        "min_year": None, "max_year": None,
        "farmed": {}, "wild caught": {},
        "consumption": {}, "population": {}
    }

    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        data["min_year"] = min_year(reader.fieldnames)
        data["max_year"] = max_year(reader.fieldnames)

        for row in reader:
            country = row["country code"]
            measure = row["measure"]

            if measure not in data:
                continue

            if country not in data[measure]:
                data[measure][country] = {}

            for year in range(data["min_year"], data["max_year"] + 1):
                value = row.get(str(year), '')

                if value == '':
                    data[measure][country][year] = None
                else:
                    data[measure][country][year] = (
                        int(value) if measure == "population" else float(value)
                    )

    return data


def get_actual_production(data, country_code, year):
    farmed = data["farmed"].get(country_code, {}).get(year, None)
    wild_caught = data["wild caught"].get(country_code, {}).get(year, None)

    if farmed is None and wild_caught is None:
        return None
    return (farmed or 0) + (wild_caught or 0)


def get_production_need(data, country_code, year):
    population = data["population"].get(country_code, {}).get(year, None)
    consumption = data["consumption"].get(country_code, {}).get(year, None)

    if population is None or consumption is None:
        return None
    return (population * consumption) / 1000


def plot_production_vs_consumption(data, country_code):
    years = list(range(data["min_year"], data["max_year"] + 1))
    actua = [get_actual_production(data, country_code, year) for year in years]
    need = [get_production_need(data, country_code, year) for year in years]

    plt.figure(figsize=(10, 5))
    plt.plot(years, actua, label="Actual Production", marker='s')
    plt.plot(years, need, label="Production Need", marker='o')
    plt.xlabel("Year")
    plt.ylabel("Metric Tonnes")
    plt.title(f"Production vs. Need for {country_code}")
    plt.legend()
    plt.savefig(f"{country_code}-prod-vs-need.png")
    plt.close()


def predict_need(data, country_code, predict_years):
    years = []
    values = []

    for year in range(data["min_year"], data["max_year"] + 1):
        need = get_production_need(data, country_code, year)
        if need is not None:
            years.append(year)
            values.append(need)

    if not years:
        return {"years": [], "values": []}

    b, m = poly.polyfit(years, values, 1)

    max_year = data["max_year"]
    predicted_years = list(range(max_year + 1, max_year + predict_years + 1))
    predicted_values = [
        m * year + b for year in predicted_years
    ]

    return {
        "years": years + predicted_years,
        "values": values + predicted_values
    }


def total_production_need(data, years_to_predict):
    total_need = 0
    for country in data["population"]:
        prediction = predict_need(data, country, years_to_predict)
        if prediction["values"]:
            total_need += prediction["values"][-1]
    return total_need


if __name__ == "__main__":
    data = parse_data("large.csv")
    plot_production_vs_consumption(data, "USA")
    plot_linear_prediction(data, "USA")
    total_need = total_production_need(data, 50)
    print(f"Metric tonnes of seafood needed to be produced in 50 years: "
          f"{total_need:,.3f}")
