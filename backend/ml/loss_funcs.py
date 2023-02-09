from keras import losses

LOSS_FUNCS = {
    losses.SparseCategoricalCrossentropy(from_logits=True) : "Разреженная категориальная перекрестная энтропия",
    losses.CategoricalHinge() : "Категориальная верхняя граница",
    losses.KLDivergence() : "Расстояние Кульбака-Лейблера",
    losses.Poisson() : "Пуассон"
}
