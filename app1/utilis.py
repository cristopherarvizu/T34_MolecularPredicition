import os
from rdkit import Chem
from rdkit.Chem import Draw
from django.conf import settings

def GenerateImageFromSmile(smile, file_name='molecule.png'):
    # Create a molecule object from the SMILES string
    mol = Chem.MolFromSmiles(smile)

    
    if mol is not None:  # Check if the molecule was created successfully
        # Generate the image
        img = Draw.MolToImage(mol, size=(300, 300))  # Adjust the size as needed
        # Create the full file path

        file_name = file_name.replace('\\', "--")
        file_path = os.path.join(settings.MEDIA_ROOT, 'molecules', file_name)
        # Save the image as a PNG file
        img.save(file_path, format='PNG')  # Change format to 'JPEG' for JPG files
        print(f"Image saved as {file_path}")
        return f'molecules/{file_name}'  # Return the relative path for the database
    else:
        print("Error: Invalid SMILES string.")
        return None