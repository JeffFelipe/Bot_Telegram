import time
import requests
from bs4 import BeautifulSoup
import os
from bot_telegram import enviar_arquivo_channel, enviar_msg_telegram


def buscar_atualizacao_bcg():
    cookies = {
        'PHPSESSID_': 'ID_USUARIO',
        'PHPSESSID': 'ID_USUARIO',
        'sc_actual_lang_SISBOL': 'pt_br',
    }  

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        # 'Cookie': 'PHPSESSID_=ID_USUARIO; PHPSESSID=ID_USUARIO; sc_actual_lang_SISBOL=pt_br',
        'Origin': 'https://sisbol.pm.ce.gov.br',
        'Referer': 'https://sisbol.pm.ce.gov.br/menu_bcg/menu_bcg_form_php.php?sc_item_menu=item_77&sc_apl_menu=con_boletins_bcg&sc_apl_link=%2F&sc_usa_grupo=',
        'Sec-Fetch-Dest': 'iframe',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    data = {
        'nmgp_parms': 'nm_run_menu?#?1?@?nm_apl_menu?#?menu_bcg?@?script_case_init?#?1',
        'script_case_init': '1',
        'nm_apl_menu': 'menu_bcg',
    }

    try:
        response = requests.post(
            'https://sisbol.pm.ce.gov.br/con_boletins_bcg/con_boletins_bcg.php',
            cookies=cookies,
            headers=headers,
            data=data
        )
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            element = soup.find(id='id_sc_field_doc_pdf_1')
            conteudo = element
            href_bcg = conteudo.find('a').get('href')

            if href_bcg.endswith('.pdf'):
                with open("sisbol.txt", "a+") as arquivo:
                    arquivo.seek(0)
                    bcgs_antigos = [bcg.strip() for bcg in arquivo.readlines()]
                    if href_bcg not in bcgs_antigos:
                        print('Novo BCG')
                        arquivo.write(f'{href_bcg}\n')
                        file_name = href_bcg.split('/')[-1]
                        return file_name
                    else:
                        return False
                        """
                        aqui abaixo serve para comparar a data
                        match = re.search(r"\d{2}\.\d{2}\.\d{2}", href_bcg)                         
                        if match:
                            data_str = match.group(0)
                            data = datetime.strptime(data_str, "%d.%m.%y").date()
                            # agora você tem um objeto data contendo a data 24/03/2023
                            data_referencia = datetime.now()
                        """
        else:
            return False

        """
        SAlva a data do bcg extraido num arquivo .txt e verifica se o atual do request é maior que ele, se sim, fazer a chamada no novo request, extraindo o 
        atual bcg e decidindo como utilizá-lo
        """

    except requests.exceptions.ConnectTimeout as e:
        print(e)


def download_file(href_bcg):
    base_url = "https://sisbol.pm.ce.gov.br/"
    file_path: str = href_bcg
    pdf_url = base_url + file_path
    response = requests.get(pdf_url)
    file_name = href_bcg.split('/')[-1]

    with open(file_name, "wb") as f:
        f.write(response.content)
        return file_name  # preciso deletar esse arquivo após o uso


def deletar_arquivo_atual(nome_arquivo):
    os.remove(nome_arquivo)


def main():
    while True:
        chamada = buscar_atualizacao_bcg()

        if chamada:
            canal = 'BCG_PMCE'
            # arquivo = download_file(chamada)
            mensagem = f'📄 {chamada} publicado! \n\nFaça login em https://sisbol.pm.ce.gov.br/login_bcg/ para acessá-lo'
            enviar_msg_telegram('ID_telegram', mensagem)
            print(chamada)
            time.sleep(60)
            #deletar_arquivo_atual(arquivo)

        time.sleep(60)


if __name__ == '__main__':
    main()
