from keras import losses

LOSS_FUNCS = [
    losses.SparseCategoricalCrossentropy(from_logits=True),
    losses.CategoricalHinge(),
    losses.KLDivergence(),
    losses.Poisson()
]
