# Speech Predictability of Parents and Children's Language

A configurable pipeline that turns raw [CHILDES](https://childes.talkbank.org/) transcripts into per-speaker **predictability measures** (summed token entropy and surprisal, plus utterance length) computed with a causal LLM (Mistral-7B), and into a longitudinal dataset ready for mixed-effects modelling. Scoring is GPU-batched and parallelised over [Slurm](https://slurm.schedmd.com/) job arrays.

It was built for a supervised project at HEC Montréal (M.Sc., 2026; supervisor: Prof. Eva Portelance) that asked whether the predictability of parents' speech predicts the predictability of their children's speech. The code is meant to be reusable for similar corpus-scoring studies: behaviour is controlled by YAML files and small pluggable `.py` files, so you rarely need to edit the core code.

## How it works

```
raw CHILDES .cha files
        │  organize_main.py          (1) rename, build model.csv, convert .cha -> .flo.cex
        ▼
organized transcripts + model.csv
        │  scoring_main.py count     (2a) clean, count lines, bin-pack files into Slurm jobs
        ▼
config_block_N.yaml + files_block_N.csv + submit_scoring.sh   (auto-launched as a Slurm array)
        │  scoring_main.py score     (2b) tokenize, run LLM on GPU, compute measures
        ▼
output_block_N.csv  (one per job)
        │  main_statsprep.py         (3) merge, aggregate, pair time t-1 -> t
        ▼
new_model.csv  ──►  Report2.qmd      (4) mixed-effects models in R
```

## Repository layout

| Path | Role |
|---|---|
| `organize_main.py` | CLI for step 1 |
| `organizer.py` | `MainOrganizer` (per-corpus reorganization/renaming) and `MainExtractor` (builds `model.csv`, runs CLAN `flo`) |
| `organizing_fx_dictionaries.py` | One `org_<corpus>()` function per CHILDES corpus, plus a registry (`main_dict`) |
| `organizing_fix_data.py` | `fix_data()`: fills in missing child sex for specific corpora |
| `ConcatTranscripts2Xml.py` | Helper that joins `childespy` transcript metadata with a local list of selected transcripts |
| `scoring_main.py` | CLI for step 2, with tasks `count` and `score` |
| `txtpreprocess.py` | `TextExtraction` (applies the cleaning steps) and `Allocator` (bin-packs files into jobs) |
| `preprocessing_fx_dictionaries.py` | The library of cleaning steps (`m01`, `m01b`, `m02`, …) and their registry |
| `txtscoring.py` | `SentenceScorer`, dataset/dataloader, token-based batch sampler, and the measures |
| `sbatchwriter.py` | Writes and submits the Slurm array script |
| `main_statsprep.py`, `statprep.py`, `generalfunctions.py` | Step 3: merge job outputs and build the longitudinal dataset |
| `Report2.qmd`, `ProjetSupervise.Rproj` | Step 4: R / Quarto analysis (`nlme`, `lme4`, `clubSandwich`) |
| `Template_study/` | Starting point for a new study: `base_config.yaml`, `model.csv`, `submission_file.sh` |

## Requirements

- Python 3.11 with `pandas`, `numpy`, `pyyaml`, `torch`, `transformers` (and `childespy` for `ConcatTranscripts2Xml.py`)
- [CLAN](https://dali.talkbank.org/clan/) (`unix-clan`), whose `flo` binary is used to convert `.cha` files
- A local copy of the Mistral-7B weights, loaded with `local_files_only=True`, so there is no download at run time
- A Slurm cluster with GPU nodes for step 2 (written for the Alliance's Rorqual cluster)
- R with Quarto for step 4
- CHILDES transcripts, which are **not** included. They must be downloaded manually from [TalkBank](https://talkbank.org/) and used under its terms.

## Usage

### 1. Organize the transcripts

Put each corpus in its own subfolder of one master folder, then write a YAML:

```yaml
source_folder:     /data/childes_raw      # master folder, one subfolder per corpus
organized_folder:  /data/organized        # renamed .cha files
text_folder:       /data/text             # .flo.cex files
model_folder:      /data/model            # where model.csv is written
organizing_opts:                          # optional: org_fx_py, org_fx_dict
extracting_opts:                          # optional: chat_path (location of CLAN binaries)
formating_opts:                           # optional
```

```bash
python organize_main.py config.yaml [--organize/-o BOOL] [--write_model/-w BOOL] [--venv BOOL]
```

This will:
- Copy each corpus's files into `organized_folder` using the naming scheme `<corpus>_<n>_<task>_<age>_<other>_<corpus>_<name>.cha`
- Write `model.csv`, with one row per speaker per transcript: `name, age_months, sex, education, code, role, task, skip, file`
- Convert the transcripts to `.flo.cex` with CLAN
- Copy the config into `text_folder`

Corpus-specific reorganization lives in `organizing_fx_dictionaries.py`. To add a corpus, write an `org_<corpus>(source_folder, destination_folder)` function and register it in `main_dict`. To compare alternatives, add another named dictionary and select it with `org_fx_dict`. A different file can be selected with `org_fx_py`. Rows with `skip = 1` (for example non-English transcripts) are ignored in later steps.

### 2. Score the transcripts

Copy `Template_study/` for each study configuration (for example, one per context length) and fill in `base_config.yaml`:

```yaml
text_folder:          /data/text          # .flo.cex files
config_folder:        /study/ctx9         # where generated configs/scripts are written
transcript_file_list: model.csv
preprocessing_steps:  [m01b, m02, m04b, m05, m06]   # cleaning steps, applied in order
nallocate:            262144              # max cleaned lines per Slurm job
context_length:       0                   # preceding utterances shown to the LLM
turn:                 True                # context counted in conversational turns
batch_size:           80                  # see "Batching" below
batch_type:           ntokens             # or nlines
num_workers:          0
measures: [sum_entropy, sum_surprisal]
output_folder:        /study/ctx9/Result
# optional: model, preprocessing_opts
```

```bash
python scoring_main.py base_config.yaml count
```

`count` runs once on a CPU:
1. Applies the cleaning steps to every transcript and counts the lines that remain
2. Packs the files into jobs of at most `nallocate` lines each, using greedy best-fit decreasing bin packing, so jobs take about the same time
3. Writes `files_block_N.csv` and `config_block_N.yaml` for each job, plus `submit_scoring.sh`
4. Submits that script with `sbatch` as a GPU job array

Each array task then runs the scoring entry point (`scoring_main.py config_block_N.yaml score`; `sbatchwriter.py` calls it `remote_main.py`, so keep the names consistent on your cluster), which loads the model, tokenizes the cleaned utterances, scores them and writes `output_block_N.csv`.

**Output columns**: `file`, `speaker`, `ntokens` (mean utterance length in tokens, the MLU), `lencontext`, `propspeaker`, one mean per measure (`sum_entropy`, `sum_surprisal`), and `count` (number of utterances).

#### Cleaning steps

Cleaning is a list of small functions, each taking `(tier, line)` and returning `[tier, line]`. The library in `preprocessing_fx_dictionaries.py` strips CHAT annotations such as ELAN codes, word completions, pauses, repetitions, non-vocal events and timestamps. To add your own, write a function in a `.py` file, register it in a dictionary, and point to it with `preprocessing_opts: {prep_fx_py: my_steps}`. Add its name to `preprocessing_steps`.

#### Measures

- `sum_entropy`: sum over the utterance's tokens of the Shannon entropy of the model's next-token distribution
- `sum_surprisal`: sum over the tokens of `-log p(token | previous tokens)`
- `ntokens`: utterance length in tokens

Only the target speaker's utterances are scored. Preceding utterances from any speaker are used as context. Token-based context lengths are not implemented yet (`turn: False` raises `NotImplementedError` when `context_length > 0`).

#### Batching

- Utterances are sorted by length so that batches contain similar lengths and need little padding.
- With `batch_type: nlines`, `batch_size` is a number of utterances per batch.
- With `batch_type: ntokens`, a custom sampler fills each batch up to a memory budget derived from `batch_size`, which is the total GPU memory in GiB. It reserves 20 GiB for the model and caps `n_utterances × max_length²`.
- Batches use pinned memory and are copied to the GPU with `non_blocking=True`. Next-token probabilities are extracted for the target span with vectorized masking, and per-utterance sums are built with `scatter_add_`.

#### Choosing the model

By default the model path is set in `scoring_main.py`. Override it with `model:` in the YAML. The scorer currently uses `MistralForCausalLM`.

### 3. Join the outputs

```bash
cd /study/ctx9/Result
python main_statsprep.py
```

The script reads `../model.csv` and merges all `output_block_*.csv` files into it. It then:
- Aggregates transcripts from the same date for each speaker with a weighted mean, weighted by the number of utterances
- Combines mothers and fathers into a single `parent` per child
- Pairs each child observation at time *t* with the most recent parent observation at least `min_age_gap` months earlier (`min_age_gap=3` by default, set in `main_statsprep.py`)

The result is written to `new_model.csv`, with `_child` and `_parent` columns, `age_months_t1`, `age_months_t2`, `age_diff` and `study`.

### 4. Analyse

Open `Report2.qmd` in RStudio (`ProjetSupervise.Rproj`) to fit the linear mixed-effects models (random intercept per child) with cluster-robust standard errors.

## Design notes

- **Configuration over code.** Paths, cleaning steps, context length, measures and batching live in YAML. Each run's config is kept next to its outputs.
- **Pluggable steps.** Corpus organizers and cleaning steps are looked up by name in dictionaries, so they can be swapped without touching the core.
- **Partial runs.** Organizing and scoring can be run in parts (`--organize`, `--write_model`, and the separate `count` and `score` tasks) to isolate problems.
- **Balanced parallelism.** Bin packing on post-cleaning line counts keeps Slurm jobs close in size.

## Known limitations and TODOs

- Several paths are hard-coded and need editing for another machine, including the Slurm account, virtualenv and code paths in `sbatchwriter.py`, the default model snapshot in `scoring_main.py`, and the CLAN path in `organizer.py`.
- `sbatchwriter.py` and `Template_study/submission_file.sh` call the entry point `remote_main.py`, while this repo names it `scoring_main.py`. Rename one or the other.
- `submit_scoring.sh` in `Template_study/` also has user-specific paths and an empty `source` line to fill in.
- Planned: benchmark execution speed, estimate per-batch GPU memory, and support user-defined measures.

## Citation

Pelland, M. (2026). *Speech predictability of parents and children language* [Software]. https://github.com/MPelland-programming/Speech_predictability_of_parents_and_children_language

## License

MIT, see [LICENSE](LICENSE).
