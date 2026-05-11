import torch
import torchvision.transforms as transforms
import matplotlib.pyplot as plt
import numpy as np

import torchvision

# MNIST Constants
MNIST_MEAN = (0.1307,)
MNIST_STD = (0.3081,)

# Normalization function for MNIST
MNIST_NORMALIZE = transforms.Normalize(MNIST_MEAN, MNIST_STD)
IMAGENET_NORMALIZE = MNIST_NORMALIZE # Alias to keep snippet compatibility

def mnist_denormalize(tensor):
    """Denormalizes MNIST tensor for visualization"""
    return tensor * 0.3081 + 0.1307

def load_example_image(preprocess=True):
    """Loads an image from the local MNIST dataset"""
    dataset = torchvision.datasets.MNIST(
        root='./data', 
        train=False, 
        download=False, 
        transform=transforms.ToTensor()
    )
    img_tensor, label = dataset[0] # Get the first sample (a '7')
    if preprocess:
        img_tensor = MNIST_NORMALIZE(img_tensor)
    return img_tensor, label

def make_single_prediction(model, image):
    """Generic prediction helper"""
    model.eval()
    with torch.no_grad():
        # Handle batching if needed
        img_input = image.unsqueeze(0) if image.dim() == 3 else image
        output = model(img_input)
        probs = torch.nn.functional.softmax(output, dim=1)
        confidence, index = torch.max(probs, 1)
    return None, index.item(), confidence.item()

def get_imagenet_label(index):
    """Returns the digit string"""
    return str(index)

def display_adv_images(clean, adv, clean_res, adv_res, **kwargs):
    """Displays MNIST images side by side"""
    clean_label, clean_conf = clean_res
    adv_label, adv_conf = adv_res
    
    plt.figure(figsize=(8, 4))
    plt.subplot(1, 2, 1)
    plt.imshow(clean.detach().squeeze().cpu().numpy(), cmap='gray')
    plt.title(f"Clean: {clean_label} ({clean_conf:.2f})")
    plt.axis('off')
    
    plt.subplot(1, 2, 2)
    plt.imshow(adv.detach().squeeze().cpu().numpy(), cmap='gray')
    plt.title(f"Adv: {adv_label} ({adv_conf:.2f})")
    plt.axis('off')
    plt.show()

def test_untargeted_attack(untargeted_adv_attack, model, device, eps=8/255., **kwargs):
    model.eval()
    
    # Load a MNIST image (unnormalized [0,1])
    image, true_label = load_example_image(preprocess=False)
    image = image.to(device).requires_grad_(True)
    true_labels = torch.tensor([true_label]).to(device)

    # Get initial prediction using normalized image
    _, index, confidence = make_single_prediction(model, MNIST_NORMALIZE(image))
    label = get_imagenet_label(index)

    # Generate Adversarial Example
    adv_image = untargeted_adv_attack(
        image.unsqueeze(0), 
        true_labels, 
        model, 
        MNIST_NORMALIZE, 
        eps=eps,
        **kwargs
    ).squeeze(0)

    # Get adversarial prediction
    _, adv_index, adv_confidence = make_single_prediction(model, MNIST_NORMALIZE(adv_image))
    adv_label = get_imagenet_label(adv_index)

    # Display Results
    display_adv_images(
        image, 
        adv_image,
        (label, confidence),
        (adv_label, adv_confidence)
    )

def test_targeted_attack(targeted_adv_attack, model, device, target_label=2, eps=8/255., **kwargs):
    """Helper to test targeted adversarial attacks"""
    model.eval()
    
    # Load a MNIST image (unnormalized [0,1])
    image, true_label = load_example_image(preprocess=False)
    image = image.to(device)
    target_labels = torch.tensor([target_label]).to(device)

    # Get initial prediction using normalized image
    _, index, confidence = make_single_prediction(model, MNIST_NORMALIZE(image))
    label = get_imagenet_label(index)

    # Generate Adversarial Example
    adv_image = targeted_adv_attack(
        image.unsqueeze(0), 
        target_labels, 
        model, 
        MNIST_NORMALIZE, 
        eps=eps,
        **kwargs
    ).squeeze(0)

    # Get adversarial prediction
    _, adv_index, adv_confidence = make_single_prediction(model, MNIST_NORMALIZE(adv_image))
    adv_label = get_imagenet_label(adv_index)

    # Display Results
    display_adv_images(
        image, 
        adv_image,
        (label, confidence),
        (f"Target: {target_label} (Pred: {adv_label})", adv_confidence)
    )
