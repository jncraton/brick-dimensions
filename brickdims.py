import argparse
import sys
import os

ldraw_path = "ldraw"

def compose_transforms(t1, t2):
    """Compose two transformation matrices (t1 followed by t2)"""
    a1, b1, c1, d1, e1, f1, g1, h1, i1, x1, y1, z1 = t1
    a2, b2, c2, d2, e2, f2, g2, h2, i2, x2, y2, z2 = t2

    # Rotation part
    a = a1 * a2 + b1 * d2 + c1 * g2
    b = a1 * b2 + b1 * e2 + c1 * h2
    c = a1 * c2 + b1 * f2 + c1 * i2
    d = d1 * a2 + e1 * d2 + f1 * g2
    e = d1 * b2 + e1 * e2 + f1 * h2
    f = d1 * c2 + e1 * f2 + f1 * i2
    g = g1 * a2 + h1 * d2 + i1 * g2
    h = g1 * b2 + h1 * e2 + i1 * h2
    i = g1 * c2 + h1 * f2 + i1 * i2

    # Translation part
    x0 = a1 * x2 + b1 * y2 + c1 * z2 + x1
    y0 = d1 * x2 + e1 * y2 + f1 * z2 + y1
    z0 = g1 * x2 + h1 * y2 + i1 * z2 + z1

    return (a, b, c, d, e, f, g, h, i, x0, y0, z0)


def apply_transform(transform, vertex):
    """Apply a transformation matrix to a vertex"""
    a, b, c, d, e, f, g, h, i, x0, y0, z0 = transform
    x, y, z = vertex
    new_x = a * x + b * y + c * z + x0
    new_y = d * x + e * y + f * z + y0
    new_z = g * x + h * y + i * z + z0
    return (new_x, new_y, new_z)


def parse_ldraw_file(file_path, current_transform=None):
    """Parse an LDraw file and return a list of triangles with transformations applied"""
    if current_transform is None:
        current_transform = (1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0)  # Identity matrix

    triangles = []

    try:
        with open(file_path, "r", encoding="latin1") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("0"):
                    continue
                parts = line.split()
                if not parts:
                    continue
                cmd_type = parts[0]

                if cmd_type == "3":
                    # Triangle command: 3 <color> <x1> <y1> <z1> <x2> <y2> <z2> <x3> <y3> <z3>
                    if len(parts) < 12:
                        continue
                    try:
                        x1, y1, z1 = float(parts[2]), float(parts[3]), float(parts[4])
                        x2, y2, z2 = float(parts[5]), float(parts[6]), float(parts[7])
                        x3, y3, z3 = float(parts[8]), float(parts[9]), float(parts[10])

                        # Apply current transformation
                        v1 = apply_transform(current_transform, (x1, y1, z1))
                        v2 = apply_transform(current_transform, (x2, y2, z2))
                        v3 = apply_transform(current_transform, (x3, y3, z3))

                        triangles.append((v1, v2, v3))
                    except (IndexError, ValueError):
                        continue

                elif cmd_type == "4":
                    # Quad command: 4 <color> <x1> <y1> <z1> <x2> <y2> <z2> <x3> <y3> <z3> <x4> <y4> <z4>
                    if len(parts) < 14:
                        continue
                    try:
                        x1, y1, z1 = float(parts[2]), float(parts[3]), float(parts[4])
                        x2, y2, z2 = float(parts[5]), float(parts[6]), float(parts[7])
                        x3, y3, z3 = float(parts[8]), float(parts[9]), float(parts[10])
                        x4, y4, z4 = (
                            float(parts[11]),
                            float(parts[12]),
                            float(parts[13]),
                        )

                        # Apply current transformation
                        v1 = apply_transform(current_transform, (x1, y1, z1))
                        v2 = apply_transform(current_transform, (x2, y2, z2))
                        v3 = apply_transform(current_transform, (x3, y3, z3))
                        v4 = apply_transform(current_transform, (x4, y4, z4))

                        # Split quad into two triangles
                        triangles.append((v1, v2, v3))
                        triangles.append((v1, v3, v4))
                    except (IndexError, ValueError):
                        continue

                elif cmd_type == "1":
                    # Subfile command: 1 <color> <x> <y> <z> <a> <b> <c> <d> <e> <f> <g> <h> <i> <file>
                    if len(parts) < 15:
                        continue
                    try:
                        # Extract transformation matrix
                        x, y, z = float(parts[2]), float(parts[3]), float(parts[4])
                        a, b, c = float(parts[5]), float(parts[6]), float(parts[7])
                        d, e, f = float(parts[8]), float(parts[9]), float(parts[10])
                        g, h, i = float(parts[11]), float(parts[12]), float(parts[13])
                        subfile = parts[14]

                        # Create transformation matrix for this subfile
                        sub_transform = (a, b, c, d, e, f, g, h, i, x, y, z)

                        # Compose with current transformation
                        composed_transform = compose_transforms(
                            current_transform, sub_transform
                        )

                        # Find subfile path
                        subfile_path = ""
                        for subdir in [False, "parts", "p"]:
                            if subdir:
                                search_path = ldraw_path + "/" + subdir
                            else:
                                search_path = ldraw_path
                            subfile_path = os.path.join(search_path, subfile)
                            subfile_path = subfile_path.replace("\\", "/")
                            if not os.path.exists(subfile_path):
                                # Try with .dat extension if not present
                                if not subfile.lower().endswith(".dat"):
                                    subfile_path = os.path.join(
                                        search_path, subfile + ".dat"
                                    )

                            if not os.path.exists(subfile_path):
                                # Try with uppercase .DAT extension
                                subfile_path = subfile_path.replace(".DAT", ".dat")

                            if not os.path.exists(subfile_path):
                                # Try with all lowercase
                                subfile_path = subfile_path.lower()

                            if os.path.exists(subfile_path):
                                break

                        if os.path.exists(subfile_path):
                            # Recursively parse subfile
                            sub_triangles = parse_ldraw_file(subfile_path, composed_transform)
                            triangles.extend(sub_triangles)
                        else:
                            print(
                                f"Warning: Subfile {subfile} not found in {ldraw_path}",
                                file=sys.stderr,
                            )
                    except (IndexError, ValueError):
                        continue
    except Exception as e:
        print(f"Error reading file {file_path}: {e}", file=sys.stderr)
        return []

    return triangles


