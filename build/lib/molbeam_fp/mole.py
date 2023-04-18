import datamol as dm
from rdkit.Chem import rdMolDescriptors

dm.disable_rdkit_log()


def smiles_to_fingerprint(smiles):

    mol = dm.to_mol(str(smiles), ordered=True)

    fingerprint_function = rdMolDescriptors.GetMorganFingerprintAsBitVect
    pars = {
        "radius": 2,
        "nBits": 512,
        "invariants": [],
        "fromAtoms": [],
        "useChirality": False,
        "useBondTypes": True,
        "useFeatures": False,
    }
    fp = fingerprint_function(mol, **pars)

    standard_smiles = dm.to_smiles(mol)
    achiral_fp = list(fp.GetOnBits())
    return standard_smiles, achiral_fp

