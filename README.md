molbeam_fp

molbeam_fp is a collection of python scripts that function to serve as tools for generating a library of morgan fingerprints and an engine for running queries on that library. The fingerprint library is built using RDKit fingerprints and datamol for normalizing/processing input smiles. The resulting fingerprints are then stored as chunked arrays in Arrow tables along with the original SMILES and compound ID. These tables are then saved as parquet files for use during fingerprint queries. 

The query engine uses Arrow to access and process the fingerprints to determine the jaccard distance between each member of the library and the query or queries. The results are then queried with duckdb to matches with good scores (values closer to zero are better) as determined by a predefined quantile. 

The results are saved as a parquet and can be directly accessed as a dataframe through Pandas or Apache Arrow.



<pre>
conda create --name molbeam_fp python=3.8
conda activate molbeam_fp
</pre>

