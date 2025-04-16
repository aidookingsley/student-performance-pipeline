import pandas as pd
import os

def load_and_transform(input_dir="data", output_dir="output"):
    # Load the CSVs
    mat_path = os.path.join(input_dir, "student-mat.csv")
    por_path = os.path.join(input_dir, "student-por.csv")

    mat_df = pd.read_csv(mat_path, sep=';')
    por_df = pd.read_csv(por_path, sep=';')

    print(f"Math dataset shape: {mat_df.shape}")
    print(f"Portuguese dataset shape: {por_df.shape}")
    # Subject label for each context
    mat_df["subject"] = "Math"
    por_df["subject"] = "Portuguese"

    # Combining datasets
    combined_df = pd.concat([mat_df, por_df], ignore_index=True)

    # Create average grade
    combined_df["G_avg"] = combined_df[["G1", "G2", "G3"]].mean(axis=1)

    # Create pass/fail flag (pass if G3 >= 10)
    combined_df["pass"] = combined_df["G3"] >= 10

    # Columns to not appear in final output
    combined_df = combined_df.drop(columns=["school", "guardian"])

    # Save the transformed dataset
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    output_path = os.path.join(output_dir, "transformed_students.csv")
    combined_df.to_csv(output_path, index=False)
    print(f"\n Transformed data saved to: {output_path}")

if __name__ == "__main__":
    load_and_transform()
