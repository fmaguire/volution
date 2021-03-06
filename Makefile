INPUT_FASTA := $(shell find data/raw_sequence_data -name "*.fas")
TM_PREDS := $(subst raw_sequence_data,tm_prediction,$(INPUT_FASTA:.fas=.tmhmm))
TM_SEQS := $(subst raw_sequence_data,tm_sequences,$(INPUT_FASTA:.fas=.tmseqs))
MATRICES := data/formatted_data/X.pkl \
	data/formatted_data/y.pkl \
	data/formatted_data/info.txt
matrix := $(MATRICES)
BIN_DIR := bin

CORES_PER_JOB := 7

all: matrix

.SECONDARY: $(TM_PREDS)

tidy:
	-rm -rf data/tmp/*

clean:
	-rm -rf $(TM_PREDS) $(TM_SEQS) $(MATRICES) data/tmp/*

matrix: $(TM_SEQS) \
		$(BIN_DIR)/create_matrices.py
	python $(BIN_DIR)/create_matrices.py \
		$(TM_SEQS)

data/tm_sequences/%.tmseqs: data/tm_prediction/%.tmhmm \
		data/raw_sequence_data/%.fas \
		$(BIN_DIR)/get_tm_seqs.py
	python $(BIN_DIR)/get_tm_seqs.py \
		$< \
		data/raw_sequence_data/$*.fas \
		data/tm_sequences/$*.tmseqs 

data/tm_prediction/%.tmhmm : data/raw_sequence_data/%.fas \
		$(BIN_DIR)/parallel_tmhmm.py
	python $(BIN_DIR)/parallel_tmhmm.py \
		-i $< \
		-o data/tm_prediction/$*.tmhmm \
		-p $(CORES_PER_JOB)
