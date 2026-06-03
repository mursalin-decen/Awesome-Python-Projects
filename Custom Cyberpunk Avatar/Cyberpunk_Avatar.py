#No -1 :


'''import python_avatars as pa
from IPython.display import SVG, display

avatar = pa.Avatar(
    style = pa.AvatarStyle.CIRCLE,
    hair_color ="#00ffff",
    background_color = "#111111",
)

avatar.render("cyber_avatar.svg")

display(SVG("cyber_avatar.svg"))

'''




#No -2
import python_avatars as pa
from IPython.display import SVG, display

avatar = pa.Avatar(
    style=pa.AvatarStyle.CIRCLE,
    background_color="#0d1117",      # Hex values work for background
    skin_color=pa.SkinColor.LIGHT,
    
    # Hair/Head wear configuration
    top=pa.HairType.SHORT_WAVED,     # Just 'top', not 'top_type' or 'hair_type'
    hair_color=pa.HairColor.BLACK,   # Use the library's HairColor enum
    
    # Eyes & Face
    eyes=pa.EyeType.DEFAULT,
    eyebrows=pa.EyebrowType.DEFAULT,
    mouth=pa.MouthType.SMILE,
    
    # Clothing configuration
    clothing=pa.ClothingType.HOODIE, # Just 'clothing', not 'clothing_type'
    clothing_color=pa.ClothingColor.HEATHER, # Use ClothingColor enum
    
    # Accessories
    accessory=pa.AccessoryType.PRESCRIPTION_2 # Just 'accessory', not 'accessory_type'
)

# Render and display matching filenames
avatar.render("cyberpunk_avatar.svg")
display(SVG("cyberpunk_avatar.svg"))

print("Cyberpunk Avatar Created Successfully!")