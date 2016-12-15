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
        - `parallel_tm_prediction.sh` script in `data/tm_prediction` 
        - `tm_seq_extraction.py` script in `data/tm_sequences`
        - `build_matrices.py` script in `data/formatted_data`
2. Rerun notebooks

