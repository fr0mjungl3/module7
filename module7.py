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

print("=== DORSais.txt ===")
print(dorsais_txt_content)


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

print("\n=== TOPOGRAFIA (arquivo baixado) ===")
print(topografia_nc_path)

# Carrega a malha de topografia como um DataArray
topografia = xr.load_dataarray(topografia_nc_path)
# print(topografia)

dorsal = topografia.sel(
	longitude=slice(0, 30), 
	latitude=slice(-60, -45),
)

# Cria o mapa da topografia com o PyGMT
fig = pygmt.Figure()
fig.grdimage(
	dorsal,
	projection="M20c",
	cmap="geo",
	frame=True,
	shading=True,
)
fig.colorbar()
# fig.show()
fig.savefig("map.png")
print("Saved map.png")



# Read each region from dorsais.txt
# Read each region from dorsais.txt
with open(dorsais_txt_path, "r", encoding="utf-8") as file:
    for linha in file:

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

        # Convert longitudes from [-180, 180] to [0, 360]
        if lon_min < 0:
            lon_min += 360

        if lon_max < 0:
            lon_max += 360

        # Slice the topography
        dorsal = topografia.sel(
            longitude=slice(lon_min, lon_max),
            latitude=slice(lat_min, lat_max),
        )

        # Create the figure
        fig = pygmt.Figure()
        fig.grdimage(
            grid=dorsal,
            projection="M20c",
            cmap="geo",
            frame=True,
            shading=True,
        )
        fig.colorbar()

        # Safe filename
        arquivo = (
            nome.lower()
                .replace(" ", "_")
                .replace("â", "a")
                .replace("á", "a")
                .replace("ã", "a")
                .replace("í", "i")
                .replace("ó", "o")
                .replace("ú", "u")
        )

        fig.savefig(f"{arquivo}.png")
        print(f"Saved {arquivo}.png")
