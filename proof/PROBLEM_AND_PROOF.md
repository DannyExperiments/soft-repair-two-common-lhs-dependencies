# Problem and proof outline

For the fixed schema R(A,B,C), minimize the deletion cost plus separately charged A→B and A→C violation costs. Each retained unordered pair pays for each violated dependency. [Source](https://doi.org/10.1145/3651156)

## Equal-size blocks

Make one B block per graph vertex and set all A values equal. Use one C label for each incident edge, shared only by its two endpoint blocks. Pad blocks to equal size with new labels. Choose a common deletion cost and a large A→B penalty so that the primary score increases until k full blocks and then decreases. At fixed retained size, packing as many full blocks as possible strictly improves the primary score. The entire C penalty is too small to offset any primary loss of one large penalty unit.

## Selecting a clique

Every optimum therefore keeps exactly k full blocks. The number of retained pairs with equal C labels equals the induced edge count. Hence an optimum meets the all-possible-edges threshold exactly if those k vertices form a clique. The weights and threshold are polynomially bounded integers, and a retained set's cost is polynomial-time computable for binary rational inputs.

[Complete argument](../paper/manuscript.pdf)
