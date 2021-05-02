---
title: Text Generation
nav_order: 6
layout: page
permalink: /text-generation/
has_children: true
---

## Text Generation

Initialize a HappyTextGeneration object to perform text generation

**Initialization Arguments:**
 1. model_type (string): Specify the model name in all caps, such as "ROBERTA" or "ALBERT" 
 2. model_name(string): below is a URL that contains potential models: 
       [MODELS](https://huggingface.co/models?pipeline_tag=text-generation)
 

We recommend using "HappyWordPrediction("GPT2", "gpt2-xl")" for the best performance. 
If you are using Google Colab on a free instance, then we recommended using  "gpt2-large". 
"gpt2" is the default. 


#### Example 1.0:
```python
    from happytransformer import HappyGeneration
    # --------------------------------------#
    happy_gen = HappyGeneration("GPT2", "gpt2")  # default
    # happy_gen = HappyGeneration("GPT2", "gpt2-large")  # Good for Google Colab
    # happy_gen = HappyGeneration("GPT2", "gpt2-xl")  # Best performance 

```
