M_WIDTH = 700 
M_HEIGHT = 700

def M_CELL_SIZE(map):
    rows = len(map)
    cols = len(map[0]) if rows > 0 else 0
    cell_size = min(M_WIDTH // cols, M_HEIGHT // rows) if cols > 0 else 0
    return cell_size

