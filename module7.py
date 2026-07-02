import pooch
import xarray as xr
import matplotlib.pyplot as plt
import pygmt

# =========================
# DADOS: dorsais.txt
# =========================
dorsais_txt_url = "https://drive.google.com/uc?export=download&id=1L15yntZf9M8QR37LsiRMDeCUMFqcaONH"
dorsais_txt_md5 = "md5:f8fc4486f6801aa85418cf50e337364a"
dorsais_txt_filename = "dorsais.txt"

cache_path = pooch.os_cache("meu_projeto")

dorsais_txt_path = pooch.retrieve(
    url=dorsais_txt_url,
    known_hash=dorsais_txt_md5,
    fname=dorsais_txt_filename,
    path=cache_path,
)

with open(dorsais_txt_path, "r", encoding="utf-8") as f:
    dorsais_txt_content = f.read()

# =========================
# DADOS: topografia (netCDF)
# =========================
topografia_nc_url = "https://drive.google.com/uc?export=download&id=1cfT3ZQyU131Wvx_LylR7WnRin4WpcxdQ"
topografia_nc_md5 = "md5:0799a5d06e5326b54882c06741eb712a"
topografia_nc_filename = "topografia.nc"

topografia_nc_path = pooch.retrieve(
    url=topografia_nc_url,
    known_hash=topografia_nc_md5,
    fname=topografia_nc_filename,
    path=cache_path,
)

# Carrega a malha de topografia como um DataArray
topografia = xr.load_dataarray(topografia_nc_path)

# =========================
# DADOS: magnetic_anomaly (netCDF)
# =========================
magnetic_anomaly_nc_url = "https://drive.google.com/uc?export=download&id=14lrKMRQVUkBgeiwJ-QkK2ib4M47FZmf4"
magnetic_anomaly_nc_md5 = "md5:6162e664ed36fc7684e0cd7b69960e15"
magnetic_anomaly_nc_filename = "magnetic_anomaly.nc"

magnetic_anomaly_nc_path = pooch.retrieve(
    url=magnetic_anomaly_nc_url,
    known_hash=magnetic_anomaly_nc_md5,
    fname=magnetic_anomaly_nc_filename,
    path=cache_path,
)

# Carrega a malha de magnetic_anomaly como um DataArray
magnetic_anomaly = xr.load_dataarray(magnetic_anomaly_nc_path)
magnetic_anomaly = magnetic_anomaly.sortby("latitude")

# Read each region from dorsais.txt
fig = pygmt.Figure()

with fig.subplot(
    nrows=2,
    ncols=4,
    figsize=("60c", "30c"),
    margins="0.5c",
):

    with open(dorsais_txt_path, "r", encoding="utf-8") as file:
        for i, linha in enumerate(file):

            # Ignore empty lines
            linha = linha.strip()
            if not linha:
                continue

            # Split the line
            lon_min, lon_max, lat_min, lat_max, nome = linha.split(",")

            # Convert coordinates to float
            lon_min = float(lon_min)
            lon_max = float(lon_max)
            lat_min = float(lat_min)
            lat_max = float(lat_max)

            # =====================================================
            # TOPOGRAPHY (0° to 360° longitude)
            # =====================================================

            lon_min_topo = lon_min
            lon_max_topo = lon_max

            if lon_min_topo < 0:
                lon_min_topo += 360

            if lon_max_topo < 0:
                lon_max_topo += 360

            dorsal_topografia = topografia.sel(
                longitude=slice(lon_min_topo, lon_max_topo),
                latitude=slice(lat_min, lat_max),
            )

            # =====================================================
            # MAGNETIC ANOMALY (-180° to 180° longitude)
            # =====================================================

            dorsal_magnetica = magnetic_anomaly.sel(
                longitude=slice(lon_min, lon_max),
                latitude=slice(lat_min, lat_max),
            )

            # -------------------------
            # Topography
            # -------------------------

            with fig.set_panel(panel=[0, i]):

                fig.grdimage(
                    grid=dorsal_topografia,
                    projection="M12c",
                    cmap="geo",
                    frame=["af", f'+t{nome}'],
                    shading=True,
                )


                # INSET global
                with fig.inset(
                    position="jTL+w3.5c+o0c",
                ):

                    fig.coast(
                        region="g",
                        projection="W0/3c",
                        land="gray85",
                        water="lightblue",
                        borders=1,
                        frame="g",
                    )

                    fig.plot(
                        x=[lon_min_topo, lon_max_topo, lon_max_topo, lon_min_topo, lon_min_topo],
                        y=[lat_min, lat_min, lat_max, lat_max, lat_min],
                        pen="2p,red",
                    )

            # -------------------------
            # Magnetic anomaly
            # -------------------------

            with fig.set_panel(panel=[1, i]):
                vmin = float(dorsal_magnetica.min())
                vmax = float(dorsal_magnetica.max())

                pygmt.makecpt(cmap="polar", series=[vmin, vmax])

                fig.grdimage(
                    grid=dorsal_magnetica,
                    projection="M12c",
                    cmap=True,
                    frame="af",
                    shading=True,
                )

                fig.colorbar(
                    position="JBC",
                    frame="af+lMagnetic anomaly (nT)",
                )

    fig.savefig("dorsais_comparacao.png")
