"""Encoder-decoder (cross) attention and a simplified multi-head attention.

In self-attention, queries, keys and values all come from the same sequence.
Here the decoder supplies the queries while the encoder supplies the keys and
values. The multi-head class at the bottom runs several attention heads and
concatenates their outputs.
"""

import torch ## torch let's us create tensors and also provides helper functions
import torch.nn as nn ## torch.nn gives us nn.module() and nn.Linear()
import torch.nn.functional as F # This gives us the softmax()
# rich.print pretty-prints the tensors this lesson displays.
from rich import print

# Cross-attention. Queries come from the decoder encodings. Keys and values
# come from the encoder encodings. The output has one vector per decoder
# token: a weighted blend of the encoder values.
class Attention(nn.Module): 
                            
    def __init__(self, d_model=2,  
                 row_dim=0, 
                 col_dim=1):
        
        ## Initialize nn.Module before assigning any layers.
        super().__init__()
        
        ## Three learned projections, one each for queries, keys and values.
        self.W_q = nn.Linear(in_features=d_model, out_features=d_model, bias=False)
        self.W_k = nn.Linear(in_features=d_model, out_features=d_model, bias=False)
        self.W_v = nn.Linear(in_features=d_model, out_features=d_model, bias=False)
        
        self.row_dim = row_dim
        self.col_dim = col_dim


    # encodings_for_q is the decoder side. encodings_for_k and encodings_for_v
    # are the encoder side. mask is True on encoder positions that should drop
    # out before the softmax. The returned tensor has the decoder's length and
    # width d_model, and the multi-head class below concatenates those tensors.
    ## The only change from SelfAttention and attention is that
    ## now we expect 3 sets of encodings to be passed in...
    def forward(self, encodings_for_q, encodings_for_k, encodings_for_v, mask=None):
        ## ...and we pass those sets of encodings to the various weight matrices.
        ## Step 1: separate projections for queries (decoder), keys and values
        ## (encoder).
        q = self.W_q(encodings_for_q)
        k = self.W_k(encodings_for_k)
        v = self.W_v(encodings_for_v)

        ## Step 2: score every decoder query against every encoder key.
        sims = torch.matmul(q, k.transpose(dim0=self.row_dim, dim1=self.col_dim))

        ## Step 3: scale by sqrt(d_k) to keep the scores well behaved.
        scaled_sims = sims / torch.tensor(k.size(self.col_dim)**0.5)

        ## Step 4: optionally hide invalid positions before softmax.
        if mask is not None:
            # A large negative score becomes a weight of about 0 after softmax.
            scaled_sims = scaled_sims.masked_fill(mask=mask, value=-1e9)
            
        ## Step 5: normalize scores and blend the value vectors.
        attention_percents = F.softmax(scaled_sims, dim=self.col_dim)

        attention_scores = torch.matmul(attention_percents, v)

        return attention_scores

# Three sequences, each 3 tokens by 2 features, with the same numbers on each
# side. q, k, and v still come out different, because each sequence goes
# through its own weight matrix. The first tensor is the decoder side and the
# other two are the encoder side.
## create matrices of token encodings...
encodings_for_q = torch.tensor([[1.16, 0.23],
                                [0.57, 1.36],
                                [4.41, -2.16]])

encodings_for_k = torch.tensor([[1.16, 0.23],
                                [0.57, 1.36],
                                [4.41, -2.16]])

encodings_for_v = torch.tensor([[1.16, 0.23],
                                [0.57, 1.36],
                                [4.41, -2.16]])

# The projections start at random. Pinning the seed makes W_q, W_k, and W_v
# the same on every run, so the printed matrices can be compared by hand.
## set the seed for the random number generator
torch.manual_seed(42)

# d_model=2 is the width of the encodings above. Axis 0 is a token, axis 1
# is a feature. forward uses those axes when it transposes the keys.
## create an attention object
attention = Attention(d_model=2,
                      row_dim=0,
                      col_dim=1)

# Runs the full forward pass. The printed matrix is the one the unrolled
# steps below are walking toward.
## calculate encoder-decoder attention
print("encoder-decoder attention output:\n",
      attention(encodings_for_q, encodings_for_k, encodings_for_v), "\n")

