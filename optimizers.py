from keras import optimizers


OPTIMIZERS = [
    optimizers.Adam(),
    optimizers.Nadam(),
    optimizers.Adamax(),
    optimizers.Adadelta()
]