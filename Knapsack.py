import numpy as np
import pandas as pd

def knapsack(w, c, K):
    n = len(w)
    S = np.zeros((n, K+1), dtype=int)  # binary matrix to store the items taken
    v = np.zeros((n, K+1), dtype=int)

    for i in range(n):
        for k in range(1, K+1):  # Start from 1 to avoid indexing issues
            if w[i] > k:
                v[i, k] = v[i-1, k] if i > 0 else 0  # Handle boundary condition for i=0
            else:
                if i > 0:
                    if c[i] + v[i-1, k-w[i]] > v[i-1, k]:
                        v[i, k] = c[i] + v[i-1, k-w[i]]
                        S[i, k] = 1  # take the item
                    else:
                        v[i, k] = v[i-1, k]
                else:
                    v[i, k] = c[i]  # Only take the current item if i=0
                    S[i, k] = 1

    k = K
    x_star = np.array([], dtype=int)  # to store the items taken
    for i in range(n-1, -1, -1):  
        if S[i, k] == 1:
            x_star = np.hstack([x_star,i])  # take the item
            k -= w[i]

    return x_star, v[n-1, K],v,S  # return the items taken and the value of the knapsack

def greedy(w, c, K):
    n = len(w)
    ratio = c / w
    idx = np.argsort(-c)  # sort indices based on value-to-weight ratio  THIS IS INTERSETINg
    # if we sort based on the ratio, we get the same as the knapsack optimization
    # if we sort based on the value (c) alone, then it is worse than the knapsack.

    total_value = 0
    x_star = np.array([], dtype=int)  # to store the items taken
    i = 0
    while(K > 0):
        total_value += c[idx[i]]  # add the value of the item
        x_star = np.hstack([x_star,idx[i]])
        K -= w[idx[i]]
        i += 1

    return x_star, total_value
def greedy_ratio(w, c, K):
    n = len(w)
    ratio = c / w
    idx = np.argsort(-ratio)  # sort indices based on value-to-weight ratio  THIS IS INTERSETINg
    # if we sort based on the ratio, we get the same as the knapsack optimization
    # if we sort based on the value (c) alone, then it is worse than the knapsack.

    total_value = 0
    x_star = np.array([], dtype=int)  # to store the items taken
    i = 0
    while(K > 0):
        total_value += c[idx[i]]  # add the value of the item
        x_star = np.hstack([x_star,idx[i]])
        K -= w[idx[i]]
        i += 1

    return x_star, total_value

w = np.array([7,4,2,2,3,4,7,5,4,3,2,3,2,2,2,7,3,2,1,4,4,1,4,7,6,7,2], dtype=int)
c = 1000 * np.array([16,1,7,14,6,10,12,18,5,11,6,13,18,5,17,17,7,12,14,9,9,6,3,6,12,8,19], dtype=int)

# variables
K = 40 # maximum time for work in a day (5 hours for 8 workers)
x_star_knapsack, total_value_knap, v,S = knapsack(w, c, 40)     # knapsack optimization
x_star_greed, total_value_greedy = greedy(w, c, 40)                    # greedy optimization
x_star_greed_ratio, total_value_greedy_ratio = greedy_ratio(w, c, 40)        # greedy optimization with value-to-weight ratio

print("Items taken:", x_star_knapsack)
print("Value of the knapsack:", total_value_knap)

v = np.transpose(v)
S = np.transpose(S)  # transpose the matrices to get the correct shape

v = np.concatenate((np.arange(0, len(v)).reshape(-1, 1), v), axis=1)  # add the first column with the number of items taken
S = np.concatenate((np.arange(0, len(S)).reshape(-1, 1), S), axis=1)  # add the first column with the number of items taken

print("V matrix:", v)
print("S matrix:", S)

df = pd.DataFrame(v, columns=['Weight','item 1', 'item 2', 'item 3', 'item 4', 'item 5', 'item 6', 'item 7', 'item 8', 'item 9', 'item 10', 'item 11', 'item 12', 'item 13', 'item 14', 'item 15', 'item 16', 'item 17', 'item 18', 'item 19', 'item 20','item 21', 'item 22', 'item 23', 'item 24', 'item 25', 'item 26','item 27'])
df2 = pd.DataFrame(S, columns=['Weight','item 1', 'item 2', 'item 3', 'item 4', 'item 5', 'item 6', 'item 7', 'item 8', 'item 9', 'item 10', 'item 11', 'item 12', 'item 13', 'item 14', 'item 15', 'item 16', 'item 17', 'item 18', 'item 19', 'item 20','item 21', 'item 22', 'item 23', 'item 24', 'item 25', 'item 26','item 27'])

# Step 3: Save the DataFrame as a CSV file
df.to_csv('KnapsackProblem\\value_matrix.csv', index=False)
df2.to_csv('KnapsackProblem\\selection_matrix.csv', index=False)

print("Matrix saved as 'matrix_table.csv'")

idx = np.argsort(x_star_greed)
x_star_greed = x_star_greed[idx]
print("Greedy Items taken:", x_star_greed)
print("Greedy Value of the knapsack:", total_value_greedy)

idx = np.argsort(x_star_greed_ratio)
x_star_greed_ratio = x_star_greed_ratio[idx]
print("Greedy Ratio Items taken:", x_star_greed_ratio)
print("Greedy Ratio Value of the knapsack:", total_value_greedy_ratio)

idx = np.argsort(x_star_knapsack)  # sort indices based on value-to-weight ratio
x_star_knapsack = x_star_knapsack[idx]  # sort the items taken

idx = np.argsort(x_star_greed)
x_star_greed = x_star_greed[idx]  # sort the items taken

print(f"Value of Knapsack = {total_value_knap}, Sorted Items taken (knapsack): {x_star_knapsack}")
print(f"Value of Greedy = {total_value_greedy}, Sorted Items taken (greedy): {x_star_greed}")
print(f"Value of Greedy Ratio = {total_value_greedy_ratio}, Sorted Items taken (greedy ratio): {x_star_greed_ratio}")