from .skin_enhancement import SkinEnhancement

def on_ui_tabs():
    return [(SkinEnhancement().process_image, "Skin Enhancement", "skin_enhancement")]