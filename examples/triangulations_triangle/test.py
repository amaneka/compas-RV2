import triangle
from compas.datastructures import Mesh
from compas_plotters import MeshPlotter

tris = {
    'vertices':
    [
        [40.50164006943794, -9.3072025435138173],
        [42.550171883893668, -9.2875863829676977],
        [44.596929693657792, -9.2026750230809462],
        [46.63523154687195, -9.0014943108559677],
        [48.644240298604799, -8.6066034791915804],
        [50.575164188611232, -7.9291066852071808],
        [52.355582964345807, -6.9213216937559681],
        [53.950088594022624, -5.6376349375583237],
        [55.391900031594254, -4.1831292950747425],
        [56.731739986471609, -2.6336313077408882],
        [57.384699641674139, -4.7974734522259359],
        [58.21079861835014, -6.8994812647262673],
        [59.523775602764687, -8.7240694127032512],
        [61.386052527702795, -9.9914895240340922],
        [63.463619301616063, -10.87870925928555],
        [65.60247613749732, -11.609314635871346],
        [63.748303388992298, -12.51191949229619],
        [61.939285535447624, -13.501802087360145],
        [60.185112408416614, -14.585866695208868],
        [58.487224080142802, -15.756258777204302],
        [56.827744415290439, -16.980735986577972],
        [55.194873835725758, -18.240212404946131],
        [53.67607342071657, -19.633578387703153],
        [52.362594322795069, -21.221145609720544],
        [51.289385488044843, -22.980425990942635],
        [50.43804508649248, -24.857765954145059],
        [49.210730622697987, -22.990109384645272],
        [47.765368566072908, -21.288967466758166],
        [45.932074014880939, -20.026500718717251],
        [43.842248425993418, -19.243442132954993],
        [41.647077257820165, -18.83049319546771],
        [39.42023689487263, -18.640815013117766],
        [40.896209772589209, -17.106914568311023],
        [41.934218978189314, -15.258719278720919],
        [42.197096768293676, -13.156204518695226],
        [41.618893178670589, -11.118506907801205],
        [40.50164006943794, -9.3072025435138173],
        [42.571435534841761, -9.6912975801336181],
        [44.64599633021345, -10.048749385932098],
        [46.725269884271285, -10.377666313976784],
        [48.809156194309054, -10.675948002635002],
        [50.897493407086557, -10.941255249258498],
        [52.990040386245319, -11.170975026917201],
        [55.086453039272442, -11.362179538959747],
        [57.186252765869156, -11.5115785558291],
        [59.288788992142102, -11.615464475155511],
        [61.393183988079443, -11.669648735943642],
        [63.498265554807489, -11.669390061413001],
        [65.60247613749732, -11.609314635871346]
    ],
    'segments':
    [
        (0, 1), (1, 2), (2, 3), (3, 4), (4, 5),
        # (5, 6), (6, 7), (7, 8), (8, 9), (9, 10), (10, 11), (11, 12), (12, 13), (13, 14), (14, 15), (15, 16), (16, 17), (17, 18), (18, 19), (19, 20), (20, 21), (21, 22), (22, 23), (23, 24), (24, 25), (25, 26), (26, 27), (27, 28), (28, 29), (29, 30), (30, 31), (31, 32), (32, 33), (33, 34), (34, 35),
        # (35, 0),
        # (36, 37), (37, 38), (38, 39), (39, 40), (40, 41), (41, 42), (42, 43), (43, 44), (44, 45), (45, 46), (46, 47), (47, 48)
    ]
}

result = triangle.triangulate(tris, opts='pa0.05q')

vertices = [[x, y, 0] for x, y in result['vertices']]
faces = result['triangles'].tolist()

mesh = Mesh.from_vertices_and_faces(vertices, faces)

plotter = MeshPlotter(mesh, figsize=(8, 5))
plotter.draw_faces()
plotter.show()
