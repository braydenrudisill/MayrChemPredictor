# Running the Model

## Training
Make sure to put your wandb api key in first
```console
$ export WANDB_API_KEY={YOUR_KEY}
```
Then you can train the model:
```console
$ python train.py -config config/mayr_augm.yaml -share_vocab  -wandb
```

## Testing
```console
$ python translate.py -model model.pt -src source.txt -output output.txt -gpu 0 -n_best 5
```

## Evaluate Predictions
```console
$ python score_predictions.py -targets targets.txt -predictions preds.txt -beam_size 5
```

# Vocabulary Chunking

The original molecular transformer paper split each smile string into tokens in a fairly straightforward way. However, a common approach in transformer architecture is to split words into sub words to increase correlation between related word and aid in  extrapolation to other datasets with different vocabularies. In this case, we can split ions:
- [Br-] ->  [Ion] Br - [Ion]
- [NH3+] -> [Ion] N H H H + [Ion]
- [MoH-3] -> [Ion] Mo H - - - [Ion]

We use a similar procedure for stereochemistry aromaticity:
- [C@@H] -> C [@@]
- [C@@]C -> C [@@] [C]
- n -> N [aro]

<!-- # Structural encoding methods
The original Molecular transformer paper uses SMILE strings along with traditional transformer positional encoding. While this works well in practice, it may be bringing too much human bias into the picture. It's possible that a more generalized encoding approach such as relative euclidian distances could improve the scalability of the model. One common approach is to use the eigenvectors of the Laplacian to encode such positional information, however, this treats the molecule as a pure mathematical graph without acknowledging varying bond types. For this reason, we propose using a more basic approach such as the inverse euclidian distance. However, for better inference, we shift this relative inverted distance to the range (-1, 1) instead of (0, 1)

## Traditional positional encoding

## Laplacian eigenvector encoding

## Relative euclidian distance -->
