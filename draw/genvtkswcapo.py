import os
import vtk
import hashlib
# 全局颜色映射字典
global_color_map = {}


def read_swc(swc_file, scale=1.0):
    tree = []
    with open(swc_file) as fp:
        for line in fp:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            idx, type_, x, y, z, r, p = map(float, line.split()[:7])
            tree.append((int(idx), int(type_), x * scale, y *
                        scale, z * scale, r * scale, int(p)))
    return tree


def generate_deterministic_color(value):
    """
    生成一个确定性的颜色，确保相同的值总是映射到相同的颜色。
    """
    # 使用哈希函数生成一个伪随机颜色
    hash_object = hashlib.md5(str(value).encode())
    hash_digest = hash_object.hexdigest()
    r = int(hash_digest[0:2], 16)
    g = int(hash_digest[2:4], 16)
    b = int(hash_digest[4:6], 16)
    return (r, g, b)

def generate_rgb(type):
    if type == 0:
        return (255, 255, 255)
    if type == 1:
        # return (20, 20, 20)
        return (0, 20, 200)
    if type == 2 or type == 247:
        return (200, 20, 0)
    # if type == 2 or type == 247:
    #     return (0, 0, 0)
    if type == 3:
        return (0, 20, 200)
    if type == 4:
        return (200, 0, 200)
    if type == 5:
        return (0, 200, 200)
    if type == 6:
        return (200, 200, 0)
    if type == 7:
        return (0, 200, 20)
    if type == 8:
        return (250, 100, 120)

def parse_apo(apo_file):
    points = []
    with open(apo_file) as fp:
        for line in fp.readlines():
            line = line.strip()
            if not line or line.startswith('##') or line.startswith('#'):
                continue
            parts = line.split(',')
            x = float(parts[5])
            y = float(parts[6])
            z = float(parts[4])
            r = float(parts[7])  # Assuming radius is stored here
            # Assuming RGB values are these positions
            color = (int(parts[-3]), int(parts[-2]), int(parts[-1]))
            points.append((x, y, z, r, color))
    return points


def genVTK(input_p, apo_p=None, scale=1.0, output_p='./tmp/tmp.vtk'):
    swcraw = read_swc(input_p, scale=scale)
    apo_points = parse_apo(apo_p) if apo_p else []

    points = vtk.vtkPoints()
    lines = vtk.vtkCellArray()
    colors = vtk.vtkUnsignedCharArray()
    colors.SetNumberOfComponents(3)
    colors.SetName("Colors")

    NeuronHash = {node[0]: idx for idx, node in enumerate(swcraw)}

    for node in swcraw:
        idx = points.InsertNextPoint(node[2], node[3], node[4])
        type = node[1]
        # if node[5] == 300:
        #     type = 7
        # node_color = generate_deterministic_color(node[1])  # Generate color based on type
        node_color = generate_rgb(type)
        colors.InsertNextTuple3(*node_color)
        NeuronHash[node[0]] = idx

    for node in swcraw:
        p = node[6]
        if p != -1 and p in NeuronHash:
            line = vtk.vtkLine()
            line.GetPointIds().SetId(0, NeuronHash[node[0]])
            line.GetPointIds().SetId(1, NeuronHash[p])
            lines.InsertNextCell(line)

    polyData = vtk.vtkPolyData()
    polyData.SetPoints(points)
    polyData.SetLines(lines)
    # polyData.GetCellData().SetScalars(colors)  # 为线条设置颜色
    polyData.GetPointData().SetScalars(colors)

    appendFilter = vtk.vtkAppendPolyData()
    appendFilter.AddInputData(polyData)


    for x, y, z, r, color in apo_points:
        sphere = vtk.vtkSphereSource()
        sphere.SetCenter(x * scale, y * scale, z * scale)
        sphere.SetRadius(5 * scale)
        sphere.SetPhiResolution(16)
        sphere.SetThetaResolution(16)
        sphere.Update()

        numPts = sphere.GetOutput().GetNumberOfPoints()
        sphereColors = vtk.vtkUnsignedCharArray()
        sphereColors.SetNumberOfComponents(3)
        sphereColors.SetName("Colors")
        for _ in range(numPts):
            sphereColors.InsertNextTuple3(
                color[0], color[1], color[2])  # Set color for each point

        spherePolyData = sphere.GetOutput()
        spherePolyData.GetPointData().SetScalars(sphereColors)

        appendFilter.AddInputData(spherePolyData)

    appendFilter.Update()

    writer = vtk.vtkPolyDataWriter()
    writer.SetFileName(output_p)
    writer.SetInputData(appendFilter.GetOutput())
    writer.Write()

# filePath1 = R"Z:\SEU-ALLEN\Users\zhy\gold_silver_bronze\experiment_sup\auto_data\18454\18454_43754.swc"
# apoPath1 = R"Z:\SEU-ALLEN\Users\zhy\gold_silver_bronze\experiment_sup\silver_standard_sup_human_mobile_checked\12507_P061_T01_(1)_S022_-_MFG.R_R0919_OMZ_20240115_WYT.ano.apo"
# genVTK(filePath1, apo_p=None, scale=1.0, output_p="./data/tmp18454_43754_auto.vtk")

filePath2 = R"Z:\SEU-ALLEN\Users\zhy\for_paper\isolated_branch_sample\swc\04176_P019_T03_-S019_SFG_R0460_YW-20230414_NYT_stamp_2025_03_28_01_00.ano.eswc"
apoPath2 = R"D:\source\PythonProjecs\Utils\draw\data\bronze_data\12555_P061_T01_(1)_S013_-_MFG.R_R0919_OMZ_20240115_YW.ano.apo"
genVTK(filePath2, apo_p=None, scale=1.0, output_p=r"Z:\SEU-ALLEN\Users\zhy\for_paper\isolated_branch_sample\vtk\04176_isolated_branch.vtk")

# data_dir = r'Z:\SEU-ALLEN\Users\zhy\gold_silver_bronze\experiment_sup\7_gold_standard'
# for file in os.listdir(data_dir):
#     if file.endswith("swc"):
#         parts = file.split("_")
#         image = parts[0]
#         dotIndex = file.index(".")
#         neuron = file[0:dotIndex]
#         swc_path = os.path.join(data_dir, file)
#         output_path = './data/tmp' + neuron + '_gold.vtk'
#         genVTK(swc_path, None, 1.0, output_path)