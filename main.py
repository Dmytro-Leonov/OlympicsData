import pandas
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def separate_man_woman(df: pandas.DataFrame):
    men = []
    women = []
    for athletes in df["Athletes"]:
        splitted_athletes = athletes.replace(",", "").split(" ")
        if "(all men)" in athletes:
            men.append(splitted_athletes[0])
            women.append(0)
        elif "(" in athletes:
            men.append(splitted_athletes[1][1:])
            women.append(splitted_athletes[-2])
        else:
            men.append(np.nan)
            women.append(np.nan)
    df["Men"] = men
    df["Women"] = women
    df["Athletes"] = df["Athletes"].apply(lambda x: x.replace(",", "").split(" ")[0])


def separate_events(df: pandas.DataFrame):
    events = []
    sports = []
    disciplines = []
    for event in df["Events"]:
        splitted_events = event.split(" ")
        events.append(splitted_events[0])
        sports.append(splitted_events[2])
        if "(" in event:
            disciplines.append(splitted_events[-2][1:])
        else:
            disciplines.append(np.nan)
    df["Events"] = events
    df["Sports"] = sports
    df["Disciplines"] = disciplines


def main():
    summer_df = pd.read_json("summer_olympics_data.json")
    winter_df = pd.read_json("winter_olympics_data.json")
    df = pd.concat([summer_df, winter_df])
    df.drop(columns=["Motto", "Cauldron", "Closed by", "Opened by"], inplace=True)
    df.replace(to_replace=["nan", "TBA"], value=np.nan, inplace=True)
    df.dropna(inplace=True)
    # cleaning data
    # convert dates
    df["Opening"] = df["Year"].astype(str) + " " + df["Opening"]
    df["Closing"] = df["Year"].astype(str) + " " + df["Closing"]
    df["Opening"] = pd.to_datetime(df["Opening"], infer_datetime_format=True)
    df["Closing"] = pd.to_datetime(df["Closing"], infer_datetime_format=True)
    # clean cities and countries
    df["Host city"] = df["Host city"].apply(lambda x: f'{x.split(", ")[0]}, {x.split(", ")[-1]}')
    # clean nations
    df["Nations"] = df["Nations"].apply(lambda x: x.split(" ")[0])
    # separate total and men/women
    separate_man_woman(df)
    # separate events
    separate_events(df)
    # convert dtypes
    for header in ["Nations", "Athletes", "Events", "Men", "Women", "Sports", "Disciplines"]:
        df[header] = pd.to_numeric(df[header], errors="coerce")
    df = df.convert_dtypes(infer_objects=True)
    # write to csv
    df.to_csv("olympic.csv", index=False)
    plt.figure(figsize=(11, 7), dpi=100)
    summer_years, summer_athletes = df[df["Kind"] == "Summer"]["Year"], df[df["Kind"] == "Summer"]["Athletes"]
    winter_years, winter_athletes = df[df["Kind"] == "Winter"]["Year"], df[df["Kind"] == "Winter"]["Athletes"]
    plt.plot(summer_years, summer_athletes, "r-", winter_years, winter_athletes, "b-",
             summer_years, summer_athletes, "ro", winter_years, winter_athletes, "bo",
             linewidth=2,)
    plt.legend(["Summer Olympics", "Winter Olympics"])
    plt.title("Number of athletes for every Olympic")
    plt.xlabel("Years")
    plt.ylabel("Athletes")
    plt.xticks(range(min(df["Year"]), max(df["Year"]) + 1, 2), rotation="vertical")
    plt.grid()
    plt.show()


if __name__ == "__main__":
    main()
