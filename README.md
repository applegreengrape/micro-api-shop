## The first micro api product - one pound nlp api
api endpoint: `https://pzoo.co.uk`

- Tokenization
path: `/1pound-nlp/api/v1.0/tokenize`
``` 
$ cat payload.json 
{
    "text": "spaCy is a library for advanced Natural Language Processing in Python and Cython. It's built on the very latest research, and was designed from day one to be used in real products. spaCy comes with pretrained statistical models and word vectors, and currently supports tokenization for 50+ languages. It features state-of-the-art speed, convolutional neural network models for tagging, parsing and named entity recognition and easy deep learning integration. It's commercial open-source software, released under the MIT license."
}

$ curl -X POST \
    -H "Content-Type: application/json" \
    -H "api_tok: 83bf1ab8-a1a7-11ea-80c5-acde48001122" \
    -d "@payload.json" \
    http://localhost:4242/1pound-nlp/api/v1.0/tokenize

{"result":["spaCy is a library for advanced Natural Language Processing in Python and Cython.","It's built on the very latest research, and was designed from day one to be used in real products.","spaCy comes with pretrained statistical models and word vectors, and currently supports tokenization for 50+ languages.","It features state-of-the-art speed, convolutional neural network models for tagging, parsing and named entity recognition and easy deep learning integration.","It's commercial open-source software, released under the MIT license."]}
```

- POS_Tagger
path: `/1pound-nlp/api/v1.0/tag`
```
$ cat payload.json
{
    "text": "spaCy is a library for advanced Natural Language Processing in Python and Cython."
}

$ curl -X POST \
    -H "Content-Type: application/json" \
    -H "api_tok: 83bf1ab8-a1a7-11ea-80c5-acde48001122" \
    -d "@payload.json" \
    http://localhost:4242/1pound-nlp/api/v1.0/tag

{"result":[["spaCy","NN"],["is","VBZ"],["a","DT"],["library","NN"],["for","IN"],["advanced","JJ"],["Natural","NNP"],["Language","NNP"],["Processing","NNP"],["in","IN"],["Python","NNP"],["and","CC"],["Cython","NNP"],[".","."]]}
```

- NER (Named Entity Recognition)
path: `/1pound-nlp/api/v1.0/ent`
```
$ cat payload.json 
{
    "text": "spaCy is a library for advanced Natural Language Processing in Python and Cython. It's built on the very latest research, and was designed from day one to be used in real products. spaCy comes with pretrained statistical models and word vectors, and currently supports tokenization for 50+ languages. It features state-of-the-art speed, convolutional neural network models for tagging, parsing and named entity recognition and easy deep learning integration. It's commercial open-source software, released under the MIT license."
}

$ curl -X POST \
    -H "Content-Type: application/json" \
    -H "api_tok: 83bf1ab8-a1a7-11ea-80c5-acde48001122" \
    -d "@payload.json" \
    http://localhost:4242/1pound-nlp/api/v1.0/ent

{"result":[["Natural Language Processing","ORG"],["Python","GPE"],["Cython","ORG"],["day one","DATE"],["50","CARDINAL"],["MIT","ORG"]]}
```
