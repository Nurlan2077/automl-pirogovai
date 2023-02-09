from keras import losses

LOSS_FUNCS = {
    losses.SparseCategoricalCrossentropy(from_logits=True): "Разреженная категориальная перекрестная энтропия",
    losses.CategoricalHinge(): "Категориальная верхняя граница",
    losses.KLDivergence(): "Расстояние Кульбака-Лейблера",
    losses.Poisson(): "Пуассон"
}

LOSS_FUNCS_REVERSED = {
	"CCE": losses.SparseCategoricalCrossentropy(from_logits=True),
	"CategoricalHinge": losses.CategoricalHinge(),
	"KLDivergence": losses.KLDivergence(),
	"Poisson": losses.Poisson()
}