def compute_bounding_box(triangles):
    """Compute the axis-aligned bounding box of a list of triangles"""
    if not triangles:
        return (0, 0, 0, 0, 0, 0)
    xs, ys, zs = [], [], []
    for tri in triangles:
        for vertex in tri:
            xs.append(vertex[0])
            ys.append(vertex[1])
            zs.append(vertex[2])
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    min_z, max_z = min(zs), max(zs)
    return (min_x, min_y, min_z, max_x, max_y, max_z)


def get_bounding_box(part):
    """Get bounding box for a part

    >>> get_bounding_box("3001")
    (-40.0, -4.0, -20.0, 40.0, 24.0, 20.0)

    >>> get_bounding_box("3005")
    (-10.0, -4.0, -10.0, 10.0, 24.0, 10.0)
    """
    file_path = f"{ldraw_path}/parts/{part}.dat"

    try:
        triangles = parse_ldraw_file(file_path)
    except Exception as e:
        print(f"Error reading file: {e}", file=sys.stderr)

    if not triangles:
        print(f"No triangles found in the LDraw file: {file_path}", file=sys.stderr)

    return compute_bounding_box(triangles)


def get_dimensions(part):
    """Get part dimensions in centimeters

    Dimension order is widgt, length, height

    This matches part names e.g. 1x5x1 Brick

    >>> get_dimensions("3001")
    (1.6, 3.2, 1.12)

    >>> get_dimensions("3005")
    (0.8, 0.8, 1.12)

    >>> get_dimensions("2555")
    (0.8, 0.8, 0.72)

    >>> get_dimensions("6019")
    (1.36, 0.8, 0.64)

    >>> get_dimensions("6558") # doctest: +ELLIPSIS
    (0.6..., 2.4, 0.6...)
    """

    bounding_box_ldu = get_bounding_box(part)
    dims_ldu = (
        abs(bounding_box_ldu[2] - bounding_box_ldu[5]),
        abs(bounding_box_ldu[0] - bounding_box_ldu[3]),
        abs(bounding_box_ldu[1] - bounding_box_ldu[4]),
    )
    ldu_to_cm = 0.04
    return tuple(coord * ldu_to_cm for coord in dims_ldu)


def main():
    parser = argparse.ArgumentParser(
        description="Compute dimensions of a LEGO brick from an LDraw file."
    )
    parser.add_argument("file", help="Path to the LDraw parts")
    args = parser.parse_args()

    with open(args.file) as f:
        print("part_num,width,length,height")
        for part in f.readlines():
            part = part.strip()
            dims_cm = get_dimensions(part)

            if sum(dims_cm) <= 0:
                print(f"Excluding part {part} with zero volume", file=sys.stderr)
            else:
                print(f"{part},{dims_cm[0]:.02f},{dims_cm[1]:.02f},{dims_cm[2]:.02f}")


if __name__ == "__main__":
    main()
