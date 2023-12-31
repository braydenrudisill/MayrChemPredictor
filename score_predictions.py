#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, unicode_literals
import argparse
from rdkit import Chem
import pandas as pd
import numpy as np
import onmt.opts

def canonicalize_smiles(smiles):
    mol = Chem.MolFromSmiles(smiles)
    if mol is not None:
        return Chem.MolToSmiles(mol, isomericSmiles=True)
    else:
        return ''

def get_rank(row, base, max_rank):
    for i in range(1, max_rank+1):
        if row['target'] == row[f'{base}{i}']:
            return i
    return 0

def main(opt):
    with open(opt.targets, 'r') as f:
        targets = [''.join(line.strip().split(' ')) for line in f.readlines()]

    canoincal_targets = [canonicalize_smiles(t) for t in targets]

    predictions = [[] for i in range(opt.beam_size)]

    test_df = pd.DataFrame(canoincal_targets)
    test_df.columns = ['target']
    total = len(test_df)

    with open(opt.predictions, 'r') as f:
        for i, line in enumerate(f.readlines()):
            predictions[i % opt.beam_size].append(''.join(line.strip().split(' ')))

    print(np.array(predictions).shape)

    

    for i, preds in enumerate(predictions):
        test_df[f'prediction_{i+1}'] = preds
        test_df[f'canonical_prediction_{i+1}'] = test_df[f'prediction_{i+1}'].apply(canonicalize_smiles)

    test_df['rank'] = test_df.apply(lambda row: get_rank(row, 'canonical_prediction_', opt.beam_size), axis=1)

    

    num_wrong = (test_df['rank'] == 0).sum()
    print(f'{num_wrong=}')


    wrong_smi = [(i, pred, tgt) for i, (pred, tgt, rank) in enumerate(zip(test_df['prediction_1'], test_df['target'], test_df['rank'])) if rank==0]
    print(wrong_smi)

    correct = 0
    for i in range(1, opt.beam_size+1):
        
        correct += (test_df['rank'] == i).sum()
        invalid_smiles = (test_df['canonical_prediction_{}'.format(i)] == '').sum()
        if opt.invalid_smiles:
            print('Top-{}: {:.1f}% || Invalid SMILES {:.2f}%'.format(i, correct/total*100,
                                                                     invalid_smiles/total*100))
        else:
            print('Top-{}: {:.1f}%'.format(i, correct / total * 100))



if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='score_predictions.py',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    # onmt.opts.add_md_help_argument(parser)

    parser.add_argument('-beam_size', type=int, default=5,
                       help='Beam size')
    parser.add_argument('-invalid_smiles', action="store_true",
                       help='Show % of invalid SMILES')
    parser.add_argument('-predictions', type=str, default="",
                       help="Path to file containing the predictions")
    parser.add_argument('-targets', type=str, default="",
                       help="Path to file containing targets")

    opt = parser.parse_args()
    main(opt)
