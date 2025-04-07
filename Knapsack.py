import numpy as np

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
x_star_knapsack, total_value_knap, v,S = knapsack(w, c, 40)

print("Items taken:", x_star_knapsack)
print("Value of the knapsack:", total_value_knap)

print("V matrix:", v)
print("S matrix:", S)

x_star_greed, total_value = greedy(w, c, 40)
print("Greedy Items taken:", x_star_greed)
print("Greedy Value of the knapsack:", total_value)

idx = np.argsort(x_star_knapsack)  # sort indices based on value-to-weight ratio
x_star_knapsack = x_star_knapsack[idx]  # sort the items taken

idx = np.argsort(x_star_greed)
x_star_greed = x_star_greed[idx]  # sort the items taken

print(f"Value of Knapsack = {total_value_knap}, Sorted Items taken (knapsack): {x_star_knapsack}")
print(f"Value of Greedy = {total_value}, Sorted Items taken (greedy): {x_star_greed}")