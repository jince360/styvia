from django import template
register = template.Library()
@register.filter
def color_to_hex(color_name):

    color_map = {
        'black': '#000000',
        'white': '#FFFFFF',
        'red': '#FF0000',
        'blue': '#0000FF',
        'sky blue': '#87CEEB',
        'light blue': '#ADD8E6',
        'navy blue': '#000080',
        'dark blue': '#00008B',
        'green': '#008000',
        'light green': '#90EE90',
        'dark green': '#006400',
        'yellow': '#FFFF00',
        'orange': '#FFA500',
        'pink': '#FFC0CB',
        'hot pink': '#FF69B4',
        'purple': '#800080',
        'brown': '#A52A2A',
        'grey': '#808080',
        'gray': '#808080',
        'beige': '#F5F5DC',
        'maroon': '#800000',
        'navy': '#000080',
        'olive': '#808000',
        'teal': '#008080',
        'coral': '#FF7F50',
        'gold': '#FFD700',
        'silver': '#C0C0C0',
        'cream': '#FFFDD0',
        'burgundy': '#800020',
        'mint': '#98FF98',
    }
    

    color_lower = color_name.lower().strip()
    
    for key, value in color_map.items():
        if key in color_lower:
            return value
    
    return '#CCCCCC'