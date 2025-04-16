import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Ensure output directory exists
os.makedirs("output", exist_ok=True)

# Load transformed data
df = pd.read_csv("output/transformed_students.csv")

# Helper to save and clear plot
def save_and_clear(name):
    plt.savefig(f"output/{name}.png")
    plt.show()
    plt.clf()

# Grade distributions
sns.histplot(df['G_avg'], bins=20, kde=True)
plt.title("Average Grade Distribution")
plt.xlabel("Average Grade")
plt.ylabel("Frequency")
save_and_clear("average_grade_distribution")

# Pass/Fail distribution
sns.countplot(x='pass', data=df)
plt.title("Pass/Fail Distribution")
plt.xlabel("Pass")
plt.ylabel("Count")
save_and_clear("pass_fail_distribution")

# Correlation heatmap
sns.heatmap(df.corr(numeric_only=True), annot=True, fmt=".2f", cmap='coolwarm', square=True)
plt.title("Correlation Heatmap")
save_and_clear("correlation_heatmap")

# Study Time vs Final Grade
sns.scatterplot(x='studytime', y='G3', data=df)
plt.title("Study Time vs Final Grade (G3)")
plt.xlabel("Study Time")
plt.ylabel("Final Grade (G3)")
save_and_clear("study_time_vs_final_grade")

# Study Time vs Average Grade
sns.scatterplot(x='studytime', y='G_avg', data=df)
plt.title("Study Time vs Average Grade")
plt.xlabel("Study Time")
plt.ylabel("Average Grade")
save_and_clear("study_time_vs_average_grade")

# Pass rate by subject
pass_rate = df.groupby('subject')['pass'].mean().reset_index()
sns.barplot(x='subject', y='pass', data=pass_rate)
plt.title("Pass Rate by Subject")
plt.xlabel("Subject")
plt.ylabel("Pass Rate")
save_and_clear("pass_rate_by_subject")

# Pass rate by study time
study_time_pass_rate = df.groupby('studytime')['pass'].mean().reset_index()
sns.barplot(x='studytime', y='pass', data=study_time_pass_rate)
plt.title("Pass Rate by Study Time")
plt.xlabel("Study Time")
plt.ylabel("Pass Rate")
save_and_clear("pass_rate_by_study_time")

# Pass rate by family size
family_size_pass_rate = df.groupby('famsize')['pass'].mean().reset_index()
sns.barplot(x='famsize', y='pass', data=family_size_pass_rate)
plt.title("Pass Rate by Family Size")
plt.xlabel("Family Size")
plt.ylabel("Pass Rate")
save_and_clear("pass_rate_by_family_size")

# Pass rate by internet access
internet_pass_rate = df.groupby('internet')['pass'].mean().reset_index()
sns.barplot(x='internet', y='pass', data=internet_pass_rate)
plt.title("Pass Rate by Internet Access")
plt.xlabel("Internet Access")
plt.ylabel("Pass Rate")
save_and_clear("pass_rate_by_internet_access")

# Pass rate by romantic relationship
romantic_pass_rate = df.groupby('romantic')['pass'].mean().reset_index()
sns.barplot(x='romantic', y='pass', data=romantic_pass_rate)
plt.title("Pass Rate by Romantic Relationship")
plt.xlabel("Romantic Relationship")
plt.ylabel("Pass Rate")
save_and_clear("pass_rate_by_romantic_relationship")


# Pass rate by age
age_pass_rate = df.groupby('age')['pass'].mean().reset_index()
sns.barplot(x='age', y='pass', data=age_pass_rate)
plt.title("Pass Rate by Age")
plt.xlabel("Age")
plt.ylabel("Pass Rate")
save_and_clear("pass_rate_by_age")

# Pass rate by address
address_pass_rate = df.groupby('address')['pass'].mean().reset_index()
sns.barplot(x='address', y='pass', data=address_pass_rate)
plt.title("Pass Rate by Address")
plt.xlabel("Address")
plt.ylabel("Pass Rate")
save_and_clear("pass_rate_by_address")

# Pass rate by gender
gender_pass_rate = df.groupby('gender')['pass'].mean().reset_index()
sns.barplot(x='gender', y='pass', data=gender_pass_rate)
plt.title("Pass Rate by Gender")
plt.xlabel("Gender")
plt.ylabel("Pass Rate")
save_and_clear("pass_rate_by_gender")
