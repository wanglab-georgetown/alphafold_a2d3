# visualize AlphaFold pdb with AlphaFold pLDDT color.
# It also highlight residues of interests as sphere.

import py3Dmol
import matplotlib.pyplot as plt

plddt_bands = ["#FF7D45", "#FFDB13", "#65CBF3", "#0053D6"]
styles = ["cartoon", "stick", "sphere"]
thresh = [
    "Very low (pLDDT < 50)",
    "Low (70 > pLDDT > 50)",
    "Confident (90 > pLDDT > 70)",
    "Very high (pLDDT > 90)",
]


def get_color(pLDDT):
    if pLDDT > 90:
        color = plddt_bands[3]
    elif pLDDT > 70:
        color = plddt_bands[2]
    elif pLDDT > 50:
        color = plddt_bands[1]
    else:
        color = plddt_bands[0]
    return color


def plot_plddt_legend(thresh, colors, title=None):
    plt.figure(figsize=(2, 2))
    for c in colors:
        plt.bar(0, 0, color=c)
    plt.legend(thresh, frameon=False, loc="center", fontsize=15)
    ax = plt.gca()
    ax.set_frame_on(False)
    ax.axis("off")
    if title:
        plt.title(title, fontsize=20, pad=20)
    return plt


def show_pdb(
    pdb_filename,
    style="cartoon",
    show_sidechains=False,
    mutation_resseq=[],
    mutation_style="sphere",
    mutation_color="magenta",
    width=800,
    height=800,
):
    if isinstance(mutation_color, str):
        mutation_color = [mutation_color] * len(mutation_resseq)

    with open(pdb_filename) as temptfile:
        pdb = "".join([x for x in temptfile])

    view = py3Dmol.view(
        js="https://3dmol.org/build/3Dmol.js",
        width=width,
        height=height,
    )
    view.addModelsAsFrames(pdb)
    if style not in styles:
        raise TypeError("style must be in {}".format(str(styles)))
    for i, line in enumerate(pdb.split("\n")):
        atom = line[:6].strip()
        if atom != "ATOM":
            continue
        pLDDT = float(line[60:66].strip())
        color = get_color(pLDDT)

        if style == "cartoon" and show_sidechains == True:
            view.setStyle(
                {"model": -1, "serial": i + 1}, {style: {"color": color}, "stick": {}}
            )
        else:
            view.setStyle({"model": -1, "serial": i + 1}, {style: {"color": color}})

        resseq = int(line[22:26].strip())
        if resseq in mutation_resseq:
            idx = list(mutation_resseq).index(resseq)
            view.setStyle(
                {"model": -1, "serial": i + 1},
                {mutation_style: {"color": mutation_color[idx]}},
            )
    plot_plddt_legend(thresh, plddt_bands).show()

    view.zoomTo()
    return view
