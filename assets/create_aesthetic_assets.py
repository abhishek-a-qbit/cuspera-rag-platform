import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import base64
from io import BytesIO
import requests

def create_6sense_logo():
    """Create a beautiful 6sense logo"""
    fig, ax = plt.subplots(figsize=(4, 4), facecolor='white')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Create gradient background circle
    gradient = np.linspace(0, 1, 256).reshape(256, 1)
    gradient = np.hstack((gradient, gradient))
    
    # Draw gradient circle
    circle = plt.Circle((5, 5), 4, color='#667eea', alpha=0.1)
    ax.add_patch(circle)
    circle2 = plt.Circle((5, 5), 3.5, color='#764ba2', alpha=0.2)
    ax.add_patch(circle2)
    circle3 = plt.Circle((5, 5), 3, color='#667eea', alpha=0.3)
    ax.add_patch(circle3)
    
    # Add 6sense text
    ax.text(5, 5.5, '6sense', fontsize=24, fontweight='bold', 
            ha='center', va='center', color='#667eea')
    ax.text(5, 4.5, 'Revenue AI', fontsize=10, 
            ha='center', va='center', color='#764ba2')
    
    # Add decorative elements
    for i in range(8):
        angle = i * np.pi / 4
        x = 5 + 2.5 * np.cos(angle)
        y = 5 + 2.5 * np.sin(angle)
        ax.plot([5, x], [5, y], color='#667eea', alpha=0.3, linewidth=1)
        ax.scatter(x, y, color='#764ba2', s=20, alpha=0.6)
    
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', dpi=150, facecolor='white')
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode()
    plt.close()
    return img_str

def create_background_pattern():
    """Create a beautiful background pattern"""
    fig, ax = plt.subplots(figsize=(10, 10), facecolor='white')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Create geometric pattern
    for i in range(10):
        for j in range(10):
            x, y = i + 0.5, j + 0.5
            
            # Create gradient circles
            size = 0.3 + 0.1 * np.sin(i * j)
            alpha = 0.1 + 0.05 * np.cos(i + j)
            
            circle = plt.Circle((x, y), size, 
                             color='#667eea', alpha=alpha)
            ax.add_patch(circle)
            
            # Add connecting lines
            if i < 9:
                ax.plot([x, x+1], [y, y], color='#764ba2', alpha=0.05, linewidth=0.5)
            if j < 9:
                ax.plot([x, x], [y, y+1], color='#667eea', alpha=0.05, linewidth=0.5)
    
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', dpi=100, facecolor='white')
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode()
    plt.close()
    return img_str

def create_hero_image():
    """Create a hero image for the dashboard"""
    fig, ax = plt.subplots(figsize=(12, 6), facecolor='white')
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6)
    ax.axis('off')
    
    # Create gradient background
    gradient = np.linspace(0, 1, 256).reshape(256, 1)
    gradient = np.hstack((gradient, gradient))
    ax.imshow(gradient, extent=[0, 12, 0, 6], aspect='auto', cmap='viridis', alpha=0.3)
    
    # Add abstract data visualization elements
    x = np.linspace(0, 12, 100)
    y1 = 3 + 1.5 * np.sin(x * 0.5) * np.exp(-x * 0.05)
    y2 = 3 + 1.2 * np.cos(x * 0.7) * np.exp(-x * 0.03)
    
    ax.fill_between(x, 3, y1, color='#667eea', alpha=0.3)
    ax.fill_between(x, 3, y2, color='#764ba2', alpha=0.3)
    ax.plot(x, y1, color='#667eea', linewidth=3)
    ax.plot(x, y2, color='#764ba2', linewidth=3)
    
    # Add data points
    for i in range(0, 100, 10):
        ax.scatter(x[i], y1[i], color='white', s=50, alpha=0.8, edgecolor='#667eea', linewidth=2)
        ax.scatter(x[i], y2[i], color='white', s=50, alpha=0.8, edgecolor='#764ba2', linewidth=2)
    
    # Add title text
    ax.text(6, 5, 'Advanced Analytics', fontsize=32, fontweight='bold', 
            ha='center', va='center', color='white')
    ax.text(6, 4.2, 'Real-time Intelligence & Insights', fontsize=18, 
            ha='center', va='center', color='white', alpha=0.9)
    
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', dpi=150, facecolor='white')
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode()
    plt.close()
    return img_str

