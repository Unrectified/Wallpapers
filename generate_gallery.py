#!/usr/bin/env python3
"""
Script pour générer automatiquement la galerie de wallpapers
Ce script scanne tous les dossiers et trouve toutes les images
"""

import os
import json
from pathlib import Path

# Extensions d'images supportées
IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.svg'}

# Dossiers à ignorer
IGNORE_FOLDERS = {'prewiew', '.git', '__pycache__', 'node_modules','Moi'}

def find_images(base_path):
    """Trouve toutes les images dans le répertoire et ses sous-dossiers"""
    wallpapers = []
    base_path = Path(base_path)
    
    # Parcourir tous les dossiers
    for root, dirs, files in os.walk(base_path):
        # Ignorer certains dossiers
        dirs[:] = [d for d in dirs if d not in IGNORE_FOLDERS]
        
        # Chemin relatif depuis la base
        rel_path = Path(root).relative_to(base_path)
        
        # Trouver toutes les images dans ce dossier
        images = []
        for file in files:
            if Path(file).suffix.lower() in IMAGE_EXTENSIONS:
                images.append(file)
        
        # Si des images sont trouvées, ajouter au résultat
        if images:
            folder_path = str(rel_path) if str(rel_path) != '.' else 'root'
            wallpapers.append({
                'folder': folder_path,
                'images': sorted(images)
            })
    
    return sorted(wallpapers, key=lambda x: x['folder'])

def generate_js_array(wallpapers):
    """Génère le code JavaScript pour le tableau wallpapers"""
    js_code = "        const wallpapers = [\n"
    
    for item in wallpapers:
        folder = item['folder'].replace("'", "\\'")
        js_code += f"            {{ folder: '{folder}', images: [\n"
        
        for img in item['images']:
            img_escaped = img.replace("'", "\\'")
            js_code += f"                '{img_escaped}',\n"
        
        js_code += "            ]},\n"
    
    js_code += "        ];\n"
    return js_code

def update_html_file(html_path, wallpapers):
    """Met à jour le fichier HTML avec la liste des wallpapers"""
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Générer le nouveau code JavaScript
    new_js = generate_js_array(wallpapers)
    
    # Trouver et remplacer le tableau wallpapers
    start_marker = "        const wallpapers = ["
    end_marker = "        ];"
    
    start_idx = content.find(start_marker)
    if start_idx == -1:
        print("❌ Erreur: Impossible de trouver le tableau wallpapers dans le HTML")
        return False
    
    # Trouver la fin du tableau
    end_idx = content.find(end_marker, start_idx) + len(end_marker)
    if end_idx == -1:
        print("❌ Erreur: Impossible de trouver la fin du tableau wallpapers")
        return False
    
    # Remplacer le contenu
    new_content = content[:start_idx] + new_js + content[end_idx+1:]
    
    # Écrire le nouveau fichier
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return True

def main():
    # Chemin du dossier contenant index.html (dossier prewiew)
    script_dir = Path(__file__).parent
    project_root = script_dir  # On scanne uniquement le dossier actuel
    html_file = script_dir / 'index.html'

    print("🔍 Scanning pour des wallpapers...")
    print(f"📂 Dossier racine: {project_root}")

    # Trouver toutes les images
    wallpapers = find_images(project_root)

    # Statistiques
    total_images = sum(len(item['images']) for item in wallpapers)
    print(f"\n✅ Trouvé {total_images} images dans {len(wallpapers)} dossiers:")

    for item in wallpapers:
        print(f"   📁 {item['folder']}: {len(item['images'])} images")

    # Mettre à jour le fichier HTML
    print(f"\n📝 Mise à jour de {html_file.name}...")
    if update_html_file(html_file, wallpapers):
        print("✅ Fichier HTML mis à jour avec succès!")
        print(f"\n🌐 Ouvrez {html_file} dans votre navigateur pour voir la galerie")
    else:
        print("❌ Échec de la mise à jour du fichier HTML")
        return 1

    return 0

if __name__ == '__main__':
    exit(main())
