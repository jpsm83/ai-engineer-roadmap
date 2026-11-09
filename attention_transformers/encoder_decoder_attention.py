import torch ## torch let's us create tensors and also provides helper functions
import torch.nn as nn ## torch.nn gives us nn.module() and nn.Linear()
import torch.nn.functional as F # This gives us the softmax()

class Attention(nn.Module): 
                            
    def __init__(self, d_model=2,  
                 row_dim=0, 
                 col_dim=1):
        
        super().__init__()
        
        self.W_q = nn.Linear(in_features=d_model, out_features=d_model, bias=False)
        self.W_k = nn.Linear(in_features=d_model, out_features=d_model, bias=False)
        self.W_v = nn.Linear(in_features=d_model, out_features=d_model, bias=False)
        
        self.row_dim = row_dim
        self.col_dim = col_dim


    ## The only change from SelfAttention and attention is that
    ## now we expect 3 sets of encodings to be passed in...
    def forward(self, encodings_for_q, encodings_for_k, encodings_for_v, mask=None):
        ## ...and we pass those sets of encodings to the various weight matrices.
        q = self.W_q(encodings_for_q)
        k = self.W_k(encodings_for_k)
        v = self.W_v(encodings_for_v)

        sims = torch.matmul(q, k.transpose(dim0=self.row_dim, dim1=self.col_dim))

        scaled_sims = sims / torch.tensor(k.size(self.col_dim)**0.5)

        if mask is not None:
            scaled_sims = scaled_sims.masked_fill(mask=mask, value=-1e9)
            
        attention_percents = F.softmax(scaled_sims, dim=self.col_dim)

        attention_scores = torch.matmul(attention_percents, v)

        return attention_scores

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

## set the seed for the random number generator
torch.manual_seed(42)

## create an attention object
attention = Attention(d_model=2,
                      row_dim=0,
                      col_dim=1)

## calculate encoder-decoder attention
print("encoder-decoder attention output:\n",
      attention(encodings_for_q, encodings_for_k, encodings_for_v), "\n")

## print out the weight matrix that creates the queries
print("W_q^T:\n", attention.W_q.weight.transpose(0, 1), "\n")

## print out the weight matrix that creates the keys
print("W_k^T:\n", attention.W_k.weight.transpose(0, 1), "\n")

## print out the weight matrix that creates the values
print("W_v^T:\n", attention.W_v.weight.transpose(0, 1), "\n")

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

class MultiHeadAttention(nn.Module):

    def __init__(self, 
                 d_model=2,  
                 row_dim=0, 
                 col_dim=1, 
                 num_heads=1):
        
        super().__init__()

        ## create a bunch of attention heads
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
        return torch.cat([head(encodings_for_q, 
                               encodings_for_k,
                               encodings_for_v) 
                          for head in self.heads], dim=self.col_dim)

## NOTE: this simplified MultiHeadAttention concatenates the outputs of all
## heads along col_dim. With d_model=2 and num_heads=2, the result has 4
## columns. A full Transformer adds an output projection back to d_model.

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