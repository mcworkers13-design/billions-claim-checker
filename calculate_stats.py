import csv
import numpy as np

def main():
    amounts = []
    
    with open('claims_detailed.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            amounts.append(float(row['Amount BILL']))
            
    amounts = np.array(amounts)
    
    total_bill = np.sum(amounts)
    count = len(amounts)
    mean_val = np.mean(amounts)
    median_val = np.median(amounts)
    min_val = np.min(amounts)
    max_val = np.max(amounts)
    
    print("--- ALLOCATION STATISTICS ---")
    print(f"Total Claims Analyzed: {count:,}")
    print(f"Total BILL Allocated:  {total_bill:,.2f} BILL")
    print(f"Average Allocation:    {mean_val:,.2f} BILL")
    print(f"Median Allocation:     {median_val:,.2f} BILL")
    print(f"Minimum Allocation:    {min_val:,.2f} BILL")
    print(f"Maximum Allocation:    {max_val:,.2f} BILL")
    
    # Distribution Brackets
    brackets = [
        (">= 1,000,000 BILL", lambda x: x >= 1000000),
        ("500,000 - 999,999 BILL", lambda x: (x >= 500000) & (x < 1000000)),
        ("100,000 - 499,999 BILL", lambda x: (x >= 100000) & (x < 500000)),
        ("10,000 - 99,999 BILL", lambda x: (x >= 10000) & (x < 100000)),
        ("1,000 - 9,999 BILL", lambda x: (x >= 1000) & (x < 10000)),
        ("500 - 999 BILL", lambda x: (x >= 500) & (x < 1000)),
        ("100 - 499 BILL", lambda x: (x >= 100) & (x < 500)),
        ("< 100 BILL", lambda x: x < 100)
    ]
    
    print("\n--- DISTRIBUTION BRACKETS ---")
    print(f"{'Bracket':<30} | {'Count':<10} | {'Percentage':<10} | {'Total BILL':<18}")
    print("-" * 78)
    for label, cond in brackets:
        bracket_amounts = amounts[cond(amounts)]
        bracket_count = len(bracket_amounts)
        bracket_pct = (bracket_count / count) * 100
        bracket_sum = np.sum(bracket_amounts)
        print(f"{label:<30} | {bracket_count:<10,} | {bracket_pct:>8.2f}% | {bracket_sum:>15,.2f} BILL")

if __name__ == "__main__":
    main()
