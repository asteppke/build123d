from cadquery import Vector
from build123d_common import *
from build_line import *
from build_sketch import *

with BuildSketch() as flag:
    PushPoints((-0.75, 0.5), (0.75, 0.5))
    Rect(0.5, 1)
    with BuildLine() as leaf:
        l1 = Polyline((0.0000, 0.0771), (0.0187, 0.0771), (0.0094, 0.2569))
        l2 = Polyline((0.0325, 0.2773), (0.2115, 0.2458), (0.1873, 0.3125))
        RadiusArc(l1 @ 1, l2 @ 0, 0.0271)
        l3 = Polyline((0.1915, 0.3277), (0.3875, 0.4865), (0.3433, 0.5071))
        TangentArc(l2 @ 1, l3 @ 0, tangent=l2 % 1)
        l4 = Polyline((0.3362, 0.5235), (0.375, 0.6427), (0.2621, 0.6188))
        SagittaArc(l3 @ 1, l4 @ 0, 0.003)
        l5 = Polyline((0.2469, 0.6267), (0.225, 0.6781), (0.1369, 0.5835))
        ThreePointArc(l4 @ 1, (l4 @ 1 + l5 @ 0) * 0.5 + Vector(-0.002, -0.002), l5 @ 0)
        l6 = Polyline((0.1138, 0.5954), (0.1562, 0.8146), (0.0881, 0.7752))
        Spline(l5 @ 1, l6 @ 0, tangents=(l5 % 1, l6 % 0), tangent_scalars=(2, 2))
        l7 = Line((0.0692, 0.7808), (0.0000, 0.9167))
        TangentArc(l6 @ 1, l7 @ 0, tangent=l6 % 1)
        Mirror(*leaf.edges(), axis=Axis.Y)
    BuildFace(*flag.pending_edges)

with BuildSketch() as din:
    PushPoints((0, 0.5))
    Rect(35, 1)
    PushPoints((0, 7.5 / 2))
    Rect(27, 7.5)
    PushPoints((0, 6.5 / 2))
    Rect(25, 6.5, mode=Mode.SUBTRACTION)
    inside_vertices = list(
        filter(
            lambda v: 7.5 > v.Y > 0 and -17.5 < v.X < 17.5,
            din.vertices(),
        )
    )
    FilletSketch(*inside_vertices, radius=0.8)
    outside_vertices = list(
        filter(
            lambda v: (v.Y == 0.0 or v.Y == 7.5) and -17.5 < v.X < 17.5,
            din.vertices(),
        )
    )
    FilletSketch(*outside_vertices, radius=1.8)

if "show_object" in locals():
    show_object(flag.sketch, name="flag")
    show_object(din.sketch, name="din rail")