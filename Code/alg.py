import os
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Prompting user for the paths to the bird species directories
oriole_dir = input("Enter the path for the oriole images: ")
gull_dir = input("Enter the path for the gull images: ")
sparrow_dir = input("Enter the path for the sparrow images: ")

# Print the first five images from each species for verification
train_oriole_names = os.listdir(oriole_dir)
print("Orioles:", train_oriole_names[:5])

train_gull_names = os.listdir(gull_dir)
print("Gulls:", train_gull_names[:5])

train_sparrow_names = os.listdir(sparrow_dir)
print("Sparrows:", train_sparrow_names[:5])

# Set batch size for training
batch_size = 60

# Data augmentation and rescaling
train_datagen = ImageDataGenerator(rescale=1/255)

# Load training data
train_generator = train_datagen.flow_from_directory(
    os.path.dirname(oriole_dir),  # Use the parent directory for flow_from_directory
    target_size=(300, 300),
    batch_size=batch_size,
    classes=['gull', 'oriole', 'sparrow'],
    class_mode='categorical'
)

# Model definition
model = tf.keras.Sequential([
    tf.keras.layers.Conv2D(16, (3, 3), activation='relu', input_shape=(300, 300, 3)),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Conv2D(32, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Dropout(0.1),
    tf.keras.layers.Conv2D(256, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Dropout(0.1),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(3, activation='softmax')
])

model.summary()

# Compile the model
model.compile(
    loss='categorical_crossentropy',
    optimizer=tf.keras.optimizers.RMSprop(learning_rate=0.001),
    metrics=['acc']
)

# Train the model
total_sample = train_generator.n
num_epochs = 10

model.fit(
    train_generator,
    steps_per_epoch=int(total_sample / batch_size),
    epochs=num_epochs,
    verbose=1
)

# Save model to disk
model_json = model.to_json()
with open("model.json", "w") as json_file:
    json_file.write(model_json)
model.save_weights("model1.h5")
print("Model saved to disk.")