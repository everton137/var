import pandas as pd
from cvxopt import matrix, solvers
import numpy as np
import pickle

csv_data = pd.read_csv('./data_breast_cancer.csv', header=False)
data = csv_data.T

braca1 = data[data[3226] == 'BRACA1']
braca2 = data[data[3226] == 'BRACA2']
not_braca1 = data[data[3226] != 'BRACA1'][1:]
not_braca2 = data[data[3226] != 'BRACA2'][1:]
solutions = {}
group1 = braca1
group2 = braca2
P = matrix(np.diag([1.0,1,0]))
q = matrix([0.0]*3)

#n_genes = 3226
n_genes = 10

for gene1, gene2 in [(gene1, gene2) for gene1 in range(n_genes) for gene2 in range(gene1, n_genes)]:
    b1 = np.array([map(float, b) for b in zip(group1[gene1], group1[gene2])])
    b2 = np.array([map(float, b) for b in zip(group2[gene1], group2[gene2])])
    h = matrix(-1*np.ones(b1.shape[0] + b2.shape[0]))
    G1 = np.column_stack([b1, np.ones(b1.shape[0])])
    G2 = -1.0*np.column_stack([b2, np.ones(b2.shape[0])])
    G = matrix(np.vstack([G1, G2]))
    try:
        sol = solvers.qp(P, q, G, h)
    except:
        pass

    if sol['status'] == 'optimal':
        w = np.array(sol['x']).reshape((1,3))[0]
        w_mod = np.sqrt(w.T.dot(w))
        solutions[(gene1, gene2)] = [w, w_mod]

pickle.dump(solutions, open('solutions', 'wb'))
