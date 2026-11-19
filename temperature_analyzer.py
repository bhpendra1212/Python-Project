from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# Load data from CSV file
def load_data():
    csv_path = Path(__file__).parent / "temps.csv"
    data = pd.read_csv(csv_path)

    # Save raw values so invalid text (e.g., 'hot') is printed accurately
    raw_temps = data["Temp_C"].copy()
    data["Temp_C"] = pd.to_numeric(data["Temp_C"], errors="coerce")

    invalid = data[data["Temp_C"].isna()]

    for idx, row in invalid.iterrows():
        print(f"Invalid reading {raw_temps.loc[idx]} on {row['Date']}. Value ignored (NaN).")

    data = data.dropna(subset=["Temp_C"])
    return data


# Calculate temperature statistics and hot days (Matches Test Cases 1 & 2)
def show_statistics(data):
    temps = data["Temp_C"].to_numpy()

    if len(temps) == 0:
        print("No valid temperature data.")
        return

    print(
        f"Mean: {np.mean(temps):.2f} | Median: {np.median(temps):.2f} | "
        f"Max: {np.max(temps):.0f} | Min: {np.min(temps):.0f} | Std Dev: {np.std(temps):.2f}"
    )
    find_hot_days(data)


# Find days above 35 C
def find_hot_days(data):
    hot_days = data[data["Temp_C"] > 35]

    if hot_days.empty:
        print("No days above 35 C")
    else:
        days_str = ", ".join(hot_days["Date"].astype(str))
        print(f"Hot days: {days_str}")


# Convert Celsius to Fahrenheit and plot line chart (Matches Test Case 4)
def convert_to_fahrenheit(data):
    if data.empty:
        print("No valid temperature data.")
        return

    fahrenheit = data["Temp_C"] * 9 / 5 + 32
    formatted_f = " | ".join(f"{temp:.2f} F" for temp in fahrenheit)
    print(formatted_f)

    plot_line_chart(data)


# Create line chart
def plot_line_chart(data):
    plt.figure(figsize=(8, 4))
    plt.plot(data["Date"], data["Temp_C"], marker="o")
    plt.title("Temperature Over Time")
    plt.xlabel("Date")
    plt.ylabel("Temperature (C)")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()


# Create histogram (Satisfies Bare Minimum Requirement #5)
def plot_histogram(data):
    plt.figure(figsize=(8, 4))
    plt.hist(data["Temp_C"], bins=5, edgecolor="black")
    plt.title("Temperature Histogram")
    plt.xlabel("Temperature (C)")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.show()


# Main menu
def main():
    data = load_data()

    while True:
        print("\n--- Temperature Data Analyzer ---")
        print("1. Show Statistics")
        print("2. Find Hot Days")
        print("3. Convert to Fahrenheit and Plot")
        print("4. Plot Histogram")
        print("5. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            show_statistics(data)

        elif choice == "2":
            find_hot_days(data)

        elif choice == "3":
            convert_to_fahrenheit(data)

        elif choice == "4":
            plot_histogram(data)

        elif choice == "5":
            print("Program closed.")
            break

        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()