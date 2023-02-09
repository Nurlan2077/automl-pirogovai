from keras import optimizers

OPTIMIZERS = [
    optimizers.Adam(),
    optimizers.Nadam(),
    optimizers.Adamax(),
    optimizers.Adadelta(),
    optimizers.RMSprop()
]

OPTIMIZERS_REVERSED = {
    "Adam": optimizers.Adam(),
    "Nadam": optimizers.Nadam(),
    "Adamax": optimizers.Adamax(),
    "Adadelta": optimizers.Adadelta(),
    "RMSprop": optimizers.RMSprop()
}