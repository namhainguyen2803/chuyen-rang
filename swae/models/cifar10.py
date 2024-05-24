import torch
import torch.nn as nn



class CIFAR10Encoder(nn.Module):
    """ CIFAR10 Encoder from Original Paper's Keras based Implementation.

        Args:
            init_num_filters (int): initial number of filters from encoder image channels
            lrelu_slope (float): positive number indicating LeakyReLU negative slope
            embedding_dim (int): embedding dimensionality
    """

    def __init__(self, init_num_filters=12, lrelu_slope=0.2, embedding_dim=32):
        super(CIFAR10Encoder, self).__init__()

        self.init_num_filters_ = init_num_filters
        self.lrelu_slope_ = lrelu_slope
        self.embedding_dim_ = embedding_dim

        self.features = nn.Sequential(
            # 64x64
            nn.Conv2d(3, self.init_num_filters_, kernel_size=4, stride=2, padding=1, bias=False),
            nn.LeakyReLU(self.lrelu_slope_, inplace=True),

            nn.Conv2d(self.init_num_filters_, self.init_num_filters_ * 2, kernel_size=4, stride=2, padding=1, bias=False),
            nn.BatchNorm2d(self.init_num_filters_ * 2),
            nn.LeakyReLU(self.lrelu_slope_, inplace=True),

            nn.Conv2d(self.init_num_filters_ * 2, self.init_num_filters_ * 4, kernel_size=4, stride=2, padding=1, bias=False),
            nn.BatchNorm2d(self.init_num_filters_ * 4),
            nn.LeakyReLU(self.lrelu_slope_, inplace=True),

            nn.Conv2d(self.init_num_filters_ * 4, self.init_num_filters_ * 8, kernel_size=4, stride=2, padding=1, bias=False),
            nn.BatchNorm2d(self.init_num_filters_ * 8),
            nn.LeakyReLU(self.lrelu_slope_, inplace=True),

            nn.Conv2d(self.init_num_filters_ * 8, self.embedding_dim_, kernel_size=2, stride=1, padding=0, bias=True),
        )

    def forward(self, x):
        x = self.features(x)
        x = x.view(-1, self.embedding_dim_)
        return x


class CIFAR10Decoder(nn.Module):
    """ CIFAR10 Decoder from Original Paper's Keras based Implementation.

        Args:
            init_num_filters (int): initial number of filters from encoder image channels
            lrelu_slope (float): positive number indicating LeakyReLU negative slope
            embedding_dim (int): embedding dimensionality
    """

    def __init__(self, init_num_filters=12, embedding_dim=32):
        super(CIFAR10Decoder, self).__init__()

        self.init_num_filters_ = init_num_filters
        self.embedding_dim_ = embedding_dim

        self.features = nn.Sequential(

            nn.ConvTranspose2d(self.embedding_dim_, self.init_num_filters_ * 4, kernel_size=4, stride=1, padding=0, bias=False),
            nn.BatchNorm2d(self.init_num_filters_ * 4),
            nn.ReLU(inplace=True),

            nn.ConvTranspose2d(self.init_num_filters_ * 4, self.init_num_filters_ * 2, kernel_size=4, stride=2, padding=1, bias=False),
            nn.BatchNorm2d(self.init_num_filters_ * 2),
            nn.ReLU(inplace=True),

            nn.ConvTranspose2d(self.init_num_filters_ * 2, self.init_num_filters_, kernel_size=4, stride=2, padding=1, bias=False),
            nn.BatchNorm2d(self.init_num_filters_),
            nn.ReLU(inplace=True),

            nn.ConvTranspose2d(self.init_num_filters_, 3, kernel_size=4, stride=2, padding=1, bias=True),
        )

    def forward(self, z):
        z = z.view(-1, self.embedding_dim_, 1, 1)
        z = self.features(z)
        return torch.sigmoid(z)


class CIFAR10Autoencoder(nn.Module):
    """ CIFAR10 Autoencoder from Original Paper's Keras based Implementation.

        Args:
            init_num_filters (int): initial number of filters from encoder image channels
            lrelu_slope (float): positive number indicating LeakyReLU negative slope
            embedding_dim (int): embedding dimensionality
    """

    def __init__(self, init_num_filters=12, lrelu_slope=0.2, embedding_dim=32):
        super(CIFAR10Autoencoder, self).__init__()

        self.init_num_filters_ = init_num_filters
        self.lrelu_slope_ = lrelu_slope
        self.embedding_dim_ = embedding_dim

        self.encoder = CIFAR10Encoder(init_num_filters, lrelu_slope, embedding_dim)
        self.decoder = CIFAR10Decoder(init_num_filters, embedding_dim)

        # self.encoder.apply(weights_init)
        # self.decoder.apply(weights_init)

    def forward(self, x):
        z = self.encoder(x)
        return self.decoder(z), z

    def generate(self, z):
        return self.decoder(z)