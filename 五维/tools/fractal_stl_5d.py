"""
未闭环数学 · 五维分形STL生成器
基于五维特征数 D5 = 24681
"""

import math
import random

def generate_5d_fractal(size=100, grid_size=30):
    """
    生成五维分形结构
    使用 grid_size³ 网格，保留 24681 个单元格
    """
    print(f"🌌 生成五维分形（{grid_size}³网格，保留24681单元格）...")
    
    total_cells = grid_size ** 3
    if total_cells < 24681:
        raise ValueError(f"网格太小！{grid_size}³={total_cells} < 24681")
    
    triangles = []
    cell_size = size / grid_size
    
    # 生成所有单元格坐标
    all_cells = []
    for x in range(grid_size):
        for y in range(grid_size):
            for z in range(grid_size):
                all_cells.append((x, y, z))
    
    # 随机选择24681个单元格
    selected_cells = random.sample(all_cells, 24681)
    print(f"   从 {total_cells} 个单元格中选择 {len(selected_cells)} 个")
    
    # 为每个选中的单元格生成立方体
    for cx, cy, cz in selected_cells:
        center_x = (cx + 0.5) * cell_size - size/2
        center_y = (cy + 0.5) * cell_size - size/2
        center_z = (cz + 0.5) * cell_size - size/2
        
        half = cell_size / 2 * 0.85  # 稍微缩小，留出间隙
        vertices = [
            (center_x-half, center_y-half, center_z-half),
            (center_x+half, center_y-half, center_z-half),
            (center_x+half, center_y+half, center_z-half),
            (center_x-half, center_y+half, center_z-half),
            (center_x-half, center_y-half, center_z+half),
            (center_x+half, center_y-half, center_z+half),
            (center_x+half, center_y+half, center_z+half),
            (center_x-half, center_y+half, center_z+half)
        ]
        
        cube_triangles = [
            [vertices[0], vertices[1], vertices[2]], [vertices[0], vertices[2], vertices[3]],
            [vertices[4], vertices[5], vertices[6]], [vertices[4], vertices[6], vertices[7]],
            [vertices[0], vertices[1], vertices[5]], [vertices[0], vertices[5], vertices[4]],
            [vertices[2], vertices[3], vertices[7]], [vertices[2], vertices[7], vertices[6]],
            [vertices[1], vertices[2], vertices[6]], [vertices[1], vertices[6], vertices[5]],
            [vertices[0], vertices[3], vertices[7]], [vertices[0], vertices[7], vertices[4]]
        ]
        
        triangles.extend(cube_triangles)
    
    print(f"   生成 {len(triangles)} 个三角形")
    return triangles

def write_stl(triangles, filename="fractal_5d.stl"):
    """写入ASCII STL文件"""
    with open(filename, 'w') as f:
        f.write(f"solid fractal_5d\n")
        for tri in triangles:
            v0, v1, v2 = tri
            ux, uy, uz = v1[0]-v0[0], v1[1]-v0[1], v1[2]-v0[2]
            vx, vy, vz = v2[0]-v0[0], v2[1]-v0[1], v2[2]-v0[2]
            
            nx = uy*vz - uz*vy
            ny = uz*vx - ux*vz
            nz = ux*vy - uy*vx
            
            length = math.sqrt(nx*nx + ny*ny + nz*nz)
            if length > 0:
                nx, ny, nz = nx/length, ny/length, nz/length
            
            f.write(f"  facet normal {nx:.6f} {ny:.6f} {nz:.6f}\n")
            f.write(f"    outer loop\n")
            for vertex in tri:
                f.write(f"      vertex {vertex[0]:.6f} {vertex[1]:.6f} {vertex[2]:.6f}\n")
            f.write(f"    endloop\n")
            f.write(f"  endfacet\n")
        f.write(f"endsolid fractal_5d\n")
    
    print(f"✅ STL文件已生成: {filename}")

if __name__ == "__main__":
    triangles = generate_5d_fractal(size=100, grid_size=30)
    write_stl(triangles)