# Captcha solver
For this project, the goal is to check on a website Check appointment availability automatically.
For that, the web scraper have to solve a image captcha on the first page. So an idea come in our mind,
solve that image captcha with a machine learning algorithm.

![Captcha image to solve!](/img/first_step.png "Captcha to solve")

We first worked on deep-learning models with CNN architecture to capture the differents patterns in images. The output of models for this kind of architecture was not sequential. But rather of fixed size with the length being the number of letters in the image that contains the most letters. The results for these architectures were inconclusive.

Our second attempt was on an image-to-text transformers type architecture inspire from [TrOCR: Transformer-based Optical Character Recognition with Pre-trained Models](https://arxiv.org/abs/2109.10282). The encoder is the vision transformer and the decoder an autoregressive text Transformer. And that time, we got better success rate.

After succeded the captcha, the automate go on the next page. Send a email to people to come and pick a appointment, otherwise it stay there for a while and shutdown after.

## Dataset

To build the dataset, we used a pipeline to extract 600 images from the site on which we had to solve the captchas ([script](https://github.com/joelk18/Captcha_solver/blob/main/collect_data.py)). The solutions were manually annotated.

## Transformer model

We use a pre-trained model from [TrOCR: Transformer-based Optical Character Recognition with Pre-trained Models](https://arxiv.org/abs/2109.10282) store on huggingface hub (**trocr-base-printed**). Then train the model on our 600 images.

## Results
![Solver](/img/captcha_solver.gif)
