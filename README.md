molbeam_fp

molbeam_fp is a collection of python scripts that function to serve as tools for generating a library of morgan fingerprints and an engine for running queries on that library. The fingerprint library is built using RDKit fingerprints and datamol for normalizing/processing input smiles. The resulting fingerprints are then stored as chunked arrays in Arrow tables along with the original SMILES and compound ID. These tables are then saved as parquet files for use during fingerprint queries. 

The query engine uses Arrow to access and process the fingerprints to determine the jaccard distance between each member of the library and the query or queries. The results are then queried with duckdb to matches with good scores (values closer to zero are better) as determined by a predefined quantile. 

The results are saved as a parquet and can be directly accessed as a dataframe through Pandas or Apache Arrow. If your fingerprint database is split over several directories, then the query process can be parallelized (code not provided here). 

Steps for utilizing the scripts:

1) First create a conda enviroment for running the scripts. Code was only tested with python 3.8.

<pre>
conda create --name molbeam_fp python=3.8
conda activate molbeam_fp
</pre>

2) Install dependencies.

<pre>
pip install pyarrow duckdb datamol rdkit pandas
</pre>

3) Clone the repo.

<pre>
git clone https://github.com/abazabaaa/molbeam_fp.git
</pre>

4) Convert the SMILES csv into a parquet dataset. An example csv is provided along with expected output. You must create a directory for the output parquet files. Based on the settings in the script the output parquet is roughly ~30k smiles strings per parquet.

<pre>
python large_csv_to_fp_pq.py /path/to/file.csv /path/to/output_dir smiles_column_name compound_id_col_name
</pre>

/path/to/file.csv = absolute path to csv file. Can be compressed (bz2). \
/path/to/output_dir = a directory that has been previously created and is meant to store the output parquet files from the csv. \
smiles_column_name = the name of the smiles column found within the csv file. \
compound_id_col_name = the name of the column that contains the compound IDs or names.

5) Convert the SMILES parquet dataset into a parquet dataset that contains morgan fingerprints.

<pre>
python process_smiles_to_fp_pq.py /path/to/parquet_dataset/from_csv_file /path/to/parquet_fps/output_dir parquet_output_file_name_prefix name_of_smiles_column num_cpu_cores_to_use fingerprint_size fingerprint_radius
</pre>

/path/to/parquet_dataset/from_csv_file = a directory that has been previously created and is meant to store the output parquet files from the csv in previous step.
\
/path/to/parquet_fps/output_dir = a directory that has been previously created and is meant to store the dataset containing the parquet with fingerprints. \
parquet_output_file_name_prefix = prefix of the filename for each parquet created in this step
\
num_cpu_cores_to_use = number of cpu cores datamol is allowed to use during fingerprint generation
\
fingerprint_size = number of bits in morgan fingerprint (256, 512, 1024, etc)
\
fingerprint_radius = radius used in generation of morgan fingerprints (2, 3, etc)
\




