from keras.models import Model
from keras import layers


def autoencoder(encoder_inputs):
    """Custom autoencoder model with attention layer

    Args:
        encoder_inputs (Tensor flow Input Layer): The input shape to be passed to the autoencoder
    """

    # Encoder

    conv_1D_layer = layers.Conv1D(32, 3, activation='relu', padding='same')
    x = layers.TimeDistributed(conv_1D_layer)(encoder_inputs)
    max_pool_1D = layers.MaxPool1D(2, padding='same')
    x = layers.TimeDistributed(max_pool_1D)(x)

    conv_1D_layer = layers.Conv1D(16, 3, activation='relu', padding='same')
    x = layers.TimeDistributed(conv_1D_layer)(x)
    max_pool_1D = layers.MaxPool1D(2, padding='same')
    x = layers.TimeDistributed(max_pool_1D)(x)

    conv_1D_layer = layers.Conv1D(1, 3 ,activation='relu', padding='same')
    x = layers.TimeDistributed(conv_1D_layer)(x)
    max_pool_1D = layers.MaxPool1D(2, padding='same')
    encoder_out = layers.TimeDistributed(max_pool_1D)(x)

    #Attention Layer
    attn_out = layers.Attention(causal =True )([encoder_out, encoder_out])

    encoder = Model(attn_out, encoder_out)

    # Decoder
    conv_1D_transpose_layer = layers.Conv1DTranspose(16, 3, strides=2, activation='relu', padding='same')
    x = layers.TimeDistributed(conv_1D_transpose_layer)(attn_out)
    conv_1D_layer = layers.Conv1D(32, 3, activation='relu', padding='same')
    x = layers.TimeDistributed(conv_1D_layer)(x)


    conv_1D_transpose_layer = layers.Conv1DTranspose(32, 3, strides=2, activation='relu', padding='same')
    x = layers.TimeDistributed(conv_1D_transpose_layer)(x)
    conv_1D_layer = layers.Conv1D(32, 3, activation='relu', padding='same')
    x = layers.TimeDistributed(conv_1D_layer)(x)


    conv_1D_transpose_layer = layers.Conv1DTranspose(32, 3, strides=2, activation='relu', padding='same')
    x = layers.TimeDistributed(conv_1D_transpose_layer)(x)
    conv_1D_layer = layers.Conv1D(32, 3, activation='relu', padding='same')
    x = layers.TimeDistributed(conv_1D_layer)(x)

    decoder_out = layers.Conv2D(1, (3, 3), activation="sigmoid", padding="same")(x)

    return Model(encoder_inputs, decoder_out), encoder