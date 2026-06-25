import pooch
import numpy as np

# Baixa as malhas de topografia e anomalia magnética globais usando a biblioteca Pooch.
fname = pooch.retrieve(
	url="https://drive.google.com/uc?export=download&id=1L15yntZf9M8QR37LsiRMDeCUMFqcaONH",
	known_hash="f8fc4486f6801aa85418cf50e337364a",
)

print(np.loadtxt(fname,encoding="utf8"))
# Baixa o arquivo com as especificações dos limites dos mapas desejados (ver tabela abaixo) também usando o Pooch. O arquivo contém os limites oeste, leste, sul, e norte da área de cada dorsal e o nome da dorsal.
# Lê as especificações de área e nome dos mapas do arquivo texto baixado.
# Lê as malhas dos arquivos baixados.
# Cria uma figura com os dados de anomalia magnética para cada área presente no arquivo de dorsais.
# Cria uma figura com os dados de topografia para cada área presente no arquivo de dorsais.
# As figuras devem ser feitas com a biblioteca PyGMT utilizando uma projeção e um mapa de cor adequados.
# As figuras devem conter o nome de cada dorsal lido do arquivo texto (não pode ser colocado na mão).
# O código deve utilizar o comando for para iterar sobre as diferentes áreas e criar as figuras (caso não utilize, o resultado será considerado somente parcialmente correto).
# Barras de cor são obrigatórias para os dados magnéticos mas podem ser omitidas nos dados de topografia.
# Avançado: Crie uma única figura utilizando subplots ao invés de várias figuras.
# Avançado: Adicione pequenos mapas globais (chamados de insets) na figura mostrando a localização de cada área com um retângulo.
