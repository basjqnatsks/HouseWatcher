import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
df = pd.read_csv("out2.csv")
df.drop(df[df['Party'] == 'libertarian'].index, inplace=True)
df['TradeDate'] = pd.to_datetime(df['TradeDate'], errors='coerce')
df['SaleDate'] = pd.to_datetime(df['SaleDate'], errors='coerce')
df['TotalReturnPct'] = pd.to_numeric(df['TotalReturnPct'], errors='coerce')
df['daysHeld'] = (df['SaleDate'] - df['TradeDate']).dt.days
df = df[df['daysHeld'] > 0]
df['TotalReturnDecimal'] = df['TotalReturnPct'] 
df['annualized_return'] = (df['TotalReturnDecimal'] / df['daysHeld']) * 365
df.dropna(subset=['annualized_return', 'Party'], inplace=True)
grouped = df.groupby('Party')['annualized_return']
summary_stats = grouped.describe()
print("Summary Statistics of Linear-Annualized Returns by Party:")
print(summary_stats)
party_arrays = []
unique_parties = df['Party'].unique()
for party in unique_parties:
    returns_for_party = df.loc[df['Party'] == party, 'annualized_return'].values
    party_arrays.append(returns_for_party)
if len(party_arrays) > 1:
    f_stat, p_val = stats.f_oneway(*party_arrays)
    print("\nOne-Way ANOVA on Annualized Return (Linear Approx):")
    print(f"F-statistic: {f_stat:.4f}")
    print(f"p-value: {p_val:.6f}")
    if p_val < 0.05:
        print("=> Reject null hypothesis: At least one party differs in mean annualized return.")
    else:
        print("=> Fail to reject null hypothesis: No significant difference among parties.")
else:
    print("\nNot enough distinct party groups to run ANOVA.")
plt.figure(figsize=(8,6))
sns.boxplot(x='Party', y='annualized_return', data=df)
plt.title("Distribution of Annualized Returns (Linear) by Party")
plt.xlabel("Party")
plt.ylabel("Approx Annualized Return")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
mean_returns = df.groupby('Party')['annualized_return'].mean().reset_index()
plt.figure(figsize=(8,6))
sns.barplot(data=mean_returns, x='Party', y='annualized_return')
plt.title("Mean Annualized Returns (Linear) by Party")
plt.xlabel("Party")
plt.ylabel("Avg Annualized Return")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()