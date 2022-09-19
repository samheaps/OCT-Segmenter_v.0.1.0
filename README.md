# OCT-Segmenter v.0.1.0
This code was adapted and customized for the purpose of automatic segmentation of porcine retinal layers in OCT-b scans. 

- *Note:* `OCT-Segmenter` *tool v.0.5.0 is now published in the NIH-NEI organization for academic use.*

If the code and methods here are useful to you and aided in your research, please consider citing the paper.

*"Automatic choroidal segmentation in OCT images using supervised deep learning methods"*

- Link: https://www.nature.com/articles/s41598-019-49816-4

# Dependencies
- Python 3.6.4
- Keras 2.4.3
- tensorflow 2.3.1
- h5py
- Matplotlib
- numpy

# Guidance for Customized Usage
## Inspect example_data.hdf5
Extract images and segmentation files from `example_data.hdf5` with `hdf5readimages.py`

## Run with example_data.hdf5
1. For a quick test, set `EPOCHS = 100` in `parameters.py`.
2. Create results and data directories at the root level directory of this repository.
3. In `parameters.py`, update the `RESULTS_LOCATION` and `DATA_LOCATION` to match the paths of the two newly created directories. Examples:
  - `DATA_LOCATION` = '/Users/user1/git/ML-Image-Segmentation/data/'
  - `RESULTS_LOCATION` = '/Users/user1/git/ML-Image-Segmentation/results/'
4. Set BIOTEAM = 0 in parameters.py and save the file.
5. Install a conda environment and all the necessary dependecies by running:

`conda env create --name ml_env --file environment.yml`

6. Activate the conda environment with `conda activate ml_env`
7. Run `python train_script_semantic_general.py`

## What to expect
- During training, the `dice_coef` (Dice Coefficient) increases as tensorflow converges on a better model.
- The results directory has one `config.hdf5` file and several hdf5 files asigned to an `epoch` number
- To read any hdf5 file from the results directory, run `hdf5scan.py`

## Custom version: Train by reading images from a directory
1. Create a `remlmaterials` directory at the root level directory of this repository with the following sub-directories: `train_images`, `train_segs`, `val_images`, `val_segs`, `test_images`, `test_segs`.
  - Example data has been added at the root level that you can use for testing in a directory called remlmaterials.
2. Copy the files into the corresponding directories. **Note: A minimum of 3 train and val files is required for training**
3. In `parameters.py`, update the `INPUT_LOCATION` to match the directory created in step one. 
(Example: `INPUT_LOCATION = '/Users/user1/git/ML-Image-Segmentation/remlmaterials/'`)
4. Set BIOTEAM = 1 in parameters.py and save the file.
5. As before, activate the conda environment with `conda activate ml_env`.
6. Run `python train_script_semantic_general.py`

## What to expect
1. `readdirimages.py` will create an hdf5 file `img_data.hdf5` with the images and segs files in the same format as the `example_data.hdf5`.
2. `img_data.hdf5` can be read with `hdf5readimages.py`
3. `img_data.hdf5` cannot be used as input to the original Kugelman et al code (BIOTEAM = 0) because it contains areas, not boundaries.
4. All other files and results are in the same format as before

# Training a model (semantic)
1. Modify load_training_data and load_validation_data functions in `train_script_semantic_general.py` to load your training and validation data (see comments in code). [see example data file and load functions]
2. Choose one of the following and pass as first training parameter as shown in code:
  - model_residual (Residual U-Net)
  - model_standard (Standard U-Net) [default] *recommended for custom use*
  - model_sSE (Standard U-Net with sSE blocks)
  - model_cSE (Standard U-Net with cSE blocks)
  - model_scSE (Standard U-Net with scSE blocks)
3. Can change the name of your dataset (DATASET_NAME).
4. Run `train_script_semantic_general.py`
5. Training results will be saved in the location defined by parameters.RESULTS_LOCATION. Each new training run will be saved in a new seperate folder named with the format: (TIMESTAMP) _ (MODEL_NAME) _ (DATASET_NAME). Each folder will contain the following files:
  - `config.hdf5` (summary of parameters used for training)
  - `stats_epoch#.hdf5` (training and validation results for each epoch up to epoch #)
  - one or more `model_epoch&.hdf5` files containing the saved model at each epoch. 
 
# Evaluating a model (semantic)
1. Update `MODEL_LOCATION` in `parameters.py` to point to the sub-directory generated during the training within the results folder. 
(Example: `MODEL_LOCATION = '/2021-06-21 17_02_56 U-net exampledata/'`)
2. Update `MODEL_NAME` in `parameters.py` to point to the largest epoch file generated during the training contained within the MODEL_LOCATION sub-directory referenced in the previous step. (Example: `MODEL_NAME = 'model_epoch100.hdf5'`)
3. Run `eval_script_semantic_general.py`
4. Evaluation results will be saved in a new folder (with the name no_aug_(DATASET_NAME).hdf5) within the specified trained network folder. Within this, a folder is created for each evaluated image containing a range of .png images illustrating the results qualitatively as well as an `evaluations.hdf5` file with all quantitative results. A new `config.hdf5` file is created in the new folder as well as `results.hdf5` and `results.csv` files summarizing the overall results after all images have been evaluated.

# Training a model (patch-based)
1. Modify `load_training_data` and `load_validation_data` functions in `train_script_patchbased_general.py` to load your training and validation data (see comments in code). [see example data file and load functions]
2. Choose one of the following and pass as first training parameter as shown in code:
  - model_cifar (Cifar CNN)
  - model_complex (Complex CNN) [default]
  - model_rnn (RNN)
3. Can change the desired patch size (PATCH_SIZE) as well as the name of your dataset (DATASET_NAME).
4. Run `train_script_patchbased_general.py`
5. Training results will be saved in the location defined by parameters`RESULTS_LOCATION`. Each new training run will be saved in a new seperate folder named with the format: (TIMESTAMP) _ (MODEL_NAME) _ (DATASET_NAME). Each folder will contain the following files:
  - `config.hdf5` (summary of parameters used for training)
  - `stats_epoch#.hdf5`(training and validation results for each epoch up to epoch #)
  - one or more `model_epoch&.hdf5` files containing the saved model at each epoch. 

# Evaluating a model (patch-based)
1. Modify `load_testing_data` function in `eval_script_patchbased_general.py` to load your testing data (see comments in code). [see example data file and load function]
2. Specify trained network folder to evaluate.
3. Specify filename of model to evaluate within the chosen folder: `model_epoch&.hdf5`
4. Run `eval_script_patchbased_general.py`
5. Evaluation results will be saved in a new folder (with the name no_aug_(DATASET_NAME).hdf5) within the specified trained network folder. Within this, a folder is created for each evaluated image containing a range of .png images illustrating the results qualitatively as well as an `evaluations.hdf5` file with all quantitative results. A new config.hdf5 file is created in the new folder as well as `results.hdf5` and `results.csv` files summarizing the overall results after all images have been evaluated.

## Still to be added
- RNN bottleneck and Combined semantic network models
- Code and instructions for preprocessing using contrast enhancement (Girard filter)
