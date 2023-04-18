import duckdb
import pyarrow as pa
import pyarrow.parquet as pq
import pandas as pd
import glob
import numpy as np
import pyarrow.feather as feather
import sys
import molbeam
import similarity

dataset_dir = sys.argv[1]
output_dir = sys.argv[2]

def process_batch_fp(query_names, query_matrix, mol_batch):
    fingerprints = mol_batch.column('achiral_fp')
    fp_matrix_in = similarity.build_fingerprint_matrix(fingerprints)
    fp_distance = similarity.fast_jaccard(fp_matrix_in, query_matrix)
    return fp_distance,  mol_batch.column('standard_smiles'), mol_batch.column('idnumber')


def export_results(result_list, query, threshold):
    result_df = pd.concat(result_list)
    result_df = result_df.sort_values(by=['Z4291231744', 'Z4418909220', 'Z2768891723', 'PV-003140863219', 'Z4591645167'], ascending=True)
    print(result_df.head(10))
    table = pa.Table.from_pandas(result_df)
    pq.write_table(table, f'{output_dir}/query_out.parquet')
    print(f'Wrote results to: {output_dir}/query_out.parquet')


def main():
    query = [
        ('PV-004207401484', 'CC(C)C(C#N)C(=O)N1CCCN(C(=O)CSc2cnn(C)c2)CC1C'),
        ('PV-005694609843', 'CC(C)C(C#N)C(=O)N1CCCC(CN(C)C(=O)c2ncnc3c2CCC3)C1')
    ]
    query_names = [q[0] for q in query]
    query_matrix = similarity.format_query(query)
    columns = ["idnumber", "standard_smiles", "achiral_fp"]
    results = []
    # print('Searching enamine database of 3.8M molecules...')

    dataset = dataset_dir
    lis = glob.glob(f'{dataset}/*.parquet')
    # minimum quatile to be considered a match
    quantile = 0.00005
    results = []
    for mol_batch in molbeam.stream(lis, file_format="parquet", batch_size=20000, columns=columns):
        result = process_batch_fp(query_names, query_matrix, mol_batch)
        results.append(result)


    scores_lis = [results[_][0] for _ in range(len(results))]
    scores_arr = np.vstack(scores_lis)
    smiles_lis_pa = [results[_][1] for _ in range(len(results))]
    canonical_id_lis_pa = [results[_][2] for _ in range(len(results))]
    smiles_arr = pa.concat_arrays(smiles_lis_pa)
    canonical_id_arr = pa.concat_arrays(canonical_id_lis_pa)
    d = {}
    for i,query in enumerate(query_names):
        query_col = f'{query}_score'
        scores_col = scores_arr[:, i]
        query_quantile = np.quantile(scores_col, quantile)
        d[query_col] = {
            'scores':scores_col,
            'quantile':query_quantile 
        }
    data = [
        canonical_id_arr,
        smiles_arr,
    ]
    col_names = [
        'idnumber',
        'standard_smiles',
    ]
    for i,col_name in enumerate(d):
        arr = d[col_name]['scores']
        data.append(arr)
        col_names.append(col_name)
    table = pa.Table.from_arrays(data, names=col_names)
    pq.write_table(table, 'test_results.parquet')

    rel = duckdb.arrow(table)


    sql_lis = []
    for i,col_name in enumerate(d):
        quantile = d[col_name]['quantile']
        sql = """
            SELECT *
            FROM 'table'
            WHERE "{col_name}" 
            < {quantile}
        """.format(col_name=col_name, quantile=quantile)
        sql_lis.append(sql)


    df_lis = []
    for sql in sql_lis:
        df = rel.query("arrow", sql).df()
        df_lis.append(df)


    bigdata = pd.concat(df_lis, ignore_index=True, sort=False)
    bigdata.reset_index()
    print(len(bigdata))
    table = pa.Table.from_pandas(bigdata)
    pq.write_table(table, f'{output_dir}/query_out.parquet')
    print(f'Wrote results to: {output_dir}/query_out.parquet')

if __name__ == '__main__':
    main()
