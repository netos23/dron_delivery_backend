import keras
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from keras import backend as K
from keras.callbacks import ModelCheckpoint
from keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import regularizers


def light_model(input_shape, filters, dense_neurons):
    model = keras.Sequential([
        tf.keras.layers.Conv2D(filters=filters, kernel_size=7, activation="relu", padding='same',
                               kernel_initializer='he_uniform', input_shape=input_shape),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.MaxPool2D(),

        tf.keras.layers.Conv2D(filters=filters, kernel_size=5, kernel_initializer='he_uniform', activation="relu",
                               padding='same'),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.MaxPool2D(),

        tf.keras.layers.Conv2D(filters=2 * filters, kernel_size=3, kernel_initializer='he_uniform', activation="relu",
                               padding='same'),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.MaxPool2D(),

        tf.keras.layers.Conv2D(filters=2 * filters, kernel_size=3, kernel_initializer='he_uniform', activation="relu",
                               padding='same'),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.MaxPool2D(),

        tf.keras.layers.Conv2D(filters=4 * filters, kernel_size=3, kernel_initializer='he_uniform', activation="relu",
                               padding='same'),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.MaxPool2D(),

        tf.keras.layers.Conv2D(filters=4 * filters, kernel_size=3, kernel_initializer='he_uniform', activation="relu",
                               padding='same'),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.MaxPool2D(),

        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(dense_neurons, activation="relu",
                              kernel_regularizer=regularizers.l1_l2(l1=1e-5, l2=1e-4)
                              ),
        tf.keras.layers.Dense(100, activation="relu",
                              kernel_regularizer=regularizers.l1_l2(l1=1e-5, l2=1e-4)
                              ),
        tf.keras.layers.Dense(2, activation="softmax"),
    ])
    model.summary()

    model.compile(optimizer=tf.keras.optimizers.Adam(1e-4),
                  loss=tf.keras.losses.BinaryCrossentropy(),
                  metrics=['accuracy'])
    return model


def plot_graphs(history):
    for key in history:
        plt.figure()
        loss = history[key]
        epochs = range(1, len(loss) + 1)
        plt.plot(epochs, loss)
        plt.title(key)
        plt.xlabel('Epochs')
        plt.ylabel(key)
    plt.show()


if __name__ == "__main__":
    np.random.seed(1234)
    tf.random.set_seed(1234)
    img_size = 350
    batch_size = 8
    input_shape = (img_size, img_size, 1)
    g = ImageDataGenerator(brightness_range=[0.8, 1.2],
                           zoom_range=[0.9, 1.1], rescale=1 / 255.0, validation_split=0.2)
    g_train = g.flow_from_directory("fire_dataset",
                                    target_size=(img_size, img_size),
                                    batch_size=batch_size,
                                    color_mode="grayscale",
                                    class_mode="categorical",
                                    subset="training", seed=12345)
    g_val = g.flow_from_directory("fire_dataset",
                                  target_size=(img_size, img_size),
                                  batch_size=batch_size,
                                  color_mode="grayscale",
                                  class_mode="categorical",
                                  subset="validation", seed=12345)

    K.clear_session()
    model = light_model(input_shape, filters=24, dense_neurons=600)
    name = 'weights.h5'

    mcp_save = ModelCheckpoint(name, save_best_only=True,
                               save_weights_only=True,
                               verbose=1,
                               monitor='val_loss', mode='min')
    history = model.fit(g_train, epochs=10, batch_size=batch_size, validation_data=g_val, verbose=1, callbacks=mcp_save)

    model.load_weights(name)
    print(model.evaluate(g_val))
    plot_graphs(history.history)
    gen = ImageDataGenerator(rescale=1 / 255.0).flow_from_directory("fire_dataset",
                                                                    target_size=(img_size, img_size),
                                                                    batch_size=1,
                                                                    color_mode="grayscale",
                                                                    class_mode="categorical", shuffle=False)

    plot_graphs(history.history)
    model.load_weights(name)
    model.save("model.h5")