# Each Linear stores its matrix as (out_features, in_features).
# Transposing shows (in_features, out_features), the matrix a token row
# is multiplied by. The labels call that matrix W^T.
## print out the weight matrix that creates the queries
print("W_q^T:\n", attention.W_q.weight.transpose(0, 1), "\n")

## print out the weight matrix that creates the keys
print("W_k^T:\n", attention.W_k.weight.transpose(0, 1), "\n")

## print out the weight matrix that creates the values
print("W_v^T:\n", attention.W_v.weight.transpose(0, 1), "\n")

# forward() in the open, on the path with no mask. The literals 0 and 1 are
# row_dim and col_dim from the constructor, and k.size(-1) is the length of
# that feature axis, d_k. q, k, and v are the projected encodings. sims holds
# every query-key dot product. Scaling by sqrt(d_k), then softmax along the
# key axis, then multiplying by v, should match the forward print above.
q = attention.W_q(encodings_for_q)
print("q:\n", q, "\n")

k = attention.W_k(encodings_for_k)
print("k:\n", k, "\n")

v = attention.W_v(encodings_for_v)
print("v:\n", v, "\n")

sims = torch.matmul(q, k.transpose(dim0=0, dim1=1))
print("sims:\n", sims, "\n")

scaled_sims = sims / (k.size(-1)**0.5)
print("scaled_sims:\n", scaled_sims, "\n")

attention_percents = F.softmax(scaled_sims, dim=1)
print("attention_percents:\n", attention_percents, "\n")

print("attention output from q, k, v:\n",
      torch.matmul(attention_percents, v), "\n")

# Each head holds its own W_q, W_k, and W_v, so the same decoder queries
# can be scored in more than one way.
class MultiHeadAttention(nn.Module):

    def __init__(self, 
                 d_model=2,  
                 row_dim=0, 
                 col_dim=1, 
                 num_heads=1):
        
        ## Initialize nn.Module before assigning any layers.
        super().__init__()

        ## create a bunch of attention heads
        ## nn.ModuleList registers each head so PyTorch can track its parameters.
        self.heads = nn.ModuleList(
            [Attention(d_model, row_dim, col_dim) 
             for _ in range(num_heads)]
        )

        self.col_dim = col_dim
        
    def forward(self, 
                encodings_for_q, 
                encodings_for_k,
                encodings_for_v):

        ## run the data through all of the attention heads
        ## Each head returns d_model columns; concatenating along col_dim turns
        ## num_heads * d_model columns into the combined output.
        return torch.cat([head(encodings_for_q, 
                               encodings_for_k,
                               encodings_for_v) 
                          for head in self.heads], dim=self.col_dim)

## NOTE: this simplified MultiHeadAttention concatenates the outputs of all
## heads along col_dim. With d_model=2 and num_heads=2, the result has 4
## columns. A full Transformer adds an output projection back to d_model.

# One head, and the same seed as the Attention above, so this run starts
# from the same weights. With a single head the printed width is still d_model.
## set the seed for the random number generator
torch.manual_seed(42)

## create a multi-head attention object with 1 head
multiHeadAttention1 = MultiHeadAttention(d_model=2,
                                         row_dim=0,
                                         col_dim=1,
                                         num_heads=1)
                                        
## calculate encoder-decoder attention
print("multi-head attention output (1 head):\n",
      multiHeadAttention1(encodings_for_q,
                          encodings_for_k,
                          encodings_for_v), "\n")

# Reset the seed so the first of the two heads starts from that same draw.
# The second head is a new initialization. Concatenating two widths of 2
# yields 4 columns.
## reset the seed so the 2-head version starts from the same weights
torch.manual_seed(42)

## create a multi-head attention object with 2 heads
multiHeadAttention2 = MultiHeadAttention(d_model=2,
                                         row_dim=0,
                                         col_dim=1,
                                         num_heads=2)

## calculate encoder-decoder attention
print("multi-head attention output (2 heads):\n",
      multiHeadAttention2(encodings_for_q,
                          encodings_for_k,
                          encodings_for_v))