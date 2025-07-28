# prepare_data.py
import tensorflow as tf
import os
import numpy as np

print("INFO: Starting data preparation...")

# Create the main data directory if it doesn't exist
if not os.path.exists("local_data"):
    os.mkdir("local_data")
    print("INFO: Created 'local_data' directory.")

# Create a subdirectory for a specific digit
# We'll simulate this provider having data for the digit '7'
digit_dir = os.path.join("local_data", "digit_7")
if not os.path.exists(digit_dir):
    os.mkdir(digit_dir)
    print(f"INFO: Created '{digit_dir}' directory.")

# Load the MNIST dataset
(x_train, y_train), (_, _) = tf.keras.datasets.mnist.load_data()
print("INFO: MNIST dataset loaded.")

# Find the first 10 images of the digit '7'
digit_7_images = x_train[y_train == 7][:10]

# Save these images to the directory
for i, image_array in enumerate(digit_7_images):
    file_path = os.path.join(digit_dir, f"seven_{i}.png")
    # Convert to a format that can be saved as a PNG
    tf.keras.preprocessing.image.save_img(file_path, np.expand_dims(image_array, axis=-1))

print(f"INFO: Successfully saved 10 images of the digit '7' to '{digit_dir}'.")
print("INFO: Data preparation complete.")