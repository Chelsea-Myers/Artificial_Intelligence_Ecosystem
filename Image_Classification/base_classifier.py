import tensorflow as tf
tf.get_logger().setLevel('ERROR')
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image
import numpy as np
import cv2
import matplotlib.pyplot as plt

model = MobileNetV2(weights="imagenet")

def make_gradcam_heatmap(img_array, model, last_conv_layer_name, pred_index=None):
    """
    Generate Grad-CAM heatmap for a given image.
    
    Args:
        img_array: Preprocessed image array
        model: The neural network model
        last_conv_layer_name: Name of the last convolutional layer
        pred_index: Index of the predicted class (None = use top prediction)
    
    Returns:
        Heatmap array showing important regions
    """
    # Create a model that outputs both predictions and last conv layer output
    grad_model = tf.keras.models.Model(
        inputs=[model.inputs],
        outputs=[model.get_layer(last_conv_layer_name).output, model.output]
    )
    
    # Record operations for automatic differentiation
    with tf.GradientTape() as tape:
        # Get the conv layer output and predictions
        last_conv_layer_output, preds = grad_model(img_array)
        
        # If no pred_index specified, use the top prediction
        if pred_index is None:
            pred_index = tf.argmax(preds[0])
        
        # Get the score for the predicted class
        class_channel = preds[:, pred_index]
    
    # Compute gradient of the predicted class with respect to conv layer output
    grads = tape.gradient(class_channel, last_conv_layer_output)
    
    # Calculate the mean intensity of the gradient over all feature maps
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
    
    # Weight the conv layer output by the gradients
    last_conv_layer_output = last_conv_layer_output[0]
    heatmap = last_conv_layer_output @ pooled_grads[..., tf.newaxis]
    heatmap = tf.squeeze(heatmap)
    
    # Normalize the heatmap between 0 and 1
    heatmap = tf.maximum(heatmap, 0) / tf.math.reduce_max(heatmap)
    return heatmap.numpy()

def save_gradcam_visualization(img_path, heatmap, output_path="gradcam_output.jpg", alpha=0.4):
    """
    Overlay Grad-CAM heatmap on original image and save.
    
    Args:
        img_path: Path to original image
        heatmap: Grad-CAM heatmap array
        output_path: Where to save the visualization
        alpha: Transparency of heatmap overlay (0-1)
    """
    # Load the original image
    img = cv2.imread(img_path)
    
    # Resize heatmap to match original image size
    heatmap = cv2.resize(heatmap, (img.shape[1], img.shape[0]))
    
    # Convert heatmap to RGB colormap
    heatmap = np.uint8(255 * heatmap)
    heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
    
    # Overlay heatmap on original image
    superimposed_img = cv2.addWeighted(img, 1 - alpha, heatmap, alpha, 0)
    
    # Save the result
    cv2.imwrite(output_path, superimposed_img)
    print(f"Grad-CAM visualization saved to: {output_path}")

def classify_image(image_path, use_gradcam=True):
    try:
        img = image.load_img(image_path, target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array = preprocess_input(img_array)
        img_array = np.expand_dims(img_array, axis=0)

        predictions = model.predict(img_array)
        decoded_predictions = decode_predictions(predictions, top=3)[0]

        print("\nTop-3 Predictions for", image_path)
        for i, (_, label, score) in enumerate(decoded_predictions):
            print(f"  {i + 1}: {label} ({score:.2f})")
        
        # Generate Grad-CAM visualization if requested
        if use_gradcam:
            print("\nGenerating Grad-CAM visualization...")
            # For MobileNetV2, the last conv layer is typically 'out_relu'
            last_conv_layer_name = "out_relu"
            
            # Generate heatmap for the top prediction
            heatmap = make_gradcam_heatmap(img_array, model, last_conv_layer_name)
            
            # Save visualization
            output_filename = image_path.rsplit('.', 1)[0] + "_gradcam.jpg"
            save_gradcam_visualization(image_path, heatmap, output_filename)
            
    except Exception as e:
        print(f"Error processing '{image_path}': {e}")

if __name__ == "__main__":
    print("Image Classifier (type 'exit' to quit)\n")
    while True:
        image_path = input("Enter image filename: ").strip()
        if image_path.lower() == "exit":
            print("Goodbye!")
            break
        classify_image(image_path)
