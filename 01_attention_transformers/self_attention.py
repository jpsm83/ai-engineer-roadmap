"""Scaled dot-product self-attention, written out step by step.

Each token attends to every token in the same sequence:

    Attention(Q, K, V) = softmax(Q K^T / sqrt(d_k)) V

The demo at the bottom uses tiny 2-dimensional encodings so the matrix math
can be followed by hand.
"""

import torch ## torch let's us create tensors and also provides helper functions
import torch.nn as nn ## torch.nn gives us nn.module() and nn.Linear()
import torch.nn.functional as F # This gives us the softmax()

class SelfAttention(nn.Module): 
                            
    def __init__(self, d_model=2,  
                 row_dim=0, 
                 col_dim=1):
        ## d_model = the number of embedding values per token.
        ##           Because we want to be able to do the math by hand, we've
        ##           the default value for d_model=2.
        ##           However, in "Attention Is All You Need" d_model=512
        ##
        ## row_dim, col_dim = the indices we should use to access rows or columns

        
        ## nn.Module must be initialized before any layers are assigned.
        super().__init__()
        
        ## Initialize the Weights (W) that we'll use to create the
        ## query (q), key (k) and value (v) for each token
        ## NOTE: A lot of implementations include bias terms when
        ##       creating the the queries, keys, and values, but
        ##       the original manuscript that described Attention,
        ##       "Attention Is All You Need" did not, so we won't either
        self.W_q = nn.Linear(in_features=d_model, out_features=d_model, bias=False)
        self.W_k = nn.Linear(in_features=d_model, out_features=d_model, bias=False)
        self.W_v = nn.Linear(in_features=d_model, out_features=d_model, bias=False)
        
        self.row_dim = row_dim
        self.col_dim = col_dim

        
    def forward(self, token_encodings):
        ## forward() is called when the model object is invoked, for example
        ## selfAttention(encodings_matrix).
        ##
        ## Step 1: project every token encoding into a query, key and value.
        ## Create the query, key and values using the encoding numbers
        ## associated with each token (token encodings)
        q = self.W_q(token_encodings)
        k = self.W_k(token_encodings)
        v = self.W_v(token_encodings)

        ## Step 2: the dot product of each query with every key measures how
        ## similar two tokens are. k is transposed so the shapes align.
        ## Compute similarities scores: (q * k^T)
        sims = torch.matmul(q, k.transpose(dim0=self.row_dim, dim1=self.col_dim))

        ## Step 3: scale by sqrt(d_k) so the dot products do not grow too
        ## large as the embedding size increases.
        ## Scale the similarities by dividing by sqrt(k.col_dim)
        scaled_sims = sims / torch.tensor(k.size(self.col_dim)**0.5)

        ## Step 4: softmax turns each row of similarity scores into weights
        ## that sum to 1, i.e. a percentage per token.
        ## Apply softmax to determine what percent of each tokens' value to
        ## use in the final attention values.
        attention_percents = F.softmax(scaled_sims, dim=self.col_dim)

        ## Step 5: weighted sum of the value vectors. Each output token is a
        ## blend of all value vectors, weighted by attention percentages.
        ## Scale the values by their associated percentages and add them up.
        attention_scores = torch.matmul(attention_percents, v)

        return attention_scores

## create a matrix of token encodings...
encodings_matrix = torch.tensor([[1.16, 0.23],
                                 [0.57, 1.36],
                                 [4.41, -2.16]])

## set the seed for the random number generator
torch.manual_seed(42)

## create a basic self_attention ojbect
selfAttention = SelfAttention(d_model=2,
                               row_dim=0,
                               col_dim=1)

## calculate basic attention for the token encodings
print("attention scores:\n", selfAttention(encodings_matrix), "\n")

## print out the weight matrix that creates the queries
print("W_q^T:\n", selfAttention.W_q.weight.transpose(0, 1), "\n")

## print out the weight matrix that creates the keys
print("W_k^T:\n", selfAttention.W_k.weight.transpose(0, 1), "\n")

## print out the weight matrix that creates the values
print("W_v^T:\n", selfAttention.W_v.weight.transpose(0, 1), "\n")

## The rest of the file repeats forward() step by step so each intermediate
## matrix can be inspected. The final result should match the output above.
q = selfAttention.W_q(encodings_matrix)
print("q:\n", q, "\n")

k = selfAttention.W_k(encodings_matrix)
print("k:\n", k, "\n")

sims = torch.matmul(q, k.transpose(dim0=0, dim1=1))
print("sims:\n", sims, "\n")

scaled_sims = sims / (k.size(-1)**0.5)
print("scaled_sims:\n", scaled_sims, "\n")

attention_percents = F.softmax(scaled_sims, dim=1)
print("attention_percents:\n", attention_percents, "\n")

print("attention output:\n",
      torch.matmul(attention_percents, selfAttention.W_v(encodings_matrix)))