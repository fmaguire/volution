Volution
--------


TM domain evolutionary analysis:


Project layout: 

```
    data/       - folder containing all data
        raw_sequence_data/ - folder containing fasta sequences of raw data for each class
        tm_prediction/     - tm_prediction for each class fasta sequence
        tm_sequences/      - extracted tm sequences for each class
        formatted_data/    - pickled X and y matrices created from extracted tm data

    analysis/   - folder containing analysis
        data_exploration/  - code and notebook for data exploration
        classifier/        - code and notebook for classifier
        mutator/           - code and notebook for mutation analysis

```

Rerunning analyses:

1. First Generate input data:
    - place a fasta for each class in `data/raw_sequence_data`: 
    - run `make` to execute the following steps:
        - `parallel_tmhmm.py` script in `data/tm_prediction` 
        - `get_tm_seqs.py` script in `data/tm_sequences`
        - `build_matrices.py` script in `data/formatted_data`
2. Rerun notebooks


##TM project overview

###Input data

Archaea and Eukaryote sequences are the entirety of the NR database harvested
by getting all GIs from entrez and then `blastdbcmd` to filter the nr database
for that taxa 

    blastdbcmd -db ../nr_db/nr -entry_batch ../gi_lists/ArcNr_gi.txt 

Sequences were then clustered at 100% to ensure no redundancy was included 
(although shouldn't have been needed for an NR database) using cd-hit e.g.
    
    cd-hit -c 1.00 


Due to problems getting Bacteria from NCBI due to being too numerous for 
`blastdbcmd` to parse easily I grabbed all the ensembl genomes instead

    find ftp.ensemblgenomes.org -type f -name *.gz | xargs gunzip -c > ensembl_bacteria.fasta; cd-hit -c 1.00 -i ensembl_bacteria.fasta -o ensembl_bacteria_clustered -M 200000 -T 10

###Extracting TM Seqs

TM seqs were extracted by running `tmhmm` on input sequences via a parallelisation
script (`parallel_tmhmm.py`), then a simple python script was used to extract
TM sequences themselves from the input fasta based on the TMHMM predictions
(`get_tm_seqs.py`).

Sequences were then built into matrices and vectors for training.

This and later stages can trivially be rerun using the makefile included
e.g.
    make



