# Finetuning Freemoji

Here’s a guide to finetuning Freemoji, whether you want to train with a different set of emojis, finetune it further, experiment with a different model, or just have fun exploring customization! 


## Navigate to the Folder

To start, activate the `venv` used for running Freemoji in the root directory. Note that training with SimpleTuner will require cloning another repository, so a separate `venv` might be needed.

Navigate to the fine-tuning folder:

```bash
cd fine-tune
```


## Preparing the Data

You’ll need a dataset of emojis, with pairs of images and their text descriptions. This folder provides the necessary scripts to collect data from [Emojigraph’s WhatsApp Emoji List](https://emojigraph.org/whatsapp/). Follow these steps:

1. **Download Emoji Data**:
   Run `downloadEmojis.py` to fetch Emojigraph’s list of WhatsApp emojis. It saves the emoji PNG links, their names, and processed names in `emojis/emojis.json`.

2. **Filter Skin Tone Variants (Optional)**:  
   Use `filterEmojis.py` to remove skin tone variants from `emojis/emojis.json`. This reduces processing time and defaults emojis to the bright yellow tone. A new `emojis/emojisFiltered.json` file will be created.

3. **Download Emojis**:  
   Run `emojiList.py` to download emojis based on the filtered or unfiltered list. By default, it uses `emojisFiltered.json`; change it to `emojis.json` for the full list.  The `emoji` folder (training data pairs with white backgrounds) and the `raw` folder (original PNG files).

You only need the `emoji` folder for training.


## Setting Up SimpleTuner

To start training, clone and set up SimpleTuner:

```bash
git clone --branch=release https://github.com/bghira/SimpleTuner.git
cd SimpleTuner
python3.11 -m venv .venv
source .venv/bin/activate
pip install -U poetry pip
poetry config virtualenvs.create false
```

Install dependencies:

```bash
# MacOS
poetry install -C install/apple

# Linux
poetry install

# Linux with ROCM
poetry install -C install/rocm
```

Replace SimpleTuner's `config` folder with the one in Open Genmoji’s directory, and update the following fields in the configuration files:

### `config.json`
- `--max_train_steps`: Number of steps to train the AI. 
- `--checkpointing_steps`: Frequency (in steps) to save the current model state. Checkpoints allow resuming training if interrupted.
- `--checkpoints_total_limit`: Maximum number of checkpoints to retain. Older checkpoints are deleted once the limit is exceeded.
- `--pretrained_model_name_or_path`: Specify the model to train (e.g., Flux). Update `--model_family` if using a non-Flux model.
- `--resolution` and `--validation_resolution`: Set to the resolution of your training data. Emojigraph’s emojis are 160x160.

### `multidatabackend.json`
Update the `emojis` section:
- `instance_data_dir`: Absolute path to the `emoji` folder.
- `minimum_image_size` and `resolution`: Match the emoji resolution (default is 160x160).


## Running the Training

Once configured, start training by running:

```bash
./train.sh
```

Training progress is saved as checkpoints, allowing you to resume from the last checkpoint if interrupted. The process may take hours or even days, depending on the setup.

During training, monitor validation images (e.g., smiley faces) and checkpoints in the `output/models` folder. The final LoRA (`.safetensors` file) will also be saved there. Rename it to `whatsapp-freemoji.safetensors` and place it in the `./fine-tune/models/` directory to use it with the Streamlit app in the root folder.


## Alternative Methods

You can also use the [AI Toolkit](https://github.com/ostris/ai-toolkit?ref=blog.paperspace.com) to train the Flux.1-dev model instead of SimpleTuner. Detailed instructions are available in [this guide](https://blog.paperspace.com/fine-tune-flux-schnell-dev/).