def create_feature_icons():
    """Create icons for different features"""
    icons = {}
    
    # Dashboard icon
    fig, ax = plt.subplots(figsize=(2, 2), facecolor='white')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Draw dashboard icon
    rect = plt.Rectangle((1, 2), 8, 6, fill=False, edgecolor='#667eea', linewidth=2)
    ax.add_patch(rect)
    
    # Add chart elements
    ax.bar([2, 3, 4], [3, 5, 4], color='#764ba2', alpha=0.7)
    ax.plot([6, 7, 8, 9], [4, 6, 5, 7], color='#667eea', linewidth=2)
    
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', dpi=100, facecolor='white')
    buf.seek(0)
    icons['dashboard'] = base64.b64encode(buf.read()).decode()
    plt.close()
    
    # Analytics icon
    fig, ax = plt.subplots(figsize=(2, 2), facecolor='white')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Draw analytics icon (magnifying glass with chart)
    circle = plt.Circle((5, 5), 3, fill=False, edgecolor='#667eea', linewidth=2)
    ax.add_patch(circle)
    ax.plot([7, 8.5], [3, 1.5], color='#667eea', linewidth=3)
    
    # Add small chart inside
    x = np.linspace(3, 7, 20)
    y = 5 + 1.5 * np.sin(x)
    ax.plot(x, y, color='#764ba2', linewidth=2)
    
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', dpi=100, facecolor='white')
    buf.seek(0)
    icons['analytics'] = base64.b64encode(buf.read()).decode()
    plt.close()
    
    # ROI icon
    fig, ax = plt.subplots(figsize=(2, 2), facecolor='white')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Draw ROI icon (dollar sign with arrow)
    ax.text(5, 5, '$', fontsize=40, fontweight='bold', 
            ha='center', va='center', color='#667eea')
    ax.arrow(3, 7, 4, 0, head_width=0.5, head_length=0.5, 
            fc='#764ba2', ec='#764ba2', linewidth=2)
    
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', dpi=100, facecolor='white')
    buf.seek(0)
    icons['roi'] = base64.b64encode(buf.read()).decode()
    plt.close()
    
    return icons

def create_status_badges():
    """Create status badges"""
    badges = {}
    
    # Online badge
    fig, ax = plt.subplots(figsize=(1, 0.5), facecolor='white')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.axis('off')
    
    # Green background
    rect = plt.Rectangle((0, 0), 10, 5, color='#4CAF50', alpha=0.9)
    ax.add_patch(rect)
    
    ax.text(5, 2.5, 'ONLINE', fontsize=8, fontweight='bold', 
            ha='center', va='center', color='white')
    
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', dpi=100, facecolor='white')
    buf.seek(0)
    badges['online'] = base64.b64encode(buf.read()).decode()
    plt.close()
    
    # Premium badge
    fig, ax = plt.subplots(figsize=(1, 0.5), facecolor='white')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.axis('off')
    
    # Gold background
    rect = plt.Rectangle((0, 0), 10, 5, color='#FFD700', alpha=0.9)
    ax.add_patch(rect)
    
    ax.text(5, 2.5, 'PREMIUM', fontsize=8, fontweight='bold', 
            ha='center', va='center', color='white')
    
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', dpi=100, facecolor='white')
    buf.seek(0)
    badges['premium'] = base64.b64encode(buf.read()).decode()
    plt.close()
    
    return badges

# Generate all assets
if __name__ == "__main__":
    print("Creating aesthetic assets...")
    
    # Create logo
    logo = create_6sense_logo()
    print("✅ Logo created")
    
    # Create background pattern
    pattern = create_background_pattern()
    print("✅ Background pattern created")
    
    # Create hero image
    hero = create_hero_image()
    print("✅ Hero image created")
    
    # Create feature icons
    icons = create_feature_icons()
    print("✅ Feature icons created")
    
    # Create status badges
    badges = create_status_badges()
    print("✅ Status badges created")
    
    # Save assets to a file
    assets_data = {
        'logo': logo,
        'background_pattern': pattern,
        'hero_image': hero,
        'icons': icons,
        'badges': badges
    }
    
    import json
    with open('assets_data.json', 'w') as f:
        json.dump(assets_data, f)
    
    print("✅ All assets saved to assets_data.json")
    print("\nAssets ready for use in enhanced UI!")
