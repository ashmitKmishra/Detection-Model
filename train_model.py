import sys
import tensorflow as tf
from tensorflow.keras import layers, models, preprocessing
import time

# Data loading
train_datagen = preprocessing.image.ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2,
    rotation_range=10,
    zoom_range=0.1
)

train_data = train_datagen.flow_from_directory(
    'dataset/asl_alphabet_train/asl_alphabet_train/',
    target_size=(64, 64),  # Reduce size for faster training
    batch_size=32,
    class_mode='categorical',
    subset='training'
)

val_data = train_datagen.flow_from_directory(
    'dataset/asl_alphabet_train/asl_alphabet_train/', 
    target_size=(64, 64),
    batch_size=32,
    class_mode='categorical',
    subset='validation'
)

# CNN Model
model = models.Sequential([
    layers.Conv2D(32, (3,3), activation='relu', input_shape=(64,64,3)),
    layers.MaxPooling2D(2,2),
    layers.Conv2D(64, (3,3), activation='relu'),
    layers.MaxPooling2D(2,2),
    layers.Conv2D(128, (3,3), activation='relu'),
    layers.MaxPooling2D(2,2),
    layers.Flatten(),
    layers.Dense(512, activation='relu'),
    layers.Dropout(0.5),
    layers.Dense(29, activation='softmax')
])

model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])


# Train
history = model.fit(
    train_data,
    epochs=10,
    validation_data=val_data
)
try:
    # Single .fit() call wrapped in try-except
    history = model.fit(
        train_data,
        epochs=10,
        validation_data=val_data
    )
except KeyboardInterrupt:
    print("\nTraining stopped early! Saving partial model...")
    model.save('asl_cnn_interrupted.h5')
    time.sleep(1)
    sys.exit(0)

# Save model
model.save('asl_cnn.h5')