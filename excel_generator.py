import pandas as pd

data = [
    {
        "Name": "John Catamora",
        "Date": "2023-10-01",
        "Department": "Sales",
        "Time-In": "09:00 AM",
        "Time-Out": "05:00 PM"
    },
    {
        "Name": "Jane Smith",
        "Date": "2023-10-01",
        "Department": "Marketing",
        "Time-In": "09:30 AM",
        "Time-Out": "05:30 PM"
    },
    {
        "Name": "Alice Johnson",
        "Date": "2023-10-01",
        "Department": "HR",
        "Time-In": "09:00 AM",
        "Time-Out": "05:00 PM"
    }
]

data2 = [
    {
        "Name": "Bob Brown",
        "Date": "2023-10-01",
        "Department": "IT",
        "Time-In": "10:00 AM",
        "Time-Out": "06:00 PM"
    },
    {
        "Name": "Charlie Davis",
        "Date": "2023-10-01",
        "Department": "Finance",
        "Time-In": "09:00 AM",
        "Time-Out": "05:00 PM"
    },
    {
        "Name": "David Wilson",
        "Date": "2023-10-01",
        "Department": "Operations",
        "Time-In": "08:30 AM",
        "Time-Out": "04:30 PM"
    }
]

def main():
    df_regular = pd.DataFrame(data)
    df_contractual = pd.DataFrame(data2)

    out_path = "export.xlsx"
    with pd.ExcelWriter(out_path, engine="xlsxwriter") as writer:
        df_regular.to_excel(writer, index=False, sheet_name="Regular")
        df_contractual.to_excel(writer, index=False, sheet_name="Contractual")

    print(f"Saved: {out_path}")

if __name__ == "__main__":
    main()
