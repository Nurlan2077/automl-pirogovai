from keras import losses

loss_funcs = [
    losses.SparseCategoricalCrossentropy(from_logits=True),
    losses.CategoricalCrossentropy(from_logits=True),
    losses.CategoricalHinge(),
    losses.KLDivergence(),
    losses.SparseCategoricalCrossentropy(from_logits=True),
    losses.CosineSimilarity()
]
