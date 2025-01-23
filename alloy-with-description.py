import pandas as pd

# Load the CSV file
input_file = "alloys_new.csv"
df = pd.read_csv(input_file, encoding="latin1")

# Clean up column names to remove leading/trailing spaces
df.columns = df.columns.str.strip()

# Columns for alloy composition
alloy_composition_columns = ["Al", "Co", "Cr", "Fe", "Ni", "Cu", "Mn", "Ti", "V", "Nb", "Mo", "Zr", "Hf", "Ta"]

# Columns for heat treatment
heat_treatment_columns = ["Homogenization_Temp", "Homogenization_Time", "Annealing_Temp", "Annealing_Time_(min)", "Quenching", "HPR"]

# Function to generate the description for each alloy
def generate_description(row):
    # Start with element composition
    element_composition = [
        f"{element} ({row[element]})"
        for element in alloy_composition_columns
        if not pd.isna(row[element]) and row[element] != 0
    ]
    element_count = len(element_composition)
    description = f"The alloy {row['Alloy']} contains {element_count} elemental compositions: {', '.join(element_composition)}"
    
    # Heat treatment section
    heat_treatment_details = []
    for column in heat_treatment_columns:
        if not pd.isna(row[column]) and row[column] != 0:
            if column == "Homogenization_Temp":
                heat_treatment_details.append(f"undergone homogenization process at {row[column]}°C")
            elif column == "Homogenization_Time":
                heat_treatment_details.append(f"for {row[column]} minutes,")
            elif column == "Annealing_Temp":
                heat_treatment_details.append(f"undergone annealing process at {row[column]}°C")
            elif column == "Annealing_Time_(min)":
                heat_treatment_details.append(f"for {row[column]} minutes,")
            elif column == "Quenching":
                heat_treatment_details.append(f"and undergone quenching process ({row[column]}),")
            elif column == "HPR":
                heat_treatment_details.append(f"with an HPR (Hot Plasticity Ratio) value of {row[column]}")
    
    if heat_treatment_details:
        description += f" and with heat treatment -  {', '.join(heat_treatment_details)},"
    else:
        description += " and without heat treatment,"
    
    # Microstructure and phases
    if not pd.isna(row["Microstructure"]) or not pd.isna(row["Phases"]):
        microstructure = (
            str(row["Microstructure"]).replace("+", "and") if not pd.isna(row["Microstructure"]) else "unspecified"
        )
        phases = row["Phases"] if not pd.isna(row["Phases"]) else "unspecified"
        description += f"showing a {microstructure} microstructure and {phases} phases."
    
    return description

# Apply the function to generate descriptions
df["alloy_description"] = df.apply(generate_description, axis=1)

# Save the updated DataFrame to a new CSV
output_file = "alloys_with_description.csv"
df.to_csv(output_file, index=False, encoding="utf-8")

print(f"Descriptions generated and saved to {output_file}")
