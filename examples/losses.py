import torch


def ranking_loss(x, y):
    x = x.div(x.norm(dim=1)[:, None])
    y = y.div(y.norm(dim=1)[:, None])
    similarities = x.matmul(y.T)
    return -torch.nn.functional.log_softmax(similarities, dim=1).diag().mean()


class AutoRegressiveLoss:
    def __init__(self, stop_token):
        self.stop_token = stop_token

    def __call__(self, x, y):
        x = x.transpose(2, 1)
        not_stops = (y != self.stop_token).type(torch.long)
        losses = torch.nn.functional.cross_entropy(x, y)
        normalizing_factors = not_stops.sum(axis=1).unsqueeze(1)
        fractional_losses = (losses * not_stops).div(normalizing_factors).sum(axis=1)
        return fractional_losses

