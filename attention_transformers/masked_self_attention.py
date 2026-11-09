import torch ## torch let's us create tensors and also provides helper functions
import torch.nn as nn ## torch.nn gives us nn.module() and nn.Linear()
import torch.nn.functional as F # This gives us the softmax()

class MaskedSelfAttention(nn.Module): 
                            
    def __init__(self, d_model=2,  
                 row_dim=0, 
                 col_dim=1):
        
        super().__init__()
        
        self.W_q = nn.Linear(in_features=d_model, out_features=d_model, bias=False)
        self.W_k = nn.Linear(in_features=d_model, out_features=d_model, bias=False)
        self.W_v = nn.Linear(in_features=d_model, out_features=d_model, bias=False)
        
        self.row_dim = row_dim
        self.col_dim = col_dim

        
    def forward(self, token_encodings, mask=None):

        q = self.W_q(token_encodings)
        k = self.W_k(token_encodings)
        v = self.W_v(token_encodings)

        sims = torch.matmul(q, k.transpose(dim0=self.row_dim, dim1=self.col_dim))

        scaled_sims = sims / torch.tensor(k.size(self.col_dim)**0.5)

        if mask is not None:
            ## Here we are masking out things we don't want to pay attention to
            ##
            ## We replace values we wanted masked out
            ## with a very small negative number so that the SoftMax() function
            ## will give all masked elements an output value (or "probability") of 0.
            scaled_sims = scaled_sims.masked_fill(mask=mask, value=-1e9) # I've also seen -1e20 and -9e15 used in masking

        attention_percents = F.softmax(scaled_sims, dim=self.col_dim)

        attention_scores = torch.matmul(attention_percents, v)

        return attention_scores

## create a matrix of token encodings...
encodings_matrix = torch.tensor([[1.16, 0.23],
                                 [0.57, 1.36],
                                 [4.41, -2.16]])

## set the seed for the random number generator
torch.manual_seed(42)

## create a masked self_attention object
maskedSelfAttention = MaskedSelfAttention(d_model=2,
                               row_dim=0,
                               col_dim=1)

## create the mask so that we don't use
## tokens that come after a token of interest
mask = torch.tril(torch.ones(3, 3))
mask = mask == 0
print("mask:\n", mask, "\n")

## calculate masked self_attention
print("masked attention scores:\n",
      maskedSelfAttention(encodings_matrix, mask), "\n")

## print out the weight matrix that creates the queries
print("W_q^T:\n", maskedSelfAttention.W_q.weight.transpose(0, 1), "\n")

## print out the weight matrix that creates the keys
print("W_k^T:\n", maskedSelfAttention.W_k.weight.transpose(0, 1), "\n")

## print out the weight matrix that creates the values
print("W_v^T:\n", maskedSelfAttention.W_v.weight.transpose(0, 1), "\n")

q = maskedSelfAttention.W_q(encodings_matrix)
print("q:\n", q, "\n")

k = maskedSelfAttention.W_k(encodings_matrix)
print("k:\n", k, "\n")

sims = torch.matmul(q, k.transpose(dim0=0, dim1=1))
print("sims:\n", sims, "\n")

scaled_sims = sims / (k.size(-1)**0.5)
print("scaled_sims:\n", scaled_sims, "\n")

masked_scaled_sims = scaled_sims.masked_fill(mask=mask, value=-1e9)
print("masked_scaled_sims:\n", masked_scaled_sims, "\n")

attention_percents = F.softmax(masked_scaled_sims, dim=1)
print("attention_percents:\n", attention_percents, "\n")

print("masked attention output:\n",
      torch.matmul(attention_percents, maskedSelfAttention.W_v(encodings_matrix)))