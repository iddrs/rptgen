from rptgen.escopo import Escopo


class RptGen:
    """Configurações globais do RptGen.

    Atributos
    ---------
    OUTPUT_BASE_DIR : str
        Diretório base para a saída dos relatórios gerados.
    DATA_BASE_DIR : str
        Diretório base para os dados usados na geração dos relatórios.
    """
    OUTPUT_BASE_DIR = r'./output'
    DATA_BASE_DIR = r'./data'


class Pad:
    """Configurações para manipulação dos arquivos do PAD.

    Atributos
    ---------
    BASE_DIR : str
        Diretório base para os arquivos de PAD.
    """
    BASE_DIR = r'C:\Users\Everton\Desktop\Prefeitura\PAD'


class Dcasp:
    """Configurações para a geração de relatórios DCASP.

    Atributos
    ---------
    BASE_OUTPUT_DIR : str
        Diretório base para a saída dos arquivos de DCASP.
    """
    BASE_OUTPUT_DIR = r'dcasp'


class Entidades:
    """Classe para armazenar informações sobre entidades e assinaturas.

    Atributos
    ---------
    entidades : dict[str, dict[str, str]]
        Dicionário contendo informações sobre as entidades.
    assinaturas : dict[str, dict[str, str]]
        Dicionário contendo informações sobre as assinaturas.
    """
    entidades = {
        'pm': {
            'nome': 'Prefeitura Municipal de Independência - RS',
            'cnpj': '87.612.826/0001-90'
        },
        'cm': {
            'nome': 'Câmara de Vereadores de Independência - RS',
            'cnpj': '12.292.535/0001-62'
        },
        'fpsm': {
            'nome': 'Fundo de Previdência dos Servidores Municipais de Independência - RS',
            'cnpj': '12.091.144/0001-80'
        },
        'mun': {
            'nome': 'Município de Independência - RS',
            'cnpj': '87.612.826/0001-90'
        },
        'exec': {
            'nome': 'Poder Executivo do Município de Independência - RS',
            'cnpj': '87.612.826/0001-90'
        },
        'leg': {
            'nome': 'Poder Legislativo do Município de Independência - RS',
            'cnpj': '12.292.535/0001-62'
        },
    }

    assinaturas = {
        'contador': {
            'nome': 'Everton da Rosa',
            'cargo': 'Contador',
            'documento': 'CRC RS-076595/O-3'
        },
        'prefeito': {
            'nome': 'João Edécio Graef',
            'cargo': 'Prefeito Municipal',
            'documento': 'CPF nº 189.955.190-53'
        },
        'secfaz': {
            'nome': 'Nerci José Mucha',
            'cargo': 'Secretário da Fazenda',
            'documento': 'CPF nº 410.980.800-68'
        },
        'presidente': {
            'nome': 'Fulano de Tal',
            'cargo': 'Presidente da Câmara',
            'documento': 'CPF nº xxx.xxx.xxx-xx'
        },
        'ucci': {
            'nome': 'Beltrano de Tal',
            'cargo': 'Controlador Interno',
            'documento': 'CPF nº xxx.xxx.xxx-xx'
        },
    }

    @classmethod
    def get_entidade(cls, escopo: Escopo) -> dict:
        """Retorna informações sobre uma entidade específica.

        Parâmetros
        ----------
        escopo : Escopo
            O escopo da entidade desejada.

        Retorna
        -------
        dict
            Dicionário contendo informações sobre a entidade especificada.
        """
        return cls.entidades[str(escopo)]

    @classmethod
    def get_assinaturas(cls) -> dict:
        """Retorna informações sobre as assinaturas.

        Retorna
        -------
        dict
            Dicionário contendo informações sobre as assinaturas.
        """
        return cls.assinaturas
